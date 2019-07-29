# API for Data Extractor

## Requirements

- Request (schedule) a data extraction job
- Check a job's status (not processed | processing | completed)

## Implementation

- The bounded buffer problem (race condition; deadlock prevention)
  - Go channel?