import os
import json
import re

project_dir = os.path.abspath(os.getcwd())
scraped_ressources_folder = os.path.join(
    project_dir, "..", "ScrapedData", "ScrapedFiles", "ScrapedRessources")
formated_data_folder = os.path.join(
    project_dir, "..", "ScrapedData", "FormatedDataFilesPrefixOnly")


desired_keys = ["title", "id", "itemTypeId", "rarity", "gfxId", "item_url"]
combined_data = []
total_items_processed = 0
total_items_combined = 0

for filename in os.listdir(formated_data_folder):
    if filename.endswith(".json") and filename != "allItems.json":
        file_path = os.path.join(formated_data_folder, filename)

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            total_items_processed += len(data)

        for item in data:
            base_params = item.get("baseParams", {})
            combined_item = {
                "title": item["title"],
                "id": item["id"],
                "rarity": base_params.get("rarity"),
                "itemTypeId": base_params.get("itemTypeId"),
                "gfxId": item["gfxId"],
                "item_url": item["item_url"]
            }
            combined_data.append(combined_item)

        total_items_combined += len(data)

output_file_path = os.path.join(formated_data_folder, "allItems.json")
with open(output_file_path, "w", encoding="utf-8") as output_file:
    json.dump(combined_data, output_file, indent=2, ensure_ascii=False)

print("Total items processed:", total_items_processed)
print("Total items combined:", total_items_combined)
print("Combined data has been saved to:", output_file_path)
