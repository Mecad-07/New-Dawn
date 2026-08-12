import pandas as pd
import os

DATA_DIR = r"A:\Military\data"

file_1970_2020 = os.path.join(
    DATA_DIR,
    "globalterrorism_1970_2020.xlsx"
)

file_2021 = os.path.join(
    DATA_DIR,
    "globalterrorism_2021.xlsx"
)

output_file = os.path.join(
    DATA_DIR,
    "globalterrorism_master.csv"
)


print("=" * 70)
print("GTD MASTER DATASET CREATION")
print("=" * 70)

# --------------------------------------------------
# Load GTD 1970-2020
# --------------------------------------------------

print("\nLoading GTD 1970-2020...")

df_1970_2020 = pd.read_excel(
    file_1970_2020,
    engine="openpyxl"
)

print("Rows:", len(df_1970_2020))
print("Columns:", len(df_1970_2020.columns))


# --------------------------------------------------
# Load GTD 2021
# --------------------------------------------------

print("\nLoading GTD 2021...")

df_2021 = pd.read_excel(
    file_2021,
    engine="openpyxl"
)

print("Rows:", len(df_2021))
print("Columns:", len(df_2021.columns))


# --------------------------------------------------
# Check column compatibility
# --------------------------------------------------

print("\nChecking columns...")

if list(df_1970_2020.columns) != list(df_2021.columns):
    print("ERROR: Column structures do not match.")

    columns_1 = set(df_1970_2020.columns)
    columns_2 = set(df_2021.columns)

    print("\nOnly in 1970-2020:")
    print(columns_1 - columns_2)

    print("\nOnly in 2021:")
    print(columns_2 - columns_1)

    raise SystemExit


print("Column structures match: OK")


# --------------------------------------------------
# Combine datasets
# --------------------------------------------------

print("\nCombining datasets...")

df = pd.concat(
    [df_1970_2020, df_2021],
    ignore_index=True
)

print("Combined rows:", len(df))
print("Combined columns:", len(df.columns))


# --------------------------------------------------
# Event ID validation
# --------------------------------------------------

print("\nChecking Event IDs...")

df["eventid"] = df["eventid"].astype("string")

duplicate_ids = df["eventid"].duplicated().sum()

print("Unique Event IDs:", df["eventid"].nunique())
print("Duplicate Event IDs:", duplicate_ids)

if duplicate_ids > 0:
    raise ValueError(
        "Duplicate Event IDs found. Master dataset was not created."
    )


# --------------------------------------------------
# Year validation
# --------------------------------------------------

print("\nChecking year range...")

print("Minimum year:", df["iyear"].min())
print("Maximum year:", df["iyear"].max())


# --------------------------------------------------
# 2021 validation
# --------------------------------------------------

rows_2021 = (df["iyear"] == 2021).sum()

print("2021 records:", rows_2021)

if rows_2021 == 0:
    raise ValueError("No 2021 records found.")


# --------------------------------------------------
# Sort chronologically
# --------------------------------------------------

print("\nSorting dataset...")

df = df.sort_values(
    by=["iyear", "imonth", "iday", "eventid"],
    na_position="last"
).reset_index(drop=True)


# --------------------------------------------------
# Save master CSV
# --------------------------------------------------

print("\nSaving master dataset...")

df.to_csv(
    output_file,
    index=False,
    encoding="utf-8"
)


# --------------------------------------------------
# Final validation
# --------------------------------------------------

print("\n" + "=" * 70)
print("MASTER DATASET CREATED SUCCESSFULLY")
print("=" * 70)

print("Output:")
print(output_file)

print("\nRows:", len(df))
print("Columns:", len(df.columns))
print("Year range:", df["iyear"].min(), "to", df["iyear"].max())
print("Unique Event IDs:", df["eventid"].nunique())
print("Duplicate Event IDs:", df["eventid"].duplicated().sum())

print("\nDataset creation complete.")