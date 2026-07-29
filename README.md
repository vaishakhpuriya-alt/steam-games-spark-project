# Steam Games Dataset – Apache Spark Data Engineering Project

## Dataset Description
This project uses the **Steam Games Dataset** from Kaggle, containing metadata for thousands of games on the Steam platform including pricing, review counts, developers, publishers, genres, and playtime statistics.

**Source:** https://www.kaggle.com/datasets/fronkongames/steam-games-dataset

## Objective
Practice core data engineering skills using Apache Spark on Databricks: reading data with appropriate modes, schema validation, data quality checks, transformations, null handling, and writing processed output in Parquet format.

## Steps Performed

### 1–2. Dataset Acquisition & Upload
Downloaded the dataset from Kaggle and uploaded it to a Databricks Unity Catalog Volume at `/Volumes/workspace/default/data/games.csv` (DBFS root upload was disabled on this workspace, so Volumes was used instead).

### 3. Reading Data
Data was first read with `inferSchema=True` and `mode="PERMISSIVE"` to explore the raw structure without crashing on malformed rows.

### 4. Data Exploration
Printed column names, total row count, schema, and column count to understand the dataset shape.

### 5. Corrupted Record Detection
Added `columnNameOfCorruptRecord="_corrupt_record"` to capture malformed rows. See `screenshots/03_corrupt_record_check.png` for results.

### 6. Schema Validation and Creation
The inferred schema mapped several numeric columns (e.g. `Metacritic score`, `Positive`, `Negative`) as strings and `About the game` as an integer, which was incorrect. A custom schema was defined using `StructType` and `StructField` to enforce correct types, then the data was reread with this schema.

### 7. Transformations
Applied the following transformation types:
- **Alias** – renamed columns during selection (e.g. `Name` → `game_name`)
- **Filter** – kept only games with `price_usd > 0`
- **Literal** – added a constant `data_source` column
- **New column** – calculated `total_reviews` from positive + negative reviews
- **Rename** – `price_usd` → `price_in_usd`
- **Cast** – converted `price_in_usd` and `metacritic_score` to correct types
- **Drop** – removed the temporary `data_source` column after use

### 8. Null Value Handling
Identified null counts per column, then:
- Filled `metacritic_score` nulls with `0` (no score ≠ bad game, just unrated)
- Dropped rows missing `game_name` or `price_in_usd` since they're unusable for analysis

### 9. Duplicate Removal
Removed duplicate rows based on `game_name` and `developers`.

### 10. Write Processed Data
Final DataFrame written as Parquet with `mode="overwrite"` to `/Volumes/workspace/default/data/steam_games_processed`.

## Screenshots
| File | Description |
|---|---|
| `01_inferred_schema.png` | Initial inferred schema showing incorrect types |
| `02_custom_schema.png` | Corrected schema after applying StructType |
| `03_corrupt_record_check.png` | Corrupted record detection results |
| `04_row_column_counts.png` | Row count, column count, and schema output |
| `05_transformations_output.png` | Sample output after transformations |
| `06_null_counts.png` | Null value counts per column |
| `07_final_parquet_write.png` | Successful Parquet write confirmation |

## Challenges Faced
- **DBFS root disabled:** Initial upload attempts to `/FileStore/tables/` failed with a `DBFS_DISABLED` error since this workspace enforces Unity Catalog. Resolved by uploading to a Unity Catalog Volume instead (`/Volumes/workspace/default/data/`).
- **Corrupt record column not populating:** `columnNameOfCorruptRecord` only works reliably with an explicit schema — using it alongside `inferSchema=True` silently failed to populate the column. Resolved by defining the custom schema first, then applying corrupt-record tracking on the second read.

## Tech Stack
- Apache Spark (PySpark) on Databricks
- Unity Catalog Volumes for storage
- Parquet as output format
