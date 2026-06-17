"""Page assemblers for the insolvency data hub.

Each module turns a Claude Design reference (design-handoff/*.html) plus live
data from the backbone into (a) a standalone preview and (b) a WordPress-ready
draft (wp:html block, scoped under .cd-data-hub, CD-NO-AUTOEDIT sentinel).
Scripts and structured data go in the mu-plugin, not page content (KSES).
"""
