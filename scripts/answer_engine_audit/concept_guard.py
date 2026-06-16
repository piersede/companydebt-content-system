"""Concept-aware already-covered guard (UK company-insolvency / debt domain).

The extract stage's already-covered guard used to be *vocabulary-blind*: the
delta model was asked to drop any nugget the page already states, but a cheap
model matches on literal tokens, so it re-flags a fact phrased "the director
kept trading while insolvent" when the page says "continued to trade after the
company became insolvent (wrongful trading)". The apply-lists then balloon with
``present_but_weak`` / ``[ADD]`` items that ARE already on the page under
different words, forcing heavy manual grep-with-synonyms triage.

This module is the deterministic backstop that runs AFTER the model pass, over
the FULL page text (prose + JSON-LD). For each candidate nugget it asks: does the
page already express this CONCEPT, near this ENTITY/route? It recognises the
recurring company-insolvency concepts under their synonyms (wrongful trading /
trading while insolvent, preference / preferring a creditor, overdrawn director's
loan account, phoenix / s.216 name reuse, Crown preference, winding-up petition,
CVL/CVA/MVL/administration/strike-off, ...), with light stemming and
phrase/bigram matching, and a content-word-overlap fallback for concepts not in
the map.

Two hard protections keep it from eating genuine work:

1. **Corrections are never suppressed.** ``outdated`` / ``contradicted`` nuggets
   say the page states something WRONG — the concept IS on the page, so a concept
   match would wrongly hide the correction. They bypass the guard.

2. **Figure-bearing nuggets need the FIGURE on the page, not just the concept.**
   A page mentioning "a winding-up petition has a deadline" does not cover the
   nugget "21 days to respond to a statutory demand" unless "21" is actually
   present near the concept. So a nugget carrying a number is only suppressed when
   that number co-occurs with its entity; otherwise it is kept (this protects real
   statutory figures like the 21-day statutory-demand window or a 6-year
   disqualification).

The optional semantic layer (``semantic=True``, behind the ``--semantic-guard``
CLI flag) embeds the residual nuggets against the page sentences via Gemini and
suppresses on cosine similarity. It is OFF by default so dry-runs and ordinary
runs make ZERO extra API calls.
"""

from __future__ import annotations

import re
from dataclasses import asdict
from typing import Any, Iterable

from .ledger import Nugget

