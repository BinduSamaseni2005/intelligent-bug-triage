import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
data = pd.read_csv("data/bugs.csv")

# Combine useful text features
X = (
    data["module"].astype(str) + " " +
    data["bug_type"].astype(str) + " " +
    data["bug_description"].astype(str)
)

# Target column
y = data["developer"]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ML Pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=5000
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=2000,
            random_state=42
        )
    )
])

# Train
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, predictions)

print("\n==============================")
print(f"Developer Assignment Accuracy: {accuracy * 100:.2f}%")
print("==============================\n")

print(classification_report(y_test, predictions))

# Save model
joblib.dump(model, "models/developer_model.pkl")

print("✅ Model saved as models/developer_model.pkl")