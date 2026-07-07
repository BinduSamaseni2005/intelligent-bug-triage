import pandas as pd

df = pd.read_csv("gitbugs/firefox/Firefox_bugs.csv")

print(df["Priority"].value_counts())