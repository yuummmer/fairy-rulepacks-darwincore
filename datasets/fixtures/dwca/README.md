# DwC-A fixtures

This folder contains small Darwin Core Archive (DwC-A) ZIP fixtures used to test:
- archive-level checks (meta.xml present/parseable, core file referenced exists)
- downstream core-table checks (occurrence/event core content)

Fixtures here are intentionally small and curated to produce predictable PASS/FAIL outcomes.

`ipt_occurence_proofpack_v1.0.zip` - Occurrence-core DwC-A proof-pack fixture (expected: PASS structure; core checks vary depending on included "good/broken" cases)