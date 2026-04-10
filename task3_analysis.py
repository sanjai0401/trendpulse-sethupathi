import pandas as pd
import os
import glob
import numpy as np

# Step 1: Find latest CSV file
csv_files = glob.glob("data/trends_*.csv")

if not csv_files:
    print("No CSV file found in data/ folder.")
    exit()

latest_file = max(csv_files, key=os.path.getctime)
print(f"Analyzing file: {latest_file}")

# Step 2: Load CSV
df = pd.read_csv(latest_file)

print(f"Total records: {len(df)}")

# -----------------------------
# ANALYSIS SECTION
# -----------------------------

# 1. Top category by number of posts
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()

print("\nTop Category:")
print(category_counts)

# 2. Average score per category
avg_score = df.groupby("category")["score"].mean().sort_values(ascending=False)

print("\nAverage Score per Category:")
print(avg_score)

# 3. Most commented posts (Top 5)
top_commented = df.sort_values(by="num_comments", ascending=False).head(5)

print("\nTop 5 Most Commented Posts:")
print(top_commented[["title", "num_comments", "category"]])

# 4. Highest scoring posts (Top 5)
top_scored = df.sort_values(by="score", ascending=False).head(5)

print("\nTop 5 Highest Scoring Posts:")
print(top_scored[["title", "score", "category"]])

# 5. Correlation between score and comments
correlation = df["score"].corr(df["num_comments"])

print("\nCorrelation between Score and Comments:")
print(correlation)

# 6. NumPy Example (extra marks)
scores_array = np.array(df["score"])
print("\nNumPy Stats on Scores:")
print(f"Mean: {np.mean(scores_array)}")
print(f"Median: {np.median(scores_array)}")
print(f"Max: {np.max(scores_array)}")

# -----------------------------
# SAVE SUMMARY (IMPORTANT)
# -----------------------------

summary = {
    "total_posts": len(df),
    "top_category": top_category,
    "avg_score_per_category": avg_score.to_dict(),
    "correlation_score_comments": float(correlation)
}

summary_file = latest_file.replace(".csv", "_summary.json")

import json
with open(summary_file, "w") as f:
    json.dump(summary, f, indent=4)

print(f"\nAnalysis summary saved to: {summary_file}")
