import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("data/firefox_priority_dataset.csv")
bugs = df["bug_description"].fillna("").astype(str)


vectorizer = TfidfVectorizer(stop_words="english")

tfidf_matrix = vectorizer.fit_transform(df["bug_description"])
tfidf_matrix = vectorizer.fit_transform(bugs)

def find_duplicate(query):

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(
        query_vector,
        tfidf_matrix
    ).flatten()

    max_score = similarities.max()
    index = similarities.argmax()

    if max_score > 0.75:
        return True, df.iloc[index]["bug_description"]

    return False, None
