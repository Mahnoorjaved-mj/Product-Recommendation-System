def recommend_products(df, top_n=8):
    """
    Simple recommendation based on highest rating
    Works with Amazon CSV (no user_id required)
    """

    # required columns check
    required_cols = {"name", "sub_category", "price", "rating"}
    if not required_cols.issubset(df.columns):
        return []

    # rating numeric
    df["rating"] = df["rating"].astype(float)

    # top rated products
    top_products = (
        df.sort_values("rating", ascending=False)
          .head(top_n)
    )

    results = []
    for _, row in top_products.iterrows():
        results.append({
            "name": row["name"],
            "category": row["sub_category"],
            "price": row["price"],
            "rating": row["rating"]
        })

    return results
