# How to read FAIRy reports (Darwin Core starter)

This short guide explains how to interpret FAIRy report results (PASS/WARN/FAIL) and how to act on them.

## What FAIRy is doing
FAIRy runs a set of checks (“rules”) against a dataset and summarizes what passed and what needs attention.

The report is organized into:
- **Summary**: how many checks passed, warned, or failed
- **Inputs**: which file was checked (plus its row count)
- **Findings**: details for each check

## PASS vs WARN vs FAIL
- **PASS**: the check is satisfied. Nothing to do.
- **WARN**: something looks unusual or outside the expected values, but may be acceptable depending on context.
- **FAIL**: the data violates the rule. This usually means the dataset needs a fix (or the rule needs to be adjusted).

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
- Important nuance: "duplicate records" in biodiversity data can be valid (e.g. a preserved specimen record and a DNA-derived record about the same organism). FAIRy's `unique` check is narrower: it flags when the same `occurrenceID` appears more than once in the same file, which usually breaks record identity and downstream joins.
- Decide whether:
  - the rows are accidental duplicates and should be removed/merged, or
  - the identifier needs to be corrected so each row has a distinct `occurrenceID`, or
  - you need a different identifier field for uniqueness in your workflow (advanced/custom rulepack).

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

## Re-run after changes
After editing the CSV, re-run FAIRy using the command in the README. The report will update and you should see FAIL/WARN counts change.
