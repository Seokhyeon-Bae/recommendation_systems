import csv

# === File paths ===
input_file = 'Recommend_Amazon/File/amazon.csv'
output_file = 'Recommend_Amazon/File/amazon_indexed.csv'
product_map_file = 'Recommend_Amazon/File/product_map.data'
category_map_file = 'Recommend_Amazon/File/category_map.txt'
user_map_file = 'Recommend_Amazon/File/user_map.txt'

# === ID maps and counters ===
product_id_map = {}
category_id_map = {}
user_id_map = {}
product_counter = 1
category_counter = 1
user_counter = 1

# === Columns to remove from the final output ===
columns_to_remove = {
    "product_name", "review_title", "img_link", "product_link",
    "review_id", "user_name"  # KEEP 'user_id'
}

# === Helper function for assigning new indices ===
def get_or_assign(mapping, key, counter):
    if key not in mapping:
        mapping[key] = str(counter)
        return mapping[key], counter + 1
    return mapping[key], counter

# === Process CSV ===
with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile, \
     open(product_map_file, 'w', encoding='utf-8') as productmapfile, \
     open(category_map_file, 'w', encoding='utf-8') as categorymapfile, \
     open(user_map_file, 'w', encoding='utf-8') as usermapfile:

    reader = csv.DictReader(infile)
    # Retain only necessary columns
    fieldnames = [field for field in reader.fieldnames if field not in columns_to_remove]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        # Remove unwanted columns
        for col in columns_to_remove:
            row.pop(col, None)

        # === Map user_id(s) ===
        user_ids = [uid.strip() for uid in row['user_id'].split(',')]
        mapped_users = []
        for uid in user_ids:
            mapped_uid, user_counter = get_or_assign(user_id_map, uid, user_counter)
            mapped_users.append(mapped_uid)
        row['user_id'] = ','.join(mapped_users)

        # === Map product_id(s) ===
        product_ids = [pid.strip() for pid in row['product_id'].split(',')]
        mapped_products = []
        for pid in product_ids:
            mapped_pid, product_counter = get_or_assign(product_id_map, pid, product_counter)
            mapped_products.append(mapped_pid)
        row['product_id'] = ','.join(mapped_products)

        # === Map category(s) ===
        categories = [cat.strip() for cat in row['category'].split('|')]
        mapped_cats = []
        for cat in categories:
            mapped_cat, category_counter = get_or_assign(category_id_map, cat, category_counter)
            mapped_cats.append(mapped_cat)
        row['category'] = '|'.join(mapped_cats)

        # Write transformed row
        writer.writerow(row)

    # === Write map files ===
    for pid, idx in product_id_map.items():
        productmapfile.write(f"{idx} | {pid}\n")

    for cat, idx in category_id_map.items():
        categorymapfile.write(f"{idx} | {cat}\n")

    for uid, idx in user_id_map.items():
        usermapfile.write(f"{idx} | {uid}\n")
