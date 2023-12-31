import json
import re
import os

# --------OPEN ITEMS JSON AND SLIM IT DOWN-------
# with open('items.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)

# subset_data = data[:500]

# with open('subset_items.json', 'w', encoding='utf-8') as output_file:
#     json.dump(subset_data, output_file, ensure_ascii=False, indent=2)

# print("Subset of items written to subset_items.json")
# --------OPEN ITEMS JSON AND SLIM IT DOWN-------

script_dir = os.path.dirname(__file__)

# FOR TESTING
with open('subset_items.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# with open('items.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)

with open('itemsStats.json', 'r', encoding='utf-8') as stats_file:
    item_stats_data = json.load(stats_file)

# List of files to check
files_to_check = ['Amulette.json', 'Anneau.json', 'Arme_secondemain.json', 'Armes_1main.json', 'Armes_2mains.json', 'Bottes.json',
                  'Cape.json', 'Casque.json', 'ceinture.json', 'Emblemes.json', 'Epaulette.json', 'Plastron.json', 'Sublimations.json']

new_items = []

subset_data = data[:20]

for item in data:
    new_item_format = {
        "title": {
            "fr": item["title"]["fr"],
            "en": item["title"]["en"]
        },
        "description": {
            "fr": item.get("description", {}).get("fr", ""),
            "en": item.get("description", {}).get("en", "")
        },
        "id": int(item["definition"]["item"]["id"]),
        "level": int(item["definition"]["item"]["level"]),
        "baseParams": {
            "itemTypeId": int(item["definition"]["item"]["baseParameters"]["itemTypeId"]),
            "itemSetId": int(item["definition"]["item"]["baseParameters"]["itemSetId"]),
            "rarity": int(item["definition"]["item"]["baseParameters"]["rarity"])
        },
        "useParams": {
            "useCostAp": int(item["definition"]["item"]["useParameters"]["useCostAp"]),
            "useCostMp": int(item["definition"]["item"]["useParameters"]["useCostMp"]),
            "useCostWp": int(item["definition"]["item"]["useParameters"]["useCostWp"]),
            "useRangeMin": int(item["definition"]["item"]["useParameters"]["useCostAp"]),
            "useRangeMax": int(item["definition"]["item"]["useParameters"]["useCostAp"]),
        },
        "gfxId": int(item["definition"]["item"]["graphicParameters"]["gfxId"]),
        "equipEffects": []
    }

    if "equipEffects" in item["definition"]:
        for effect_entry in item["definition"]["equipEffects"]:
            if "effect" in effect_entry:
                effect_definition = effect_entry["effect"].get(
                    "definition", {})
                params_list = effect_definition.get("params", [])
                first_param_value = int(
                    params_list[0]) if params_list else None
                action_id = effect_definition.get("actionId", "")
                stat_info = next(
                    (stat for stat in item_stats_data if stat["definition"]["id"] == action_id), {})
                stat_description_fr = stat_info.get(
                    "description", {}).get("fr", "")
                stat_description_fr_cleaned = re.sub(
                    r'[-\[]#(\d+)\]', '', stat_description_fr).strip()
                stat_value_fr = f"{first_param_value} {stat_description_fr_cleaned}" if first_param_value else ""

                stat_description_en = stat_info.get(
                    "description", {}).get("en", "")
                stat_description_en_cleaned = re.sub(
                    r'\[#\d+\]', '', stat_description_en).strip()
                stat_value_en = f"{first_param_value} {stat_description_en_cleaned}" if first_param_value else ""

                del effect_entry["effect"]["definition"]["areaShape"]
                del effect_entry["effect"]["definition"]["areaSize"]
                del effect_entry["effect"]["definition"]["params"]

                modified_effect_entry = {
                    "effect": {
                        "definition": {
                            "id": effect_definition.get("id", ""),
                        },
                        "stats": {
                            "display": {
                                "fr": stat_value_fr,
                                "en": stat_value_en
                            },
                            "property": action_id,
                            "value": first_param_value
                        }
                    }
                }
                new_item_format["equipEffects"].append(modified_effect_entry)

    matching_droprate_item = None
    # Check each file for droprates
    for file_to_check in files_to_check:
        file_path = os.path.join(script_dir, file_to_check)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as droprate_file:
                droprate_data = json.load(droprate_file)

                for droprate_item in droprate_data:
                    # print(str(droprate_item["item"]["id"]), new_item_format["id"])
                    if str(droprate_item["item"]["id"]) == str(new_item_format["id"]):
                        matching_droprate_item = droprate_item
                        break  # Stop searching further since we found a match

                if matching_droprate_item:  # type: ignore
                    new_item_format["droprates"] = matching_droprate_item.get(
                        "droprates", [])
                    print(
                        f"Match found in {file_to_check}: {new_item_format['droprates']}")
                    break  # Stop searching further since we found a match
                else:
                    print(
                        f"No match found in {file_to_check} for item ID {new_item_format['id']}")

        else:
            print(f"File not found: {file_path}")

    new_items.append(new_item_format)