# --------------------------------------------------------------------------
# Concept vocabulary — canonical concept -> the surface forms that express it.
# Lowercase. Multi-word entries are matched as phrases (covers bigrams); single
# words are matched on a stemmed token set so plural/verb variants collapse.
# This is the UK company-insolvency / company-debt map (the BusinessExpert map
# of payments concepts does not apply here).
# --------------------------------------------------------------------------
CONCEPT_MAP: dict[str, set[str]] = {
    "wrongful-trading": {
        "wrongful trading", "trading while insolvent", "trading whilst insolvent",
        "continued to trade", "continue to trade", "kept trading", "carried on trading",
        "knew or ought", "no reasonable prospect", "worsened the position",
    },
    "fraudulent-trading": {
        "fraudulent trading", "intent to defraud", "defraud creditors",
        "intention to defraud", "dishonest", "dishonestly",
    },
    "misfeasance": {
        "misfeasance", "breach of duty", "breach of fiduciary", "fiduciary duty",
        "misapplied", "misapplication", "breached their duties", "breached his duties",
    },
    "director-disqualification": {
        "disqualification", "disqualified", "disqualify", "banned as a director",
        "director ban", "unfit conduct", "cdda", "company directors disqualification",
        "up to 15 years", "2 to 15 years", "undertaking",
    },
    "personal-guarantee": {
        "personal guarantee", "personally liable", "personal liability",
        "personally guarantee", "pg", "guaranteed the debt", "called in",
    },
    "overdrawn-dla": {
        "director's loan account", "directors loan account", "overdrawn", "dla",
        "overdrawn loan account", "loan account", "repay the loan", "money you owe the company",
        "owe the company", "drawn more than",
    },
    "preference": {
        "preference", "preferential payment", "preferring a creditor",
        "preferring creditors", "preferred a creditor", "paying one creditor",
        "unlawful preference", "voidable preference", "favoured", "favouring",
    },
    "crown-preference": {
        "crown preference", "preferential creditor", "secondary preferential",
        "hmrc preferential", "hmrc priority", "vat", "paye", "preferential status",
        "moved up the order", "ahead of floating",
    },
    "phoenix-name-reuse": {
        "phoenix", "phoenixing", "reuse the name", "re-use the name", "reuse a name",
        "same or similar name", "prohibited name", "s.216", "section 216",
        "s216", "restricted name", "trading under the same name",
    },
    "creditor-ranking": {
        "order of priority", "ranking of creditors", "waterfall", "priority order",
        "secured creditors", "preferential creditors", "unsecured creditors",
        "prescribed part", "floating charge", "fixed charge", "who gets paid first",
        "paid first", "paid last", "distribution to creditors",
    },
    "winding-up-petition": {
        "winding-up petition", "winding up petition", "compulsory liquidation",
        "court petition", "statutory demand", "wound up", "petition to wind up",
        "21 days", "750", "court order",
    },
    "creditors-voluntary-liquidation": {
        "creditors voluntary liquidation", "creditors' voluntary liquidation", "cvl",
        "voluntary liquidation", "shareholders resolution", "75%", "deemed consent",
    },
    "members-voluntary-liquidation": {
        "members voluntary liquidation", "members' voluntary liquidation", "mvl",
        "solvent liquidation", "declaration of solvency", "capital distribution",
        "business asset disposal relief", "entrepreneurs relief",
    },
    "company-voluntary-arrangement": {
        "company voluntary arrangement", "cva", "arrangement with creditors",
        "repay over", "monthly contributions", "75% by value", "nominee", "supervisor",
    },
    "administration": {
        "administration", "administrator", "pre-pack", "pre pack", "prepack",
        "moratorium", "breathing space", "rescue the company", "going concern sale",
    },
    "strike-off-dissolution": {
        "strike off", "strike-off", "struck off", "dissolution", "dissolve",
        "ds01", "voluntary dissolution", "objection to strike off", "restoration",
    },
    "bounce-back-loan": {
        "bounce back loan", "bounce-back loan", "bbl", "cbils", "covid loan",
        "government-backed loan", "government backed loan",
    },
    "insolvency-practitioner": {
        "insolvency practitioner", "licensed insolvency practitioner", "ip",
        "office holder", "appoint an", "liquidator", "appointed to",
    },
    "antecedent-transactions": {
        "transaction at undervalue", "undervalue", "antecedent", "clawback",
        "claw back", "set aside", "reviewable transaction", "transactions defrauding",
    },
    "hmrc-personal-liability": {
        "personal liability notice", "pln", "joint and several", "hmrc can pursue",
        "personally for the company's tax", "security deposit", "personally for vat",
    },
    "redundancy-claims": {
        "redundancy", "redundancy payments service", "rps", "owed wages",
        "employee claims", "unpaid wages", "statutory redundancy", "notice pay",
    },
}

# Generic insolvency / structural words that must NOT count as the distinguishing
# content of a nugget when doing the content-word-overlap fallback. Includes the
# stop list plus insolvency boilerplate that appears on essentially every page.
# NOTE: route names (liquidation, administration, creditor, ...) are deliberately
# NOT here — they are legitimate entity tokens used to scope concept hits.
_GENERIC = {
    "business", "company", "companies", "director", "directors", "process",
    "option", "options", "money", "pay", "paid", "payment", "payments", "owe",
    "owed", "owing", "amount", "ltd", "limited", "uk", "use", "uses", "using",
    "include", "includes", "included", "involve", "involves", "available",
    "need", "needs", "want", "get", "gets", "also", "based", "via", "per",
    "month", "monthly", "year", "years", "annual", "small", "large", "new",
    "current", "standard", "situation", "situations", "case", "cases", "thing",
    "things", "people", "person", "good", "best", "make", "makes", "well",
    "help", "helps", "able", "way", "ways", "step", "steps", "type", "types",
}

