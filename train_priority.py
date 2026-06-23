import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib

data = pd.read_csv("data/bugs.csv")

X = data["bug_description"]
y = data["priority"]

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", RandomForestClassifier())
])

model.fit(X, y)

joblib.dump(model, "models/priority_model.pkl")

print("Priority model trained successfully")