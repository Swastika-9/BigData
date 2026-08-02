import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/processed")

files = [
    "stops.csv",
    "operators.csv",
    "services.csv",
    "routes.csv",
    "route_links.csv",
    "journey_pattern_links.csv",
    "vehicle_journeys.csv"
]

for file in files:
    path = DATA_DIR / file

    if path.exists():
        df = pd.read_csv(path)

        print("---------------------------")
        print(file)
        print("Rows:", len(df))
        print("Columns:", list(df.columns))
        print(df.head(3))
    else:
        print(file, "NOT FOUND")