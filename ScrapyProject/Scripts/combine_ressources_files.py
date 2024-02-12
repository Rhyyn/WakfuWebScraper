import os
import json
import re

project_dir = os.path.abspath(os.getcwd())
scraped_ressources_folder = os.path.join(
    project_dir, "..", "ScrapedData", "ScrapedFiles", "ScrapedRessources")
formated_ressources_folder = os.path.join(
    project_dir, "..", "ScrapedData", "FormatedRessources")


# def replace_unicode_escapes(text):
#     print(text)
#     unicode_mapping = {
#         r'\u00e9': 'é',
#         r'\u00ea': 'ê',
#         r'\u00ee': 'î',
#         r'\u00e8': 'è',
#         r'\u00fb': 'û',
#         r'\u00e4': 'ä',
#         r'\u00e2': 'â',
#         r'\u014d': 'ō'
#     }

#     for escape_sequence, char in unicode_mapping.items():
#         text = re.sub(escape_sequence, char, text)
#     print(text)
#     return text


with open(os.path.join(scraped_ressources_folder, "en_ressources_data.json"), "r", encoding="utf-8") as en_file:
    en_ressources_data = json.load(en_file)

with open(os.path.join(scraped_ressources_folder, "fr_ressources_data.json"), "r", encoding="utf-8") as fr_file:
    fr_ressources_data = json.load(fr_file)


merged_ressources = []
for en_ressource in en_ressources_data:
    for fr_ressource in fr_ressources_data:
        if en_ressource["id"] == fr_ressource["id"]:
            merged_ressources.append({
                "id": en_ressource["id"],
                "level": en_ressource["level"],
                "title": {"en": en_ressource["title"], "fr": fr_ressource["title"]},
                "rarity": en_ressource["rarity"],
                "gfxId": en_ressource["gfxId"]
            })
            break

output_file_path = os.path.join(formated_ressources_folder, "ressources.json")
with open(output_file_path, "w", encoding="utf-8") as output_file:
    json.dump(merged_ressources, output_file, indent=2, ensure_ascii=False)

print("Merged data has been saved to:", output_file_path)