_STOP = {
    "the", "a", "an", "and", "or", "of", "to", "for", "on", "in", "at", "by",
    "with", "is", "are", "be", "from", "up", "as", "it", "its", "this", "that",
    "you", "your", "they", "their", "has", "have", "but", "not", "no", "if",
    "when", "than", "then", "any", "all", "each", "into", "does", "do", "can",
    "will", "may", "such", "both", "more", "most", "while", "which", "who",
}

# A nugget detail mentions a figure if its value or text carries a number with a
# money/percent/quantity/time context (statutory deadlines and bans are common).
_FIGURE = re.compile(
    r"(£\s*\d[\d,.]*)|(\d[\d,.]*\s*%)|(\d[\d,.]*\s*(p|pence|days?|weeks?|months?|"
    r"years?|x))\b", re.I)

# Co-occurrence window in characters: a concept counts as covered "near" the
# entity if a surface form falls within this many chars of an entity mention.
# ~170 chars is roughly one sentence, tight enough to scope a page where several
# routes interleave.
_WINDOW = 170


def has_figure(n: Nugget) -> bool:
    """True if the nugget pins a specific number (money/%/quantity/time). Such
    nuggets are only suppressed when the FIGURE itself is on the page, not merely
    the concept — this is what protects statutory-figure corrections."""
    return bool(_FIGURE.search(n.value or "")) or bool(_FIGURE.search(n.detail or ""))


def _stem(word: str) -> str:
    """Light en-GB stemmer: collapse common plural/verb suffixes so 'holds',
    'holding', 'restricted' map toward their root. Deliberately crude — we only
    need phrasing variants of the same word to collide, not linguistic accuracy."""
    w = word.lower()
    for suf in ("ies",):
        if w.endswith(suf) and len(w) > 4:
            return w[: -len(suf)] + "y"
    for suf in ("ing", "ed", "es", "s"):
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            return w[: -len(suf)]
    return w


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").lower())


def _figures_in(text: str) -> set[str]:
    """Bare numeric tokens (digits only, commas stripped) in a string, so a
    nugget figure can be matched against the page regardless of £/%/wording."""
    return {m.replace(",", "") for m in re.findall(r"\d[\d,]*", text or "")}


class PageIndex:
    """Pre-tokenised page text for cheap repeated lookups: normalised text (for
    phrase/figure substring search), a stemmed token set, and the char positions
    of every entity (route/body) mention so concept hits can be scoped."""

    def __init__(self, page_text: str) -> None:
        self.norm = _norm(page_text)
        self.stems = {_stem(w) for w in re.findall(r"[a-z][a-z'-]+", self.norm)}
        self.figures = _figures_in(self.norm)

    def phrase_positions(self, surface: str) -> list[int]:
        """All start indices of a (possibly multi-word) surface form. Single
        words match on stem so plural/verb variants count; phrases match as a
        normalised substring (covers bigrams)."""
        s = surface.lower().strip()
        if not s:
            return []
        if " " in s or "-" in s:
            out, start = [], 0
            while True:
                i = self.norm.find(s, start)
                if i == -1:
                    break
                out.append(i)
                start = i + 1
            return out
        # single word -> stem-aware: scan word tokens
        stem = _stem(s)
        out = []
        for m in re.finditer(r"[a-z][a-z'-]+", self.norm):
            if _stem(m.group(0)) == stem:
                out.append(m.start())
        return out

    def entity_positions(self, aliases: Iterable[str]) -> list[int]:
        pos: list[int] = []
        for a in aliases:
            pos.extend(self.phrase_positions(a))
        return sorted(pos)


def _entity_aliases(n: Nugget) -> list[str]:
    """Distinct, page-matchable entity tokens for a nugget: provider/route +
    card_name words, dropping generic words and short fragments."""
    aliases: set[str] = set()
    for raw in (n.provider, n.card_name):
        s = (raw or "").strip().lower()
        if not s:
            continue
        aliases.add(s)
        for w in re.findall(r"[a-z][a-z'-]+", s):
            if len(w) >= 4 and w not in _GENERIC and w not in _STOP:
                aliases.add(w)
    return [a for a in aliases if a]


