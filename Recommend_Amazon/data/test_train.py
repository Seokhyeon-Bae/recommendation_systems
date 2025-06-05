import random
import ast

# Read, sort, and save MovieLens u.data file
input_file = "Recommend_Amazon/File/product_data.data"
output_file = "Recommend_Amazon/File/product_data_sorted.data"
train_file = "Recommend_Amazon/File/train_u.data"
test_file = "Recommend_Amazon/File/test_u.data"

# Read all lines
with open(input_file, "r") as f:
    lines = f.readlines()

data = []

# Parse each line into tuples
for line in lines:
    parts = line.strip().split('\t')
    if len(parts) == 4:
        product_id = int(parts[0])
        rating = float(parts[1])
        review_vector = ast.literal_eval(parts[2])  # safely parse list string
        about_vector = ast.literal_eval(parts[3])
        data.append((product_id, rating, review_vector, about_vector))

# Sort
sorted_data = sorted(data, key=lambda x: (x[0],x[1]))

# making a train and test set
# 8:2 split into train and test
split_index = int(0.8 * len(data))

random.shuffle(data)

# split them by array length
bare_train_lines = data[:split_index]
bare_test_lines = data[split_index:]

# sort
train_lines = sorted(bare_train_lines, key=lambda x: (x[0], x[1]))
test_lines = sorted(bare_test_lines, key=lambda x: (x[0], x[1]))

# Store it in another file
# If needed, we can make more than 1 set of train test dataset
with open(output_file, "w") as f:
    for product_id, rating, review_vector, about_vector in sorted_data:
        f.write(f"{product_id}\t{rating}\t{review_vector}\t{about_vector}\n")

with open(train_file, "w") as f:
    for product_id, rating, review_vector, about_vector in train_lines:
        f.write(f"{product_id}\t{rating}\t{review_vector}\t{about_vector}\n")

with open(test_file, "w") as f:
    for product_id, rating, review_vector, about_vector in test_lines:
        f.write(f"{product_id}\t{rating}\t{review_vector}\t{about_vector}\n")