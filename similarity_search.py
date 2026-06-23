import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def search_similar_bugs(query):

    df = pd.read_csv("data/bugs.csv")

    bugs = df["bug_description"].tolist()

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(
        bugs + [query]
    )

    similarities = cosine_similarity(
        tfidf_matrix[-1],
        tfidf_matrix[:-1]
    )[0]

    results = []

    for i, score in enumerate(similarities):

        results.append(
            (
                bugs[i],
                round(score * 100, 2)
            )
        )

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return results[:5]