def _concepts_in_detail(detail: str) -> list[str]:
    """Which mapped concepts the nugget's own text invokes."""
    norm = _norm(detail)
    stems = {_stem(w) for w in re.findall(r"[a-z][a-z'-]+", norm)}
    hits: list[str] = []
    for concept, surfaces in CONCEPT_MAP.items():
        for s in surfaces:
            if " " in s or "-" in s:
                if s in norm:
                    hits.append(concept)
                    break
            elif _stem(s) in stems:
                hits.append(concept)
                break
    return hits


def _content_words(detail: str) -> list[str]:
    """Distinguishing content stems of a nugget (drop stop + generic words)."""
    words = re.findall(r"[a-z][a-z'-]+", _norm(detail))
    out: list[str] = []
    for w in words:
        if len(w) < 4 or w in _STOP or w in _GENERIC:
            continue
        st = _stem(w)
        if st not in out:
            out.append(st)
    return out


def _near(positions: list[int], targets: list[int], window: int) -> int:
    """Count how many of ``positions`` fall within ``window`` chars of any
    target. If there are no targets (entity not on page / route-less), every
    position counts."""
    if not targets:
        return len(positions)
    count = 0
    for p in positions:
        if any(abs(p - t) <= window for t in targets):
            count += 1
    return count


# Depth thresholds: how many on-page co-occurrences are needed to treat a status
# as already-covered. A model "missing" verdict is refuted by a single
# co-occurrence (it claimed ABSENT); a "present_but_weak" needs corroboration
# that the topic is genuinely covered, not a single passing mention.
_MIN_COOCCUR = {"missing": 1, "present_but_weak": 2, "buried": 2, "unsupported": 1}
# Statuses the guard never touches: corrections (the concept IS on the page, but
# stated wrongly) and already-resolved verdicts.
_SKIP_STATUS = {"outdated", "contradicted", "present", "not_relevant"}


def _covered_lexically(n: Nugget, idx: PageIndex) -> tuple[bool, str]:
    """Is this nugget already covered by the page, by concept or content-word
    overlap, scoped to its entity? Returns (covered, reason)."""
    entities = _entity_aliases(n)
    epos = idx.entity_positions(entities)
    threshold = _MIN_COOCCUR.get(n.article_status, 1)

    # 1. Mapped-concept path (synonym-aware).
    for concept in _concepts_in_detail(n.detail):
        cpos: list[int] = []
        for s in CONCEPT_MAP[concept]:
            cpos.extend(idx.phrase_positions(s))
        if _near(cpos, epos, _WINDOW) >= threshold:
            return True, f"concept:{concept}"

    # 2. Content-word-overlap fallback (concepts not in the map). Covered only if
    # (nearly) all the nugget's distinguishing words land near the entity in one
    # window — a high bar, so we don't suppress genuine gaps that merely share a
    # word or two with the page.
    words = _content_words(n.detail)
    if len(words) >= 2:
        word_pos = {w: [m.start() for m in re.finditer(r"[a-z][a-z'-]+", idx.norm)
                        if _stem(m.group(0)) == w] for w in words}
        present = [w for w in words if word_pos[w]]
        if len(present) / len(words) >= 0.8:
            anchors = epos or [p for w in present for p in word_pos[w]]
            for a in anchors:
                near_words = sum(
                    1 for w in present
                    if any(abs(p - a) <= _WINDOW for p in word_pos[w]))
                if near_words == len(words):
                    return True, "content-overlap"
    return False, ""


def _figure_on_page(n: Nugget, idx: PageIndex) -> bool:
    """For a figure-bearing nugget: is the specific number present on the page?
    (Concept presence alone is not enough — protects statutory-figure corrections.)"""
    nums = _figures_in(n.value) | _figures_in(n.detail)
    nums = {x for x in nums if len(x) >= 2 or x not in {"0", "1", "2", "3"}}
    if not nums:
        return False
    return any(x in idx.figures for x in nums)


class GuardResult:
    def __init__(self, kept: list[Nugget], suppressed: list[tuple[Nugget, str]]):
        self.kept = kept
        self.suppressed = suppressed

    @property
    def counts(self) -> dict[str, int]:
        by_reason: dict[str, int] = {}
        for _n, reason in self.suppressed:
            tag = reason.split(":")[0]
            by_reason[tag] = by_reason.get(tag, 0) + 1
        return {"kept": len(self.kept), "suppressed": len(self.suppressed), **by_reason}


