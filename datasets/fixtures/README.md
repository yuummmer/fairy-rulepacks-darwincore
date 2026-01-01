# Fixture datasets

This directory contains small demo datasets used for examples/tests.

## OBIS SF Bay Area occurrence fixture

- File: `obis_sf_bay_mytilus_tiny_seeded.csv`
- Source: OBIS occurrence query (see `scripts/download_obis.R`)

## Notes: 
This fixture is a reduced subset and may include intentionally seeded issues to demonstrate FAIL/WARN output.
- Seeded demo issue: One row has `basisOfRecord = "Preserved Specimen"` (with a space) to intentionally trigger a WARN for enum validation.

## License
Follow the original source dataset license and attribution requirements.
