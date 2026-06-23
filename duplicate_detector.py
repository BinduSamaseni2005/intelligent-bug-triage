import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv("data/bugs.csv")

vectorizer = TfidfVectorizer()

vectors = vectorizer.fit_transform(data["bug_description"])

def find_duplicate(new_bug):

    new_vector = vectorizer.transform([new_bug])

    similarity = cosine_similarity(new_vector, vectors)

    max_score = similarity.max()

    if max_score > 0.5:
        index = similarity.argmax()
        return True, data.iloc[index]["bug_description"]

    return False, None