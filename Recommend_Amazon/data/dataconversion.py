import pandas as pd

# Load the CSV
df = pd.read_csv("Recommend_Amazon/File/amazon_with_vectors.csv")

# Clean the 'rating' column to float if it's not already
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df = df.dropna(subset=["rating"])


# ----- File 1: product_id, rating, review_vector, about_vector -----
product_data = df[["product_id", "rating", "review_vector", "about_vector"]]
product_data.to_csv("Recommend_Amazon/File/product_data.data", sep="\t", index=False, header=False)

# ----- File 2: user_id, product_id, rating -----
rows = []
for _, row in df.iterrows():
    product_id = row["product_id"]
    rating = row["rating"]
    user_ids = str(row["user_id"]).split(",") 
    for user_id in user_ids:
        user_id = user_id.strip()
        if user_id:
            rows.append((user_id, product_id, rating))

# Create DataFrame and sort
user_data_df = pd.DataFrame(rows, columns=["user_id", "product_id", "rating"])
user_data_df["user_id"] = user_data_df["user_id"].astype(int)
user_data_df["product_id"] = user_data_df["product_id"].astype(int)
user_data_df = user_data_df.sort_values(by=["user_id", "product_id"])

# Write to .data file
output_file = "Recommend_Amazon/File/user_data.data"
with open(output_file, "w") as f:
    for _, row in user_data_df.iterrows():
        user_id = int(float(row["user_id"]))
        product_id = int(float(row["product_id"]))
        rating = float(row["rating"])
        f.write(f"{user_id}\t{product_id}\t{rating:.1f}\n")