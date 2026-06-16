"""Shared foundation for the Company Debt insolvency data hub.

This package is the reusable layer behind every data page (the flagship
statistics page, the hub landing page, and future sector / tracker pages).

Modules:
    registry  -- load and validate the source registry, release ledger and
                 caveats library; resolve sources, releases and caveat text.

Design note: V1 stores the data architecture (source_registry, dataset_release,
stat_observation) as documented JSON under data/_meta and data/<dataset>/, not a
database. The JSON follows the shapes in the hub brief so the heavier ingestion
machinery (Gazette events, company matching) can be added later without rework.
"""
