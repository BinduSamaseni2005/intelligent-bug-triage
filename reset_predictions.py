import pandas as pd

pd.DataFrame(
    columns=[
        "bug_description",
        "developer",
        "priority",
        "confidence"
    ]
).to_csv("data/predictions.csv", index=False)

print("created")