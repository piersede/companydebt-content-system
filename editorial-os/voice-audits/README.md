# Voice self-audit records

One JSON file per page slug (`<slug>.json`). Each is the recorded attestation
that the human-authorship voice pass in
[`../docs/human-authorship-voice-engine.md`](../docs/human-authorship-voice-engine.md)
was actually run for that page.

`article_audit.py` **check 26** (hard gate) requires a record here whose
`prose_sha` matches the current draft prose. Any edit to the page's authored
prose changes the hash and invalidates the record, forcing the voice pass to be
re-run and re-attested. This is deliberate: it stops the voice step being run
once and then quietly outrun by later edits (the 2026-07-30 failure that
prompted this).

## Writing a record

Do the voice pass on Opus, then:

```bash
python scripts/voice_audit.py --slug <slug> --record \
  --by claude-opus-4-8 --scenes <n> --bite <n> \
  --tone pass --rhythm pass --read-aloud pass --verdict pass \
  --notes "short honest attestation"
```

The mechanical fields (`prose_sha`, pronoun densities, zero-`you` sections,
rhythm proxy) are measured automatically. The `--scenes/--bite/--tone/--rhythm/
--read-aloud/--verdict/--notes` fields are your attestation of the subjective
checks a script cannot score. Record honestly — a false attestation defeats the
gate.

`--verdict pass` is required for check 26 to pass. Run
`python scripts/voice_audit.py --slug <slug>` (no `--record`) to see the metrics
and whether an existing record is still fresh.

## Related mechanical checks

- **27** (hard): no 200-word+ section without a reader-serving `you`.
- **28** (advisory): `you` density within the 30/1k ceiling.
- **29** (advisory): paragraph-length rhythm not uniform (read aloud for flatness).
