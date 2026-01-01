# How to read FAIRy reports (Darwin Core starter)

This short guide explains how to interpret FAIRy report results (PASS/WARN/FAIL) and how to act on them.

_Scope note: FAIRy community rulepacks provide practical checks and guidance, but they are not the authoritative source for Darwin Core/GBIF policy. Where domain semantics matter, we link to official documentation._

## What FAIRy is doing
FAIRy runs a set of checks (“rules”) against a dataset and summarizes what passed and what needs attention.

The report is organized into:
- **Summary**: how many checks passed, warned, or failed
- **Inputs**: which file was checked (plus its row count)
- **Findings**: details for each check

## PASS vs WARN vs FAIL
- **PASS**: the check is satisfied. Nothing to do.
- **WARN**: something looks unusual or outside the expected values, but may be acceptable depending on context. Informational and review needed.
- **FAIL**: the data violates the rule. This usually means the dataset needs a fix (or the rule needs to be adjusted). Generally means not submission ready.

## The “Summary” section
Example:

- PASS: 3
- WARN: 1
- FAIL: 3

This means: 3 checks succeeded, 1 raised a warning, and 3 checks found problems that should be addressed.

## The “Findings” section
Each finding has:
- a **severity** in brackets: `[PASS]`, `[WARN]`, or `[FAIL]`
- a **rule id** (example: `dwc_decimalLatitude_range`)
- a **rule type** (example: `range`, `enum`, `required`, `unique`)
- a short message that often includes **row numbers**

### What “rows [54]” means
The report’s row numbers refer to the CSV data rows. Depending on the tool you open the file in (Excel/Google Sheets vs a text editor), row numbers may appear off by 1 because of the header row.

To inspect a row:
1) Open the CSV file listed under **Inputs**
2) Go to the row number mentioned in the finding
3) Look at the relevant column for that rule

## Common rule types in this starter
### `required` (FAIL)
Meaning: a required field is missing.
Example from this report:
- `[FAIL] dwc_occurrenceid_present — required`

What to do:
- Find the referenced row(s) and fill in the missing value in the required column (here: `occurrenceID`).

### `unique` (FAIL)
Meaning: a field that should uniquely identify each record has duplicates (identifier collision).

Example from this report:
- `[FAIL] dwc_occurrenceid_unique — unique`
- “Duplicates at rows [62]”

For duplicates, FAIRy lists the row(s) that repeat a prior value (the first instance is earlier in the file).

What to do:
- Inspect the duplicate value(s) around the referenced row(s).
- FAIRy’s `unique` check flags when the same `occurrenceID` appears more than once in the same file, which usually breaks record identity and downstream joins.

Decide whether:
  - the rows are accidental duplicates and should be removed/merged, or
  - the identifier needs to be corrected so each row has a distinct `occurrenceID`, or
  - you need a different identifier field for uniqueness in your workflow (advanced/custom rulepack).

### Duplicates in biodiversity data (important nuance)
FAIRy’s `unique` checks are about **identifier collisions inside a single file** (e.g., the same `occurrenceID` appearing twice). This usually indicates a data hygiene issue that can break joins and downstream processing.

Biodiversity aggregators (like GBIF) may include multiple valid records that refer to the same underlying organism or sampling context (e.g., a preserved specimen record and a DNA-derived record). These are sometimes called “scientific duplicates” and are not always errors. Tools like GBIF’s clustering can help **estimate** duplication, but you should not automatically remove clustered records without review.

Domain reference:
- GBIF “Duplicates” (data use course): https://docs.gbif.org/course-data-use/en/duplicates.html
- GBIF technical docs on clustering: https://techdocs.gbif.org/en/data-processing/clustering-occurrences

### `range` (FAIL)
Meaning: a numeric value is outside an allowed range.
Example from this report:
- `[FAIL] dwc_decimalLatitude_range — range`
- “Out of bounds rows [54]”

What to do:
- Check `decimalLatitude` in that row.
- Common causes:
  - latitude/longitude swapped
  - wrong sign (positive vs negative)
  - typing/format issue

### `eventDate` format (WARN)
FAIRy may warn if `eventDate` doesn’t look like an ISO date:
- `YYYY-MM-DD`, or
- `YYYY-MM-DD/YYYY-MM-DD` (date interval)

What to do:
- Normalize dates to ISO format where possible.
- If your workflow uses full timestamps, this starter rule may be too strict (use a custom/advanced rulepack).

### Suspicious coordinates (WARN)
FAIRy flags `decimalLatitude` or `decimalLongitude` values of `0` / `0.0` because they’re often used as placeholders when coordinates are unknown. In many datasets, `(0,0)` is a strong sign of missing coordinates.

What to do:
- Verify the coordinates against the source.
- If coordinates are unknown, prefer leaving them blank (workflow-dependent) rather than using `0`.

### `enum` (WARN)
Meaning: the value isn’t in an allowed set (controlled vocabulary).
Example from this report:
- `[WARN] dwc_basisOfRecord_enum — enum`
- “Out of set rows [24]”

What to do:
- Check `basisOfRecord` in that row.
- Either:
  - update the dataset to use the expected value, or
  - update the rule’s allowed list if your organization expects other values.

This starter normalizes case and trims leading/trailing whitespace, so capitalization/extra spaces at the ends won’t trigger a warning.

### `regex` (WARN) — formatting checks (example: `countryCode`)
Meaning: the value doesn’t match an expected format.

Example:
- `[WARN] dwc_countryCode_iso2 — regex`

What to do:
- Check `countryCode` in the referenced row(s).
- In Darwin Core, `countryCode` is typically a **two-letter code** (ISO 3166-1 alpha-2 style), e.g. `US`, `SE`, `FR`.
- Common fixes:
  - `USA` → `US`
  - extra whitespace → trim
  - missing value → fill if your workflow requires it

## Re-run after changes
After editing the CSV, re-run FAIRy using the command in the README. The report will update and you should see FAIL/WARN counts change.

## When to change the data vs change the rulepack
If a rule is obviously right for DwC (e.g. latitude out of range), fix the data
If the rule is too strict for your workflow (timestamps, different controlled vocabulary, etc) adjust or override the rulepack.