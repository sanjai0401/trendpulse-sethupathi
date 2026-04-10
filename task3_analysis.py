import pandas as pd

df = pd.read_csv("cleaned_data.csv")

print(df.describe())
print(df['title'].value_counts().head())
