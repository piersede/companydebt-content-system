"""Stranger-read step for editorial pages.

Purpose
-------
The mechanical gate (`article_audit.py`) and the writer's own voice audit
(`voice_audit.py`) both share a blind spot: they are gamed by writing to hit
the rules rather than to serve the reader. A stressed director landing cold
on the page sees things a writer who has been in the drafting session for
hours cannot see. This script produces the outside-eye read that the writer
cannot.

Two modes:

1. Interactive prompt mode (default): prints a persona-anchored prompt and a
   template response file for you to hand to a fresh agent (e.g. via the
   Agent tool in your Claude Code session, or by pasting into any other
   assistant). You paste the response text into the file it printed. The
   `voice_audit.py --stranger-read-report <path>` flag then references it.

2. Fill mode (`--fill <path>`): validates the response file (rejects empty
   or template-only submissions) and stamps it with the current prose SHA so
   the audit can prove the report matches the draft it claims to review.

The stranger-read persona is anchored in editorial-os/17-audience-and-persona.md.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO = SCRIPTS_DIR.parent
REPORTS_DIR = REPO / "editorial-os" / "stranger-reads"


# WARNING TO FUTURE MAINTAINERS -- do not "restore" the old question 5.
#
# Until 2026-08-13 question 5 read:
#     "Did the page acknowledge how you feel before it gave you rules to
#      follow?"
#
# That question actively trained the failure this whole gate exists to catch.
# On the company-ccj-mortgage-lender-criteria page the chain was documented in
# editorial-os/stranger-reads/company-ccj-mortgage-lender-criteria_2026-08-13T042755Z.md:
#
#   round 1, Q5 -> "No. Not a word."
#   the writer responded by inventing a scene: "If you are reading this late,
#   with an application already moving and a letter on the desk you did not
#   want..."
#   round 3, Q5 -> "'a letter on the desk you did not want' - that got me.
#   That's my actual desk."
#
# The gate rewarded a fabricated evening, a fabricated letter and a fabricated
# emotional state. That is precisely what humanise.md Part D and
# 15-good-vs-bad-examples.md ban as borrowed empathy and performance. Two
# governance artefacts were pulling in opposite directions, and the mechanical
# one won.
#
# Question 5 now detects performance instead of rewarding it. Question 6 tests
# for synthetic expertise, which is the other half of the same failure.
PERSONA_PROMPT = """You are a UK limited-company director.

You have not slept properly for the last week. HMRC has sent a letter you do
not fully understand. Your bookkeeper is not answering emails today. You have
opened this page for the first time on your phone at 11:40pm.

That is your situation. It is NOT something the page is supposed to know, guess
at or describe back to you. A page that invents your evening has not understood
you, it has flattered you. Judge it on whether it answers your question.

Read the opening 500 words of the page below, then answer these questions
briefly and honestly:

1. Which word or phrase did you have to re-read?
2. Which term would you have to look up before you could act on the advice?
3. At which point, if any, would you have closed the tab?
4. If a friend asked you 'what does this page tell me to do?' after your
   first read, what would you say?
5. Did any sentence feel written to make you feel something rather than to
   tell you something? Quote it. Include anything that describes your mood,
   your evening, your kitchen table or what is keeping you awake.
6. Does the page claim anything about what 'most' people do, what 'usually'
   happens, or what the writer has 'often seen', that it does not show you
   evidence for? Quote it.

Answer as the director, not as an editor. Do not soften your answer to be
polite. Do not give the page credit for sympathising with you: you came here
for an answer, not for company. If the opening is fine, say so plainly.

---

PAGE OPENING TO REVIEW:

{opening}
"""

RESPONSE_TEMPLATE = """# Stranger-read response for {slug}

Prose SHA at time of request: {prose_sha}
Requested: {timestamp}

Paste the responding agent's text below the line, verbatim. Do NOT edit it.
The auditor validates that the response contains substantive answers to the
six persona questions. Empty responses or template stubs are rejected.

---

"""


def prose_sha(raw: str) -> str:
    plain = re.sub(r"<[^>]+>", " ", raw)
    plain = re.sub(r"\s+", " ", plain).strip().encode("utf-8")
    return hashlib.sha256(plain).hexdigest()


def extract_opening(raw: str, words: int = 500) -> str:
    body_start = raw.find("<article>")
    body_start = 0 if body_start < 0 else body_start + len("<article>")
    body = raw[body_start:]
    text = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    parts = text.split()
    return " ".join(parts[:words])


def find_draft(slug: str) -> Path | None:
    matches = sorted((REPO / "drafts").glob(f"*_{slug}.html"))
    return matches[0] if matches else None


def cmd_prompt(args) -> int:
    draft = find_draft(args.slug)
    if not draft or not draft.exists():
        print(f"ERROR: draft not found for slug: {args.slug}", file=sys.stderr)
        return 2
    raw = draft.read_text(encoding="utf-8")
    opening = extract_opening(raw, args.words)
    sha = prose_sha(raw)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    out = REPORTS_DIR / f"{args.slug}_{ts}.md"
    out.write_text(
        RESPONSE_TEMPLATE.format(slug=args.slug, prose_sha=sha, timestamp=ts),
        encoding="utf-8",
    )
    print("STRANGER-READ PROMPT")
    print("=" * 70)
    print(PERSONA_PROMPT.format(opening=opening))
    print("=" * 70)
    print()
    print(f"Response template written to: {out.relative_to(REPO)}")
    print("Paste the responding agent's answer verbatim under the line, then run:")
    print(f"  python scripts/stranger_read.py --fill {out.relative_to(REPO)}")
    return 0


def cmd_fill(args) -> int:
    path = Path(args.fill)
    if not path.exists():
        print(f"ERROR: report file not found: {path}", file=sys.stderr)
        return 2
    text = path.read_text(encoding="utf-8")
    # Split on the "---" separator; response is everything after the FINAL "---".
    parts = text.split("\n---\n")
    if len(parts) < 2:
        print("ERROR: response file has no '---' separator; paste the agent response under the line.", file=sys.stderr)
        return 3
    response = parts[-1].strip()
    if len(response) < 120:
        print(f"ERROR: response is too short ({len(response)} chars); a stranger-read pass needs substantive answers.", file=sys.stderr)
        return 3
    # Ensure at least a mention of two of the six question numbers so we know
    # the responder actually answered rather than commenting freely.
    numbered = sum(1 for n in ("1.", "2.", "3.", "4.", "5.", "6.") if n in response)
    if numbered < 2:
        print(f"ERROR: response does not answer at least two of the numbered questions.", file=sys.stderr)
        return 3
    # A relative --fill path (the obvious way to type it) blew up here on
    # relative_to, after all the validation had already passed.
    try:
        shown = path.resolve().relative_to(REPO)
    except ValueError:
        shown = path
    print(f"Report validated: {shown}")
    print(f"  response length: {len(response)} chars")
    print(f"  numbered answers detected: {numbered} of 6")
    print("Pass the file to voice_audit.py with --stranger-read-report <path>")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Stranger-read step: an outside eye on the opening of the page.",
    )
    sub = ap.add_subparsers(dest="mode")
    # Default: prompt mode
    ap.add_argument("--slug", help="Page slug (drafts/*_<slug>.html) — prompt mode")
    ap.add_argument("--words", type=int, default=500, help="How many opening words to include")
    ap.add_argument("--fill", help="Path to a response file to validate after the agent has answered")
    args = ap.parse_args()

    if args.fill:
        return cmd_fill(args)
    if args.slug:
        return cmd_prompt(args)
    ap.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
