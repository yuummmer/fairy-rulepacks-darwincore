# FAIRy Intertidal (Darwin Core–style) Starter

## What is this?
- **FAIRy**: the tool that checks a dataset and produces a report (pass/warn/fail).
- **FAIRy-core**: the underlying engine/codebase that FAIRy runs on.
- This repo: a small example “bundle” (sample data + rules + example reports).

## Darwin Core–style
The checks in this starter target common Darwin Core occurrence fields:
`occurrenceID`, `eventDate`, `decimalLatitude`, `decimalLongitude`, `basisOfRecord`.
This is a small practical subset (not a full Darwin Core validator) meant to catch common issues early.

## Start here (no install required)
If you just want to see what FAIRy outputs look like, you do **not** need to install anything.

1) Click `reports/`
2) Open:
   - `intertidal-report.md` (human-readable summary)
   - `intertidal.json` (machine-readable report)

**Two questions (feedback welcome):**
1) Is the report clear / what’s confusing?
2) What are the top 3–5 checks you’d want in a first version?

This repo is a tiny, runnable example of using FAIRy to validate a Darwin Core–ish **occurrence** table (tested on an OBIS “tiny” CSV).

## Optional: run it yourself (one command)
From the repo root:

```bash
fairy validate \
  --rulepack rulepacks/intertidal_starter/rulepack.yaml \
  --inputs occurrences=datasets/intertidal_obis_tiny_seeded.csv \
  --report-json reports/intertidal.json \
  --report-md reports/intertidal-report.md

```
## Outputs
After running, you should have:
- reports/intertidal.json - machine-readable report
- reports/intertidal.md - human-readable summary

## How to interpret results

See: `docs/how-to-read-fairy-reports.md`

## Repo layout
- rulepacks/intertidal_starter/ — the rulepack used for this demo
- datasets/ — demo datasets (including intertidal_obis_tiny_seeded.csv)
- reports/ — saved example outputs (json + md)