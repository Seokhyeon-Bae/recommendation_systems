import numpy as np
from numpy.linalg import norm
import ast

# Convert stringified vectors to actual NumPy arrays for dot product and distance
def parse_vector(vec_str):
    try:
        return np.array(ast.literal_eval(vec_str))
    except:
        return np.zeros(256)


# add user_file as an input if needed
class ratings:
    def __init__(self, product_file):
        self.product_file = product_file
        # not going to use user file because the user data is not properly clustered
        # if the data is properly collected, might be able to use the user_data for the hybrid filtering
        # self.user_file = user_file
        # self.user_hash = {} 
        self.product_hash = {}
        self.average_review_score = 0

    def hashing(self):
        # Build user_hash and product_hash from user_data
        # disabled user_hash for now
        total_score = []
        with open(self.product_file, "r") as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) != 4:
                    continue
                
                product_id = int(parts[0])
                rating = float(parts[1])
                review_vector = ast.literal_eval(parts[2])  # safely parse list string
                about_vector = ast.literal_eval(parts[3])
                    

                # if user_id not in self.user_hash:
                #     self.user_hash[user_id] = []
                # self.user_hash[user_id].extend([product_id, rating])

                if product_id not in self.product_hash:
                    self.product_hash[product_id] = [review_vector, about_vector]
                self.product_hash[product_id].append(rating)
                total_score.append(rating)
        self.average_review_score = sum(total_score)/len(total_score)

    # Cosine similarity function for production similarity
    def cosine_similarity(self, vec1, vec2):
        return np.dot(vec1, vec2) / (norm(vec1) * norm(vec2)+1e-8) # dot product / distance of each var, avoid divide by 0 

    # def user_similarity(self, user1, user2):
    #     if user1 not in self.user_hash or user2 not in self.user_hash:
    #         return 0

    #     a = self.user_hash[user1]  # list: [prod_id, rating, prod_id, rating, ...]
    #     b = self.user_hash[user2]
        
    #     # Convert b to a dict for faster lookup
    #     b_dict = {b[i]: int(b[i + 1]) for i in range(0, len(b), 2)}

    #     similarities = []

    #     for i in range(0, len(a), 2):
    #         product_a = a[i]
    #         rating_a = int(a[i + 1])
            
    #         if product_a in b_dict:
    #             rating_b = b_dict[product_a]
    #             similarity = 1 - abs(rating_a - rating_b) / 5.0  # scale 0–1
    #             similarities.append(similarity)

    #     if not similarities:
    #         return 0

    #     return sum(similarities) / len(similarities)

            
    def most_similar_product(self, product_id):
        similar_products = []
        sim_score = []
        
        # if product_id not in the set, unable to find the similarity
        if product_id not in self.product_hash:
            return [[], []]
        
        # find cosine similarity of the product comparing to other products and append product_id if similar
        # append similar score as well for the better prediction
        for products in self.product_hash:
            if products != product_id:
                review_sim = self.cosine_similarity(self.product_hash[products][0], self.product_hash[product_id][0])
                about_sim = self.cosine_similarity(self.product_hash[products][1], self.product_hash[product_id][1])
                if review_sim >= 0.1 and about_sim >= 0.1:
                    similar_products.append(products)
                    sim_score.append(review_sim + about_sim)
        return [similar_products, sim_score]

    # Return simliar users using matrix factorization
    # Comment: this does not work well because the raw dataset had already clustered user_id.
    #          this method followed the netflix method
    # def most_similar_user(self, user_id):
    #     similar_users = []
    #     for users in self.user_hash:
    #         # avoid comparing the same user
    #         if users == user_id:
    #             continue
            
    #         if self.user_similarity(user_id, users) >= 0.3:
    #             similar_users.append(users)

    #     return similar_users
    
    # prediction using user hash does not work - will not use this prediction
    # def hybrid_predict(self, user, product):
    #     if user not in self.user_hash:
    #         return 3.0  # default for unknown user

    #     user_data = self.user_hash[user]
    #     user_dict = {user_data[i]: float(user_data[i+1]) for i in range(0, len(user_data), 2)}

    #     # If user already rated this product
    #     if product in user_dict:
    #         return user_dict[product]

    #     sim_ratings = []

    #     # 1. Use similar products that this user rated
    #     similar_products = self.most_similar_product(product)
    #     for i in range(0, len(user_data), 2):
    #         prod = user_data[i]
    #         rating = float(user_data[i+1])
    #         if prod in similar_products:
    #             sim_ratings.append(rating)

    #     # 2. Use similar users who rated this product
    #     similar_users = self.most_similar_user(user)
    #     for other_user in similar_users:
    #         other_data = self.user_hash[other_user]
    #         other_dict = {other_data[i]: float(other_data[i+1]) for i in range(0, len(other_data), 2)}
    #         if product in other_dict:
    #             sim_ratings.append(other_dict[product])

    #     if not sim_ratings:
    #         return 3.0  # fallback average rating

    #     return sum(sim_ratings) / len(sim_ratings)
    
    # prediction using product only
    def product_prediction(self, product):
        similarity_eval = self.most_similar_product(product)
        similar_products = similarity_eval[0]
        sim_scores = similarity_eval[1]
        
        # put ratings of similar products into the sim_ratings array
        weighted_sum = 0
        total_weight = 0

        for i in range(len(similar_products)):
            prod_id = similar_products[i]
            if prod_id not in self.product_hash:
                continue
            score = sim_scores[i]
            ratings = self.product_hash[prod_id][2:]

            if ratings:
                avg_rating = sum(ratings) / len(ratings)
                weighted_sum += avg_rating * score
                total_weight += score

        if total_weight == 0:
            return self.average_review_score  # set dafault rating to average
                    
        
        # avearge of the sim_ratings for the prediction
        return round(weighted_sum / total_weight, 1)
