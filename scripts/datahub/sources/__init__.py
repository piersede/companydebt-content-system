"""Per-source data acquisition for the insolvency data hub.

Each module here fetches from one upstream source, stores the result under
data/<dataset>/, and records a release in that dataset's dataset_release.json
(the fetch-store-log pattern). Sources map to entries in
data/_meta/source_registry.json.
"""
