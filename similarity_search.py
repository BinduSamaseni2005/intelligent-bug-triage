import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("data/firefox_priority_dataset.csv")

texts = df["bug_description"].fillna("").astype(str)

vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(texts)

def search_similar_bugs(query):

    query_vec = vectorizer.transform([query])

    similarity = cosine_similarity(
        query_vec,
        tfidf_matrix
    )[0]

    df["score"] = similarity

    results = df.sort_values(
        "score",
        ascending=False
    ).head(5)

    return list(zip(
        results["bug_description"],
        (results["score"] * 100).round(2)
    ))