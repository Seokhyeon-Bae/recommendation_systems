import ratings
import math

# calculate how off the prediction is from the actual value.
# base_ratings are the train set and the other is test set.
# we run the validate function to see if the code is meaningful.
class validator:
    def __init__(self, base_case, test_case):
        self.base_ratings = ratings.Ratings(base_case)
        self.base_ratings.hashing()
        self.user = self.base_ratings.user_hash
        self.movie = self.base_ratings.movie_hash
        self.test = open(test_case, "r")
        self.prediction = []
        self.exact_count = 0
        self.off_by_one_count = 0
        self.off_by_more_count = 0
    
    # calculate difference of the prediction from train model compared to test model
    def validate(self):
        lines = self.test.readlines()
        for line in lines:
            if len(line.strip()) == 0:
                continue
            parts = line.strip().split()
            if int(parts[1]) in self.base_ratings.movie_hash:
                diff = abs(int(parts[2]) - self.base_ratings.predict(parts[0], parts[1]))
                if diff == 0:
                    self.exact_count += 1
                elif diff <= 1:
                    self.off_by_one_count +=1
                else:
                    self.off_by_more_count += 1
                self.prediction.append(diff)
    
    # return exact, off by one, off by more than one, mean, standard deviation
    def stats(self):
        if len(self.prediction) == 0:
            return [0, 0, 0, 0, 0]
        
        mean = sum(self.prediction) / len(self.prediction)
        # rooted sum of squared (num - mean) 
        stdev = math.sqrt(sum((x - mean) ** 2 for x in self.prediction) / (len(self.prediction) - 1))
        
        return [
            self.exact_count,
            self.off_by_one_count,
            self.off_by_more_count,
            mean,
            stdev
        ]