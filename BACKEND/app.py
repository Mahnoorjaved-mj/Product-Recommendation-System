from flask import Flask, render_template, jsonify, request
from services.data_loader import load_data

app = Flask(__name__, template_folder="templates", static_folder="static")

# ======================
# LOAD CSV DATA
# ======================
df = load_data()

# ======================
# AMAZON CSV NORMALIZATION
# ======================
if "asin" in df.columns:
    df["productId"] = df["asin"]

if "overall" in df.columns:
    df["rating"] = df["overall"]

# ======================
# PAGE ROUTES (SINGLE PAGE)
# ======================
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/recommendations")
def recommendations_page():
    # same HTML (SPA navigation)
    return render_template("dashboard.html")

# ======================
# DASHBOARD API (PHASE-1)
# ======================
@app.route("/api/dashboard")
def dashboard_data():
    return jsonify({
        "active_recs": int(len(df)),
        "conversion_rate": round(df["discount_percentage"].mean(), 2),
        "model_accuracy": round(df["rating"].mean(), 2),
        "revenue_impact": round(df["discounted_price"].sum(), 2),

        # TOP PRODUCTS (CSV)
        "top_products": df.head(6)[
            ["product_name", "category", "discounted_price", "rating", "product_link"]
        ].to_dict(orient="records")
    })

# ======================
# PERFORMANCE CHART API
# ======================
@app.route("/api/chart/performance")
def performance_chart():
    return jsonify({
        "labels": ["Discount Impact", "User Trust"],
        "ctr": [
            round(df["discount_percentage"].mean(), 2),
            round(df["discount_percentage"].mean() * 0.6, 2)
        ],
        "conversion": [
            round(df["rating"].mean(), 2),
            round(df["rating"].mean() * 0.8, 2)
        ]
    })

# ======================
# ALGORITHM DISTRIBUTION
# ======================
@app.route("/api/chart/algorithm")
def algorithm_chart():
    total = len(df)
    return jsonify({
        "labels": ["Collaborative", "Content-based", "Hybrid", "Popularity"],
        "values": [
            int(total * 0.35),
            int(total * 0.25),
            int(total * 0.20),
            int(total * 0.20)
        ]
    })

# ======================
# CATEGORY PERFORMANCE CHART
# ======================
@app.route("/api/chart/categories")
def category_chart():
    cat = (
        df.groupby("category")["discount_percentage"]
        .mean()
        .sort_values(ascending=False)
        .head(6)
    )

    return jsonify({
        "labels": list(cat.index),
        "values": [round(v, 2) for v in cat.values]
    })

# ======================
# RECOMMENDATION RULES TABLE (PHASE-1)
# ======================
@app.route("/api/recommendation-rules")
def recommendation_rules():
    rules = [
        {
            "name": "Frequently Bought Together",
            "algorithm": "Collaborative",
            "status": "Active",
            "priority": "High",
            "ctr": f"{round(df['discount_percentage'].mean(),2)}%",
            "conversions": int(len(df) * 0.15),
            "updated": "2 days ago"
        },
        {
            "name": "Similar Products",
            "algorithm": "Content-Based",
            "status": "Active",
            "priority": "Medium",
            "ctr": f"{round(df['rating'].mean(),2)}%",
            "conversions": int(len(df) * 0.10),
            "updated": "1 week ago"
        },
        {
            "name": "Trending Now",
            "algorithm": "Hybrid",
            "status": "Active",
            "priority": "High",
            "ctr": f"{round(df['rating'].mean()*1.1,2)}%",
            "conversions": int(len(df) * 0.18),
            "updated": "3 days ago"
        }
    ]
    return jsonify(rules)

# ======================
# BASIC RECOMMENDATIONS API
# ======================
@app.route("/api/recommendations")
def recommendations_api():
    algo = request.args.get("algo", "collaborative")

    if algo == "content":
        data = df.sort_values("rating", ascending=False).head(10)

    elif algo == "hybrid":
        data = df.sample(10)

    else:  # collaborative
        data = (
            df.groupby("productId", as_index=False)["rating"]
            .mean()
            .sort_values("rating", ascending=False)
            .head(10)
        )

    return jsonify(
        data[["productId", "rating"]].to_dict(orient="records")
    )
@app.route("/api/algorithm-cards")
def algorithm_cards():
    total = len(df)

    return jsonify({
        "collaborative": {
            "daily_recs": int(total * 0.35),
            "ctr": round(df["rating"].mean(), 2),
            "conversion": round(df["rating"].mean() * 0.5, 2)
        },
        "content": {
            "daily_recs": int(total * 0.25),
            "ctr": round(df["discount_percentage"].mean(), 2),
            "conversion": round(df["discount_percentage"].mean() * 0.3, 2)
        },
        "hybrid": {
            "daily_recs": int(total * 0.40),
            "ctr": round(df["rating"].mean() * 1.1, 2),
            "conversion": round(df["rating"].mean() * 0.6, 2)
        }
    })
@app.route("/api/products/stats")
def product_stats():
    total_products = len(df)

    total_categories = (
        df["category"].nunique()
        if "category" in df.columns else 0
    )

    avg_rating = (
        round(df["rating"].mean(), 2)
        if "rating" in df.columns else 0
    )

    return jsonify({
        "total_products": int(total_products),
        "total_categories": int(total_categories),
        "avg_rating": avg_rating
    })
# ======================
# RUN APP
# ======================
if __name__ == "__main__":
    app.run(debug=True)
