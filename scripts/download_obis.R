library(robis)
library(dplyr)
library(readr)
library(tidyr)

sf_bay_coast_wkt <- "POLYGON ((-123.6 36.7, -123.6 38.8, -122.0 38.8, -122.0 36.7, -123.6 36.7))"

species <- "Mytilus californianus"
start_date <- "2015-01-01"
end_date   <- "2024-12-31"

occ <- occurrence(
  scientificname = species,
  startdate = start_date,
  enddate   = end_date,
  geometry  = sf_bay_coast_wkt,
  fields    = c("occurrenceID","eventID","eventDate","decimalLatitude","decimalLongitude",
                "scientificName","basisOfRecord","countryCode","datasetID")
)

# sample tiny dataset
set.seed(1)
n_take <- min(200L, nrow(occ))
occ_tiny <- occ %>% dplyr::slice_sample(n = n_take)

# write datasets
dir.create("datasets", showWarnings = FALSE)
dir.create("datasets/raw", showWarnings = FALSE)

readr::write_csv(occ, "datasets/raw/OBIS_SF_Bay_2015-2024_Mytilus_raw.csv")
readr::write_csv(occ_tiny, "datasets/OBIS_SF_Bay_2015-2024_Mytilus_tiny.csv")

# ---- dataset summary (Markdown) ----
dir.create("notes", showWarnings = FALSE)

n_rows <- nrow(occ_tiny)
n_cols <- ncol(occ_tiny)
cols   <- names(occ_tiny)

core_fields <- c("occurrenceID","eventID","eventDate","decimalLatitude","decimalLongitude",
                 "scientificName","basisOfRecord","countryCode","id")

present_fields <- intersect(core_fields, names(occ_tiny))

missing_tbl <- occ_tiny |>
  dplyr::summarise(dplyr::across(
    dplyr::all_of(present_fields),
    ~ sum(is.na(.) | . == "")
  )) |>
  tidyr::pivot_longer(
    cols = dplyr::everything(),
    names_to = "field",
    values_to = "missing"
  )

summary_path <- sprintf(
  "notes/OBIS_SF_Bay_%s_%s_%s_summary.md",
  gsub(" ", "_", species),
  "2015-2024",
  format(Sys.Date(), "%Y-%m-%d")
)

lines <- c(
  "# OBIS DwC demo dataset summary",
  "",
  sprintf("- **Generated:** %s", format(Sys.time(), "%Y-%m-%d %H:%M")),
  "- **Region:** SF Bay Area coast (WKT box)",
  sprintf("- **Species filter:** %s", species),
  sprintf("- **Date range:** %s to %s", start_date, end_date),
  "",
  "## Shape",
  sprintf("- **Rows:** %d", n_rows),
  sprintf("- **Columns:** %d", n_cols),
  "",
  "## Columns",
  paste0("- ", cols),
  "",
  "## Missingness (core fields)",
  "",
  "| field | missing |",
  "|---|---:|",
  paste0("| ", missing_tbl$field, " | ", missing_tbl$missing, " |")
)

writeLines(lines, summary_path)
message("Wrote dataset summary to: ", summary_path)
