import pandas as pd
import os

DATA_DIR = r"A:\Military\data"

files = [
    "globalterrorism_1970_2020.xlsx",
    "globalterrorism_2021.xlsx"
]

for filename in files:
    path = os.path.join(DATA_DIR, filename)

    print("\n" + "=" * 70)
    print(filename)
    print("=" * 70)

    try:
        df = pd.read_excel(path)

        print("Rows:", len(df))
        print("Columns:", len(df.columns))

        print("\nYear range:")
        if "iyear" in df.columns:
            print(df["iyear"].min(), "to", df["iyear"].max())
        else:
            print("iyear column NOT FOUND")

        print("\nEvent ID:")
        if "eventid" in df.columns:
            print("Unique IDs:", df["eventid"].nunique())
            print("Duplicate IDs:", df["eventid"].duplicated().sum())
        else:
            print("eventid column NOT FOUND")

        print("\nFirst 15 columns:")
        print(list(df.columns[:15]))

        print("\nLast 10 columns:")
        print(list(df.columns[-10:]))

    except Exception as e:
        print("ERROR:", e)