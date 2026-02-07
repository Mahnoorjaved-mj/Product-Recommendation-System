import pandas as pd
import os
import re

def clean_price(x):
    if pd.isna(x):
        return 0
    x = str(x)
    x = re.sub(r"[^\d.]", "", x)
    return float(x) if x else 0

def load_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(base_dir, "data", "amazon.csv")

    df = pd.read_csv(csv_path)

    # normalize columns
    if "asin" in df.columns:
        df["productId"] = df["asin"]

    if "overall" in df.columns:
        df["rating"] = df["overall"]

    # clean numeric columns (safe)
    for col in ["discounted_price","actual_price",
                "discount_percentage","rating","rating_count"]:
        if col in df.columns:
            df[col] = df[col].apply(clean_price)

    return df
