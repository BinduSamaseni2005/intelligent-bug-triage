import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("data/firefox_priority_dataset.csv")

X = df["bug_description"]
y = df["Priority"]

model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english")),
    ("clf", LogisticRegression(max_iter=1000))
])

model.fit(X, y)

joblib.dump(
    model,
    "models/priority_model.pkl"
)

print("Real Priority Model Trained Successfully")