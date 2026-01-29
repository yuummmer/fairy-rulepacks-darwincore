# DwC-A fixtures

This folder contains small Darwin Core Archive (DwC-A) ZIP fixtures used to test:
- archive-level checks (meta.xml present/parseable, referenced core file exists)
- downstream core-table checks (e.g., required terms, uniqueness, ranges)

Fixtures here are intentionally small and curated to produce predictable PASS/FAIL outcomes.

## Proof pack bundle (optional)
- `ipt_occurrence_proofpack_v1.0.zip` — curated occurrence-core DwC-A proof pack bundle (for convenience; canonical fixtures are listed below)

## Ready-to-validate ZIP fixtures

- `zips/good.zip` — expected: **PASS**
- `zips/broken-1-duplicate-ids.zip` — expected: **FAIL**
  - Duplicate DwC-A core IDs; `meta.xml` uses `<id index="0" />`
- `zips/broken-2-missing-scientificName.zip` — expected: **FAIL**
  - Required term missing: `scientificName` removed from `occurrence.txt`
- `zips/broken-3-bad-meta.zip` — expected: **FAIL**
  - Archive descriptor error: `meta.xml` references `occurrence.txt` but the file was renamed
