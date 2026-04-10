import pandas as pd
import os
import glob

# Step 1: Find latest JSON file from data folder
data_files = glob.glob("data/trends_*.json")

if not data_files:
    print("No JSON file found in data/ folder.")
    exit()

latest_file = max(data_files, key=os.path.getctime)
print(f"Processing file: {latest_file}")

# Step 2: Load JSON into DataFrame
df = pd.read_json(latest_file)

print(f"Initial records: {len(df)}")

# Step 3: Data Cleaning

# Remove duplicates based on post_id
df = df.drop_duplicates(subset="post_id")

# Remove rows with missing important fields
df = df.dropna(subset=["title", "category", "author"])

# Ensure numeric columns are correct
df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0).astype(int)
df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce").fillna(0).astype(int)

# Standardize text (optional improvement)
df["title"] = df["title"].str.strip()
df["author"] = df["author"].str.strip()

# Remove empty titles after cleaning
df = df[df["title"] != ""]

print(f"Cleaned records: {len(df)}")

# Step 4: Save as CSV

# Create output filename
csv_file = latest_file.replace(".json", ".csv")

df.to_csv(csv_file, index=False)

print(f"Cleaned data saved to: {csv_file}")
