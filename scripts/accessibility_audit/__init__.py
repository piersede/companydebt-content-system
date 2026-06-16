"""AI Agent Readability & Accessibility Audit.

Audits a URL for how well AI agents (and assistive technology) can read and
operate the page — the rendered accessibility tree, not just the source HTML.

Built from a real remediation on a sister site where the entire article body was
invisible to agents because a caching plugin deferred off-screen rendering. See
README.md for the full findings catalogue and remediation playbook.

Entry point: `python -m accessibility_audit --url https://example.com`
"""

from .audit import audit_url, Finding, Report  # noqa: F401
