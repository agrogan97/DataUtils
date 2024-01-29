# DataUtils

A collection of utility files for working with the games data. See contents for file descriptions.

Contents:
---
- parseQS24.ipynb : Structure the raw data from JSON into CSV, in the format expected by RISE for Snowflake

File Structure:
---

```
DataUtils
|   Utils
|   |   DataHandler.py: [In progress] data handling library
|   pointer
|   |   pilot2024
|   |   |   parse.ipynb: Handle and structure data from pointer pilot
|   |   |   README.md
|   roomworld
|   |   oxford-studes
|   |   |   parseY2.ipynb: Handle and structure data from the roomworld Dec/Jan 24 pilot
|   |   rise
|   |   |   year3
|   |   |   year4
|   |   |   rawDataHandler.ipynb: Takes raw data from the server and creates sequence-level datasets
|   |   README.md
|   README.md
```