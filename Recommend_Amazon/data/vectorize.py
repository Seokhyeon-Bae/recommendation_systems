import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

# make sure download this at least once
nltk.download('punkt')
nltk.download('stopwords')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Load data
df = pd.read_csv("/Recommend_Amazon/File/amazon_indexed.csv")

# Output File
output_path = "/Recommend_Amazon/File/amazon_with_vectors.csv"

# fill null values in review content and about product
review = df["review_content"].fillna('')
about = df["about_product"].fillna('')

# Preprocess each document
def preprocess(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words("english"))
    tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
    return " ".join(tokens)

preprocessed_review = review.apply(preprocess)
preprocessed_about = about.apply(preprocess)

# TF-IDF vectorization
vectorizer = TfidfVectorizer(max_features=256)  # higher feature space before SVD
X = vectorizer.fit_transform(preprocessed_review)
Y = vectorizer.fit_transform(preprocessed_about)

# it is a sparse matrix from vectorizer.fit_transform()
# currently, each cell is filled with its relative frequency, but change all of them to 1 for the one-hot-encoding
X_review_bin = (X > 0).astype(int)
Y_review_bin = (Y > 0).astype(int)

# convert to dense list format for cosine similarity
review_vectors = X_review_bin.toarray().tolist()
about_vectors = Y_review_bin.toarray().tolist()

# changes in the new file
df["review_vector"] = review_vectors
df["about_vector"] = about_vectors
df.to_csv(output_path, index=False)