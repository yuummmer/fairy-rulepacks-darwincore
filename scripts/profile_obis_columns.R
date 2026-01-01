library(readr)
library(dplyr)

x <- read_csv("data/intertidal_obis_tiny.csv", show_col_types = FALSE)
glimpse(x)

x %>%
  summarise(
    n = n(),
    missing_occurrenceID = sum(is.na(occurrenceID) | occurrenceID == ""),
    missing_eventDate = sum(is.na(eventDate) | eventDate == ""),
    missing_lat = sum(is.na(decimalLatitude)),
    missing_lon = sum(is.na(decimalLongitude))
  )
