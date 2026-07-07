import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

df = pd.read_csv("data/firefox_priority_dataset.csv")

X = df["bug_description"]
y = df["Priority"]

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            stop_words="english",
            max_features=10000
        )
    ),
    (
        "classifier",
        LinearSVC(
            class_weight="balanced"
        )
    )
])

model.fit(X, y)

joblib.dump(
    model,
    "models/priority_model.pkl"
)

print("SVM model saved successfully")