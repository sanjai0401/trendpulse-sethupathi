import pandas as pd

df = pd.read_json("data.json")
df = df.dropna()
df = df.drop_duplicates()

df.to_csv("cleaned_data.csv", index=False)
