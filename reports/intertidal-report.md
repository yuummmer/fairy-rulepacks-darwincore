# FAIRy Validate Report

**Timestamp:** 2025-12-17T23:05:38+00:00
**Rulepack:** intertidal_starter@0.1.0 (rulepacks/intertidal_starter/rulepack.yaml)

## Summary
- PASS: 3
- WARN: 1
- FAIL: 3

## Inputs
- `datasets/intertidal_obis_tiny_seeded.csv` — sha256=ec64334c093b82813866fe319d8bc0845b3218d0103d682d0124325a6d88a490, rows=189, bytes=37448

## Findings for `datasets/intertidal_obis_tiny_seeded.csv`
### [WARN] dwc_basisOfRecord_enum — enum
Out of set rows [24] (count=1)
### [FAIL] dwc_decimalLatitude_range — range
Out of bounds rows [54] (count=1)
### [PASS] dwc_decimalLongitude_range — range
### [PASS] dwc_eventdate_non_empty_trimmed — non_empty_trimmed
### [PASS] dwc_eventdate_present — required
### [FAIL] dwc_occurrenceid_present — required
### [FAIL] dwc_occurrenceid_unique — unique
Duplicates at rows [62]
