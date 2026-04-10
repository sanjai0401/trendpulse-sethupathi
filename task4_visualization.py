import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("cleaned_data.csv")

df['title'].value_counts().head().plot(kind='bar')
plt.title("Top Titles")
plt.show()
