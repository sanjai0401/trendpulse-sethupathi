import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os

# Step 1: Find latest CSV
csv_files = glob.glob("data/trends_*.csv")

if not csv_files:
    print("No CSV file found in data/ folder.")
    exit()

latest_file = max(csv_files, key=os.path.getctime)
print(f"Visualizing file: {latest_file}")

# Step 2: Load data
df = pd.read_csv(latest_file)

# Create output folder
output_folder = "visuals"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# -----------------------------
# 1. Category Distribution
# -----------------------------
plt.figure()
df["category"].value_counts().plot(kind='bar')
plt.title("Number of Posts per Category")
plt.xlabel("Category")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(f"{output_folder}/category_distribution.png")
plt.close()

# -----------------------------
# 2. Average Score per Category
# -----------------------------
plt.figure()
df.groupby("category")["score"].mean().plot(kind='bar')
plt.title("Average Score per Category")
plt.xlabel("Category")
plt.ylabel("Average Score")
plt.tight_layout()
plt.savefig(f"{output_folder}/avg_score_category.png")
plt.close()

# -----------------------------
# 3. Score vs Comments (Scatter)
# -----------------------------
plt.figure()
plt.scatter(df["score"], df["num_comments"])
plt.title("Score vs Comments")
plt.xlabel("Score")
plt.ylabel("Comments")
plt.tight_layout()
plt.savefig(f"{output_folder}/score_vs_comments.png")
plt.close()

# -----------------------------
# 4. Top 10 Posts by Score
# -----------------------------
top_posts = df.sort_values(by="score", ascending=False).head(10)

plt.figure()
plt.barh(top_posts["title"], top_posts["score"])
plt.title("Top 10 Posts by Score")
plt.xlabel("Score")
plt.ylabel("Title")
plt.tight_layout()
plt.savefig(f"{output_folder}/top_posts.png")
plt.close()

print("Visualizations saved in 'visuals/' folder")
