# FAIRy Darwin Core starter (community)

This repo contains a community-maintained Darwin Core “starter” rulepack for FAIRy plus a tiny demo fixture dataset.

## What’s included

- `rulepacks/dwc_starter/` — starter rulepack with a small set of high-signal checks
- `datasets/fixtures/` — small demo datasets (fixtures) used for examples/tests
- `scripts/` — reproducible scripts to download/profile the OBIS source data
- `docs/` — documentation, including how to read FAIRy reports

Start here:
- `docs/overview.md`
- `docs/how-to-read-fairy-reports.md`
- `docs/examples/obis-occurrence.md`

## Quickstart

Run FAIRy against the demo fixture:

```bash
fairy validate \
  --rulepack rulepacks/dwc_starter/rulepack.yaml \
  --inputs default=datasets/fixtures/obis_sf_bay_mytilus_tiny_seeded.csv \
  --report-json /tmp/dwc_starter_report.json \
  --report-md /tmp/dwc_starter_report.md

```
## Outputs
After running, you should have:
- `/tmp/dwc_starter_report`.json - machine-readable report
- `/tmp/dwc_starter_report` - human-readable summary

## How to interpret results

See: `docs/how-to-read-fairy-reports.md`

## Repo layout
- `rulepacks/dwc_starter/` — the rulepack used for this demo
- `datasets/fixtures` — small demo datasets committed to this repo
- `datasets/raw/` — local-only raw pulls (intentionally not committed)
- `docs/` - docs and examples
- `scripts/` - reproducible scripts to download/profile OBIS source data