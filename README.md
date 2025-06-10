# Recommendation Systems Project

This project explores two recommendation system approaches:

1. **User-based Filtering** using the Netflix dataset from GitHub:  
   [https://github.com/MARCOpo1o/Movie-rating-prediction-algorithm](https://github.com/MARCOpo1o/Movie-rating-prediction-algorithm)

2. **Content-based Filtering** using the Amazon dataset from Kaggle:  
   [https://www.kaggle.com/code/mehakiftikhar/amazon-sales-dataset-eda](https://www.kaggle.com/code/mehakiftikhar/amazon-sales-dataset-eda)

I actually tried hybrid filtering on the Amazon dataset, but failed due to bias in the data — user IDs were already clustered.  
I left those parts in the code so you can see how I approached the problem.

---

## 1. User-based Filtering

I mostly followed the process from the referenced GitHub repository.

### ⭐ `ratings.py` – Approach

#### 1. Dataset usage – `hashing()`
The dataset has a format of user ID, movie ID, rating, and timestamp.  
Once we load the file and apply the `hashing()` function, it builds:

- `user_hash` → `user_id: movie_id1, rating1, movie_id2, rating2, ...`
- `movie_hash` → `movie_id: user_id1, rating1, user_id2, rating2, ...`

#### 2. Movie Popularity – `popularity(movie_id)`
Evaluates how popular a movie is.  
Returns the average rating for the target `movie_id` using `movie_hash`.

#### 3. User Similarity – `similarity(user1, user2)`
Compares two users by evaluating their rating differences on mutual movies.  
Uses `abs((rating1 - rating2) / 5)` and averages it.  
Returns `0` if there's no mutual movie.

#### 4. Most Similar Users – `most_similar(user)`
Returns a list of users with similarity score higher than `0.4` compared to the input user.

#### 5. Predict Ratings – `predict(user, movie)`
Tried collaborative filtering here, but it failed due to insufficient data.  
However, I left the code so you can see the approach.

---

You can check prediction accuracy using `validate.py`.  
I'll add `main.py` and the virtual environment file later.

---

### 🔄 Changes from Original GitHub Project

- Original system used **Ruby**, mine uses **Python**.
- I manually split the train-test sets (see `test_train.py`).
- I added a function that returns a list of recommended movies.

---

## 2. Content-based Filtering

The Amazon dataset had many redundant columns.  
I extracted only the ones necessary for filtering.

### ⭐ Data Handling – "Data" folder inside `File/`

#### 1. `datacleaning.py`
- Converted string values into integer values (e.g., `user_id`, `product_id`)
- Removed unused columns like `product_name`, `review_title`, `img_link`, `product_link`, `review_id`, `user_name`
- Result saved as `amazon_indexed.csv`

#### 2. `vectorize.py`
- Tokenized `review_content` and `about_product`
- Converted them into 256-dimensional vectors  
- Output: `amazon_with_vectors.csv`

#### 3. `dataconversion.py`
- Converted `.csv` into `.data` format
  - `product_data.data`: `product_id, rating, review_vector, about_vector`
  - `user_data.data`: `user_id, product_id, rating` (not used due to bias)

#### 4. `test_train.py`
- Shuffled data using `random`
- Split into 80% train / 20% test
- Sorted by `product_id`

---

### ⭐ `ratings.py` – Approach

I left hybrid filtering code in place, but it won't work well because we can't cluster `user_id` based on `most_similar`.  
The original dataset contains average ratings from multiple users, leading to clustered user ratings that don’t allow meaningful prediction.

#### 1. `hashing()`
Same structure as the first project.  
However, `user_hash` is not used.  
- `product_hash` → `product_id: review_vector, about_vector, rating1, rating2, ...`

#### 2. `cosine_similarity(vec1, vec2)`
Measures cosine similarity between two vectors (review/about).  
Formula: **dot product / (norm(vec1) × norm(vec2))**

#### 3. `most_similar_product(product)`
Finds other products with cosine similarity > `0.1` in **both** review and about vectors.  
Returns both product IDs and similarity scores.

#### 4. `product_prediction(product)`
Returns the **weighted average** of ratings from the most similar products.

---

### ▶️ How to Run

```bash
git clone https://github.com/Seokhyeon-Bae/recommendation_systems.git
cd Recommend_Amazon
python main.py
```

---
### reflection
A recommendation system is known as a basic machine learning technique. I had fun thinking of how I should solve the problems. 
Recommendation itself is hard as well, but how I handle the data was pretty important. 
As this is my first recommendation system project, I had to delete the whole code and start all over again 3 times. However, it was a meaningful process because now I know which data is important.
Also, the recommendation process can have multiple approaches, each with different role.
I learned that picking the right method can also affect the result a lot. 
For example, if I were to use user-based filtering on the second project, the project seemed to work fine because it was overfitted, which would result pretty bad if I had new data to predict.
