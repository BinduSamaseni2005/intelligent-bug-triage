import pandas as pd

df = pd.read_csv("data/bugs.csv")

mapping = {
    "Authentication": "Developer_A",
    "Security": "Developer_A",

    "Payments": "Developer_B",
    "Billing": "Developer_B",

    "Dashboard": "Developer_C",
    "Notifications": "Developer_C",
    "User Profile": "Developer_C",
    "UI": "Developer_C",

    "API": "Developer_D",
    "Database": "Developer_D",

    "Inventory": "Developer_E",
    "Orders": "Developer_E",
    "Reports": "Developer_E",
    "Search": "Developer_E",
    "Analytics": "Developer_E",
    "Messaging": "Developer_E"
}

for i in range(len(df)):
    module = df.loc[i, "module"]

    if module in mapping:
        df.loc[i, "developer"] = mapping[module]

df.to_csv("data/bugs.csv", index=False)

print("Dataset fixed successfully!")