import pandas as pd

df = pd.read_csv(
    "gitbugs/ms_vscode_bugs/vscode_bugs.csv"
)

df = df[["Summary", "Description"]]

df["bug_description"] = (
    df["Summary"].fillna("")
    + " "
    + df["Description"].fillna("")
)

df = df[["bug_description"]]

print(df.head())

df.to_csv(
    "data/real_bugs.csv",
    index=False
)

print("Saved:", len(df))