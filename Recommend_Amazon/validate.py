import ratings
import math

# calculate how off the prediction is from the actual value.
# base_ratings are the train set and the other is test set.
# we run the validate function to see if the code is meaningful.
class validator:
    def __init__(self, base_case_file, test_case_file):
        # Initialize and hash the product ratings
        self.base_ratings = ratings.ratings(base_case_file)
        self.base_ratings.hashing()

        # Read and store test lines
        with open(test_case_file, "r") as f:
            self.test_lines = f.readlines()

        self.prediction = []
        self.exact_count = 0
        self.off_by_half_count = 0
        self.off_by_more_count = 0

    def validate(self):
        for line in self.test_lines:
            if len(line.strip()) == 0:
                continue

            parts = line.strip().split('\t')
            if len(parts) < 4:
                continue

            product_id = int(parts[0])
            actual_rating = float(parts[1])

            predicted_rating = self.base_ratings.product_prediction(product_id)

            diff = abs(predicted_rating - actual_rating)

            if diff == 0:
                self.exact_count += 1
            elif diff <= 0.5:
                self.off_by_half_count += 1
            else:
                self.off_by_more_count += 1

            self.prediction.append(diff)

    def stats(self):
        n = len(self.prediction)
        if n == 0:
            return [0, 0, 0, 0, 0]

        mean = sum(self.prediction) / n
        stdev = math.sqrt(sum((x - mean) ** 2 for x in self.prediction) / (n - 1)) if n > 1 else 0

        return [
            self.exact_count,
            self.off_by_half_count,
            self.off_by_more_count,
            mean,
            stdev
        ]