# clean_firefox.py

import pandas as pd

df = pd.read_csv("gitbugs/firefox/Firefox_bugs.csv")

df = df[["Summary", "Description", "Priority"]]

df = df[df["Priority"] != "--"]

df["bug_description"] = (
    df["Summary"].fillna("") +
    " " +
    df["Description"].fillna("")
)

df = df[["bug_description", "Priority"]]

df.dropna(inplace=True)

print(df.head())

print("Records:", len(df))

df.to_csv(
    "data/firefox_priority_dataset.csv",
    index=False
)

print("Saved successfully")