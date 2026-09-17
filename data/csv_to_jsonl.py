"""
Convert the local JBB-Behaviors CSVs (already downloaded into data/) into
JSONL files with only the columns this project needs.

Original columns: Index, Goal, Target, Behavior, Category, Source.
We keep Behavior (-> id), Goal (-> goal), Category (-> category).
"""

import json
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent
WANTED = ["Behavior", "Goal", "Category"]
RENAME = {"Behavior": "id", "Goal": "goal", "Category": "category"}

FILES = {
    "harmful-behaviors.csv": DATA_DIR / "jbb_behaviors.jsonl",
    "benign-behaviors.csv": DATA_DIR / "jbb_behaviors_benign.jsonl",
}

for csv_name, out_path in FILES.items():
    df = pd.read_csv(DATA_DIR / csv_name)
    df = df[WANTED].rename(columns=RENAME)

    with out_path.open("w") as f:
        for _, row in df.iterrows():
            f.write(json.dumps(row.to_dict()) + "\n")

    print(f"Wrote {len(df)} rows to {out_path}")