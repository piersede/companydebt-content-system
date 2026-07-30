"""Shared voice / human-authorship metrics.

Single source of truth for the measurable half of
`editorial-os/docs/human-authorship-voice-engine.md`. Imported by both:

  - `voice_audit.py`  -- computes the metrics and writes the attestation record
  - `article_audit.py` -- the gate checks that read the record and re-measure

Only the MECHANICAL parts live here (pronoun density, per-section `you`
coverage, a paragraph-length rhythm proxy, and a prose hash for freshness).
The subjective parts (concrete-scene quality, evaluative bite, tone modulation,
read-aloud flatness) cannot be scored reliably by a script -- they are recorded
as an operator/Opus attestation in the voice-audit sidecar, not measured here.
"""

from __future__ import annotations

import hashlib
import re

# Thresholds mirror human-authorship-voice-engine.md "Pronoun density targets".
YOU_FLOOR = 8.0
YOU_CEILING = 30.0
WE_FLOOR = 5.0
I_CEILING = 5.0
SECTION_MIN_WORDS = 200      # a section longer than this must serve the reader with >=1 "you"
RHYTHM_MIN_CV = 0.30         # paragraph-length coefficient of variation floor (uniform => flat)
RHYTHM_MIN_PARAS = 8         # only judge rhythm once there are enough paragraphs to have any


def _strip_tags(html: str) -> str:
    return re.sub(r"<[^>]+>", " ", html)


def body_html(raw: str) -> str:
    """The voice-bearing body: everything before the methodology/sources asides,
    with data tables removed (table cells are data, not authored prose)."""
    body = raw.split('<aside class="cd-methodology"')[0]
    body = body.split('<aside class="cd-sources"')[0]
    body = re.sub(r"<table.*?</table>", " ", body, flags=re.S | re.I)
    return body


def body_paragraphs(raw: str) -> list[str]:
    """Stripped inner text of each <p> in the voice-bearing body (includes FAQ
    answers and call-out prose; excludes tables, methodology and sources)."""
    paras = re.findall(r"<p[^>]*>(.*?)</p>", body_html(raw), re.S | re.I)
    return [_strip_tags(p).strip() for p in paras if _strip_tags(p).strip()]


def body_text(raw: str) -> str:
    return " ".join(body_paragraphs(raw))


def prose_sha(raw: str) -> str:
    """SHA-256 of the normalised body prose. Any change to authored prose
    invalidates a voice-audit record; edits to tables/comments/attributes do
    not. This is the freshness anchor that stops a voice pass being run once and
    then outrun by later prose edits."""
    norm = re.sub(r"\s+", " ", body_text(raw)).strip().lower()
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()


def _count(pattern: str, text: str) -> int:
    return len(re.findall(pattern, text, re.I))


def pronoun_densities(raw: str) -> dict:
    text = body_text(raw)
    words = len(text.split()) or 1
    you = _count(r"\b(you|your|yours|yourself)\b", text)
    we = _count(r"\b(we|our|ours|us)\b", text)
    i = _count(r"\b(I|my|mine|me|myself)\b", text)
    per1k = lambda n: round(n / words * 1000, 1)
    return {
        "words": words,
        "you": you, "you_per_1k": per1k(you),
        "we": we, "we_per_1k": per1k(we),
        "i": i, "i_per_1k": per1k(i),
    }


def sections_over_200w_without_you(raw: str) -> list[dict]:
    """H2 sections whose prose exceeds SECTION_MIN_WORDS but contain zero 'you'.
    Per the voice engine: a section that long with no 'you' is not serving the
    reader. Returns the offending sections (empty list == pass)."""
    body = body_html(raw)
    parts = re.split(r"<h2[^>]*>(.*?)</h2>", body)
    offenders = []
    # parts = [pre, title1, seg1, title2, seg2, ...]
    for idx in range(1, len(parts), 2):
        title = _strip_tags(parts[idx]).strip()
        seg = parts[idx + 1] if idx + 1 < len(parts) else ""
        seg_text = " ".join(
            _strip_tags(p).strip() for p in re.findall(r"<p[^>]*>(.*?)</p>", seg, re.S | re.I)
        )
        wc = len(seg_text.split())
        you = _count(r"\b(you|your)\b", seg_text)
        if wc > SECTION_MIN_WORDS and you == 0:
            offenders.append({"section": title, "words": wc})
    return offenders


def rhythm_uniformity(raw: str) -> dict:
    """Advisory paragraph-length rhythm proxy. Flat writing tends to uniform
    paragraph lengths; the coefficient of variation (std/mean) captures that
    cheaply. Not a substitute for the read-aloud check, hence advisory only."""
    lens = [len(p.split()) for p in body_paragraphs(raw)]
    if len(lens) < RHYTHM_MIN_PARAS:
        return {"paras": len(lens), "cv": None, "uniform": False}
    mean = sum(lens) / len(lens)
    if mean == 0:
        return {"paras": len(lens), "cv": None, "uniform": False}
    var = sum((x - mean) ** 2 for x in lens) / len(lens)
    cv = round((var ** 0.5) / mean, 3)
    return {"paras": len(lens), "cv": cv, "uniform": cv < RHYTHM_MIN_CV}


def scene_proxy(raw: str) -> int:
    """A LOOSE proxy for concrete scenes, to help the operator, NOT a gate
    metric. Counts second-person/temporal concrete cues. The recorded scene
    count in the sidecar is the operator's judgement, not this number."""
    text = body_text(raw)
    cues = re.findall(
        r"\b(by the time|on a (?:monday|friday|morning)|the moment|sitting|"
        r"lie awake|brown envelope|at the pump|by friday|walks in|picks up the phone|"
        r"across the office|the letter|the knock|hands over)\b",
        text, re.I,
    )
    return len(cues)


def full_report(raw: str) -> dict:
    d = pronoun_densities(raw)
    return {
        "prose_sha": prose_sha(raw),
        "metrics": d,
        "sections_over_200w_without_you": sections_over_200w_without_you(raw),
        "rhythm": rhythm_uniformity(raw),
        "scene_proxy": scene_proxy(raw),
        "flags": {
            "you_below_floor": d["you_per_1k"] < YOU_FLOOR,
            "you_above_ceiling": d["you_per_1k"] > YOU_CEILING,
            "we_below_floor": d["we_per_1k"] < WE_FLOOR,
            "i_above_ceiling": d["i_per_1k"] > I_CEILING,
        },
    }
