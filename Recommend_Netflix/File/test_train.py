import random

# Read, sort, and save MovieLens u.data file
input_file = "File/u.data"
output_file = "File/sorted_u.data"
train_file = "File/train_u.data"
test_file = "File/test_u.data"

# Read all lines
with open(input_file, "r") as f:
    lines = f.readlines()

data = []

# Parse each line into tuples
for line in lines:
    parts = line.strip().split('\t')
    if len(parts) == 4:
        user_id, item_id, rating, timestamp = map(int, parts)
        data.append((user_id, item_id, rating, timestamp))

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
    for user_id, item_id, rating, timestamp in sorted_data:
        f.write(f"{user_id}\t{item_id}\t{rating}\t{timestamp}\n")

with open(train_file, "w") as f:
    for user_id, item_id, rating, timestamp in train_lines:
        f.write(f"{user_id}\t{item_id}\t{rating}\t{timestamp}\n")

with open(test_file, "w") as f:
    for user_id, item_id, rating, timestamp in test_lines:
        f.write(f"{user_id}\t{item_id}\t{rating}\t{timestamp}\n")