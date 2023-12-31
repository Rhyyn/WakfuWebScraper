import json

# Read the entire items.json file
with open('items.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

subset_data = data[:400]

# Write the subset to a new file
with open('subset_items.json', 'w', encoding='utf-8') as new_file:
    json.dump(subset_data, new_file, ensure_ascii=False, indent=2)

print("Subset of items.json written to subset_items.json.")