def guard_nuggets(nuggets: list[Nugget], page_text: str, *,
                  semantic: bool = False, model: str = "gemini-2.5-flash",
                  sim_threshold: float = 0.74) -> GuardResult:
    """Drop nuggets the page already covers (same concept, near the same entity).

    Deterministic by default. ``semantic=True`` adds a Gemini-embedding pass over
    the residual (still-flagged, non-figure) nuggets — opt-in, so the default
    path makes no extra API calls.
    """
    idx = PageIndex(page_text)
    kept: list[Nugget] = []
    suppressed: list[tuple[Nugget, str]] = []
    residual: list[Nugget] = []

    for n in nuggets:
        if n.article_status in _SKIP_STATUS:
            kept.append(n)
            continue
        if has_figure(n):
            # Only the specific figure being on the page (near the entity) counts;
            # concept-only coverage must NOT hide a new/corrected number.
            if _figure_on_page(n, idx):
                covered, _ = _covered_lexically(n, idx)
                if covered:
                    suppressed.append((n, "figure-on-page"))
                    continue
            kept.append(n)
            continue
        covered, reason = _covered_lexically(n, idx)
        if covered:
            suppressed.append((n, reason))
        else:
            kept.append(n)
            residual.append(n)

    if semantic:
        sem_residual = [n for n in residual if not has_figure(n)]
        sem_suppressed = _semantic_pass(sem_residual, page_text, model=model,
                                        threshold=sim_threshold)
        if sem_suppressed:
            drop = {id(n) for n in sem_suppressed}
            kept = [n for n in kept if id(n) not in drop]
            suppressed.extend((n, "semantic") for n in sem_suppressed)

    return GuardResult(kept, suppressed)


def _page_sentences(page_text: str, *, max_sentences: int = 400) -> list[str]:
    raw = re.split(r"(?<=[.!?])\s+|\n+", page_text or "")
    out = [s.strip() for s in raw if len(s.strip()) >= 25]
    return out[:max_sentences]


def _semantic_pass(nuggets: list[Nugget], page_text: str, *, model: str,
                   threshold: float) -> list[Nugget]:
    """Embed each residual nugget against the page sentences (Gemini embeddings);
    suppress a nugget whose max cosine similarity to any sentence exceeds the
    threshold. Cost-bounded: one batched embed of the page sentences (reused) +
    one batched embed of the nuggets. Any failure degrades to 'no suppression'."""
    if not nuggets:
        return []
    sentences = _page_sentences(page_text)
    if not sentences:
        return []
    try:
        from .core import gemini_client

        client = gemini_client()
        embed_model = "text-embedding-004"

        def _embed(texts: list[str]) -> list[list[float]]:
            vecs: list[list[float]] = []
            for i in range(0, len(texts), 100):  # API batch ceiling
                resp = client.models.embed_content(
                    model=embed_model, contents=texts[i:i + 100])
                vecs.extend([e.values for e in resp.embeddings])
            return vecs

        svecs = _embed(sentences)
        nvecs = _embed([n.detail for n in nuggets])
    except Exception as exc:  # never block discovery on an embedding hiccup
        import sys
        print(f"[concept-guard] semantic pass skipped: {type(exc).__name__}: {exc}",
              file=sys.stderr)
        return []

    def _cos(a: list[float], b: list[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        na = sum(x * x for x in a) ** 0.5
        nb = sum(y * y for y in b) ** 0.5
        return dot / (na * nb) if na and nb else 0.0

    out: list[Nugget] = []
    for n, nv in zip(nuggets, nvecs):
        if any(_cos(nv, sv) >= threshold for sv in svecs):
            out.append(n)
    return out


def suppressed_records(result: GuardResult) -> list[dict[str, Any]]:
    """Serialisable rows for the already-covered sidecar (audit transparency)."""
    rows: list[dict[str, Any]] = []
    for n, reason in result.suppressed:
        row = asdict(n)
        row["_suppressed_reason"] = reason
        rows.append(row)
    return rows
