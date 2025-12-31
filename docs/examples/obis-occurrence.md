# Example: OBIS occurrence demo (SF Bay Area, Mytilus)

This example uses a tiny occurrence-style dataset derived from OBIS to demonstrate the `dwc_starter` rulepack and how FAIRy reports issues.

## Files

- Fixture dataset: `datasets/fixtures/obis_sf_bay_mytilus_tiny_seeded.csv`
- Rulepack: `rulepacks/dwc_starter/rulepack.yaml`
- Scripts:
  - `scripts/download_obis.R`
  - `scripts/profile_obis_columns.R`

> Note: `datasets/raw/` is intentionally not committed. Use the script to re-download if needed.

## Run FAIRy

```bash
fairy validate \
  --rulepack rulepacks/dwc_starter/rulepack.yaml \
  --inputs default=datasets/fixtures/obis_sf_bay_mytilus_tiny_seeded.csv \
  --report-md /tmp/dwc_starter_report.md \
  --report-json /tmp/dwc_starter_report.json
  ```

## What to look for in the report
- FAIL/WARN summary
- Identifier checks (`occrrenceID`)
- Date validity (`eventDate`)
- Coordinate validity (`decimalLatitude`, `decimalLongitude`)