with open('formated-items.json', 'w', encoding='utf-8') as new_file:
    json.dump(new_items, new_file, ensure_ascii=False, indent=2)

# {
#     "definition": {
#       "item": {
#         "id": 2021,
#         "level": 6,
#         "baseParameters": {
#           "itemTypeId": 120,
#           "itemSetId": 41,
#           "rarity": 1,
#           "bindType": 0,
#           "minimumShardSlotNumber": 1,
#           "maximumShardSlotNumber": 4
#         },
#         "useParameters": {
#           "useCostAp": 0,
#           "useCostMp": 0,
#           "useCostWp": 0,
#           "useRangeMin": 0,
#           "useRangeMax": 0,
#           "useTestFreeCell": false,
#           "useTestLos": false,
#           "useTestOnlyLine": false,
#           "useTestNoBorderCell": false,
#           "useWorldTarget": 0
#         },
#         "graphicParameters": {
#           "gfxId": 1202021,
#           "femaleGfxId": 1202021
#         },
#         "properties": []
#       },
#       "useEffects": [],
#       "useCriticalEffects": [],
#       "equipEffects": [
#         {
#           "effect": {
#             "definition": {
#               "id": 360361,
#               "actionId": 31,
#               "areaShape": 32767,
#               "areaSize": [],
#               "params": [
#                 1.0,
#                 0.0,
#                 1.0,
#                 0.0,
#                 0.0,
#                 0.0
#               ]
#             }
#           }
#         },
#         {
#           "effect": {
#             "definition": {
#               "id": 184047,
#               "actionId": 20,
#               "areaShape": 32767,
#               "areaSize": [],
#               "params": [
#                 6.0,
#                 0.0,
#                 1.0,
#                 0.0,
#                 0.0,
#                 0.0
#               ]
#             }
#           }
#         },
#         {
#           "effect": {
#             "definition": {
#               "id": 184048,
#               "actionId": 150,
#               "areaShape": 32767,
#               "areaSize": [],
#               "params": [
#                 2.0,
#                 0.0
#               ]
#             }
#           }
#         },
#         {
#           "effect": {
#             "definition": {
#               "id": 184049,
#               "actionId": 120,
#               "areaShape": 32767,
#               "areaSize": [],
#               "params": [
#                 9.0,
#                 0.0
#               ]
#             }
#           }
#         }
#       ]
#     },
#     "title": {
#       "fr": "Amulette du Bouftou",
#       "en": "Gobball Amulet",
#       "es": "Amuleto de jalató",
#       "pt": "Amuleto de Papatudo"
#     },
#     "description": {
#       "fr": "Attention mesdemoiselles, il paraît qu'elle bouffe tout, même les boutons de chemise et les lacets de tunique ! Ou peut-être n'est-ce qu'une légende ?",
#       "en": "Watch out ladies, it seems this thing chews everything it comes across! Lacy shawls, woolly sweaters, and even leather clavicle-warmers have all been known to get a nibbling. Or is it all just tall talk?",
#       "es": "Cuidado señoritas, al parecer se lo jala todo, ¡incluso los botones de las camisas y los lazos de las túnicas! ¿O quizás sea solo una leyenda?",
#       "pt": "Cuidado, meninas, parece que essa coisa mastiga tudo que passa pela frente! Xales rendados, suéteres de lã e até aquecedores de clavícula de couro já foram mordiscados. Ou é tudo conversa fiada?"
#     }
#   }
