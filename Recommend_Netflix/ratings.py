class Ratings:
    def __init__(self, input_file):
        # Read all lines
        self.f = open(input_file, "r")
        
        self.user_hash = {}
        self.movie_hash = {}
        
    def hashing(self):
        # split lines
        lines = self.f.readlines()
        
        # user_hash, user ID: movie ID, ratings
        # movie_hash, movie ID: user ID, ratings
        for line in lines:
            if len(line.strip()) == 0:
                continue
            parts = line.strip().split()
            user, movie, rating = int(parts[0]), int(parts[1]), int(parts[2])
            # user_hash
            if user not in self.user_hash:
                self.user_hash[user] = []
            self.user_hash[user].extend([movie, rating])

            # movie_hash
            if movie not in self.movie_hash:
                self.movie_hash[movie] = []
            self.movie_hash[movie].extend([user, rating])
        
    # calculate how popular the movie is based on ratings
    def popularity(self, movie_id):
        if movie_id not in self.movie_hash:
            return 3
        # if movie_id not in hash, return 1(not popular)        
        rate_list = self.movie_hash[movie_id]
        
        if len(rate_list) < 2:
            return 1
        
        rate_count = 1
        popular_rate = 0
        
        # iterate until it reaches the end of the value
        while rate_count < len(self.movie_hash[movie_id]):
            popular_rate += self.movie_hash[movie_id][rate_count]
            rate_count += 2

        # return the popularity
        return int(round((popular_rate)/(rate_count//2)))
    
    # return the similarity, 0 if no simliarity at all
    def similarity(self, user1, user2):
        if user1 not in self.user_hash or user2 not in self.user_hash:
            return "User Not Found"
        sim = []
        a = self.user_hash[user1]
        b = self.user_hash[user2]
        i = 0
        while i < len(a):
            movie_a = a[i]
            rating_a = int(a[i+1])
            if movie_a in b:
                j = b.index(movie_a)
                rating_b = int(b[j+1])
                # simliarity += abs((ratings1 - ratings2)/5)
                diff = abs(rating_a - rating_b) / 5.0
                sim.append(diff)
            i += 2
        if not sim:
            return 0
        return sum(sim) / len(sim)

    # return the list of most similar users 
    def most_similar(self, user):
        similar = []
        for other in self.user_hash:
            # if similarity is larger than 0.4, append the user to the list 
             if other != user and self.similarity(user, other) >= 0.4:
                similar.append(other)
        return similar
    
    # predict what the user is going to rate the movie
    def predict(self, user, movie):
        
        return self.popularity(movie)
        # similar_users = self.most_similar(user)
        # ratings = []
        
        # # put most_similar for broader purpose
        # # when optimizing, we can put user_list as an input instead for fast return
        # for u in similar_users:
        #     items = self.user_hash[u]
        #     i = 0
        #     while i < len(items):
        #         if items[i] == movie:
        #             ratings.append(int(items[i+1]))
        #         i += 2
        # # if no similar user rated the movie, the user will not like the movie.
        # if not ratings:
        #     return 1
        
        # return sum(ratings)//len(ratings)

    # return the recommend movie list, and the not recommend list in case
    def recommend_movie_list(self, user):
        watched = set()
        a = 0
        # if the user already rated the movie, append it to the watched
        while a < len(self.user_hash[user]):
            watched.add(self.user_hash[user][a])
            a += 2
        highly_recommend = set()
        recommend = set()
        not_recommend = set()
        # for each similar users, see if it is recommendable or not
        for u in self.most_similar(user):
            j = 0
            while j < len(self.user_hash[u]):
                movie = self.user_hash[u][j]
                if movie not in watched:
                    rating = self.predict(user, movie)
                    if rating >= 4.70:
                        highly_recommend.add(movie)
                    elif rating >= 4.20:
                        recommend.add(movie)
                    else:
                        not_recommend.add(movie)
                j += 2
        return print("highly recommended: ", sorted(list(highly_recommend)), "\nrecommened: ", sorted(list(recommend)))
