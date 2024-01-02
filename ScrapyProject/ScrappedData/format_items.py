import os
import json
import click
import re
import typing

@click.group()
def cli():
    pass


@click.command()
def format_items():
    # Get a list of all JSON files in the current directory
    json_files = [file for file in os.listdir() if file.endswith('.json')]

    if not json_files:
        click.echo("No JSON files found in the current directory.")
        return

    click.echo(f"Available files to format: {json_files}")

    # Ask the user to input the filename
    selected_file = click.prompt(
        "Enter the name of the file to format", type=click.Choice(json_files))

    # Validate if the selected file exists
    if selected_file not in json_files:
        click.echo(f"Error: File '{selected_file}' not found.")
        return

    # Format the selected JSON file
    format_json(selected_file)
    click.echo(f"File '{selected_file}' formatted successfully.")


patterns = ["{[>1]?s:}",
            "{[~2]?%:}",
            "{[~2]?([#2]%):}",
            "{[99>3]?:{[0<3]?:{[~3]?([#3]%):}}}",
            "{[~3]?[#1] Résistance [#3]:[#1] Résistance sur [#2] élément{[>2]?s:} aléatoire{[>2]?s:}}",
            "{[~3]?[#1] Resistance [#3]:[#1] Resistance to [#2] random element{[>2]?s:}}" <
            "{[~3]?[#1] Maîtrise [#3]:[#1] Maîtrise sur [#2] élément{[>2]?s:} aléatoire{[>2]?s:}}",
            "{[~3]?[#1] Mastery [#3]:[#1] Mastery of [#2] random{[=2]?:} element{[=2]?:s}}",
            "{[~2]? en [#2]:}"]

jobs = {
    '75' : {'fr': 'Pêcheur', 'en' : "Fisherman"},
    '71' : {'fr': 'Forestier', 'en' : "Lumberjack"},
    '72' : {'fr': 'Herboriste', 'en' : "Herbalist"},
    '64' : {'fr': 'Paysan', 'en' : "Farmer"},
    '73' : {'fr': 'Mineur', 'en' : "Miner"},
    '74' : {'fr': 'Trappeur', 'en' : "Trapper"},
    '77' : {'fr': 'Armurier', 'en' : "Armorer"},
    '78' : {'fr': 'Bijoutier', 'en' : "Jeweler"},
    '40' : {'fr': 'Boulanger', 'en' : "Baker"},
    '76' : {'fr': 'Cuisinier', 'en' : "Chef"},
    '81' : {'fr': 'Ébéniste', 'en' : "Handyman"},
    '83' : {'fr': "Maitre d'armes", 'en' : "Weapons Master"},
    '80' : {'fr': 'Maroquinier', 'en' : "Leather Dealer"},
    '79' : {'fr': 'Tailleur', 'en' : "Tailor"},
}


element_mapping = {
    'el0': {'fr': 'Neutre', 'en': 'Neutral'},
    'el1': {'fr': 'Feu', 'en': 'Fire'},
    'el2': {'fr': 'Eau', 'en': 'Water'},
    'el3': {'fr': 'Terre', 'en': 'Earth'},
    'el4': {'fr': 'Air', 'en': 'Air'},
    'el6': {'fr': 'Lumière', 'en': 'Light'},
}

element_pattern = re.compile(r'\[(el\d+)\]')

def replace_element(match: re.Match) -> str:
    element_key = match.group(1)
    
    if element_key in element_mapping:
        language = 'fr'
        return element_mapping[element_key][language]
    
    return match.group(0)


def interpret_description(action_id:int, params_list:list, stat_description:dict):
    result = {
                "display": {
                    "fr": '',
                    "en": ''
                },
                "property": action_id,
                "values": []
            }
    
    match int(action_id):
        case action_id if action_id in [20, 26, 31, 41, 71, 80, 82, 83, 84, 85, 120, 122, 123, 124, 125, 149, 160, 162, 166, 171, 173, 175, 177, 180, 184, 191, 988, 1052, 1053, 1055, 150, 875, 56, 57, 90, 96, 97, 98, 100, 130, 132, 172, 174, 176, 181, 192, 876, 1056, 1059, 1060, 1061, 1062, 1063]:
            # gain flat
            result['values'] = [int(params_list[0])]
            for lang_key, lang_description in stat_description.items():
                if lang_key in ['fr', 'en'] and isinstance(lang_description, str):
                    updated_description = re.sub(r'\[#1\]', str(int(params_list[0])), lang_description)
                    updated_description = element_pattern.sub(lambda match: replace_element(match), updated_description)
                    result["display"][lang_key] = updated_description
            # print(result)
            return result
        case action_id if action_id in [21]:
            # perte / deboost flat
            result['values'] = [int(params_list[0])]
            for lang_key, lang_description in stat_description.items():
                if lang_key == 'fr' and isinstance(lang_description, str):
                    result["display"][lang_key] = f'-{int(params_list[0])} PV'
                elif lang_key == 'en':
                    result["display"][lang_key] = f'-{int(params_list[0])} HP'

            return result
        case 1068:
            # random mastery
            result['values'] = [int(params_list[0]), int(params_list[2])]
            result['display']['fr'] = '[#1] Maîtrise sur [#2] éléments aléatoires'.replace(
                '[#1]', str(int(params_list[0]))).replace('[#2]', str(int(params_list[2])))
            result['display']['en'] = '[#1] Mastery of [#2] randoms elements'.replace(
                '[#1]', str(int(params_list[0]))).replace('[#2]', str(int(params_list[2])))
            return result
        case 1069:
            # random resists
            result['values'] = [int(params_list[0]), int(params_list[2])]
            result['display']['fr'] = '[#1] Résistance sur [#2] éléments aléatoires'.replace(
                '[#1]', str(int(params_list[0]))).replace('[#2]', str(int(params_list[2])))
            result['display']['en'] = '[#1] Resistance of [#2] randoms elements'.replace(
                '[#1]', str(int(params_list[0]))).replace('[#2]', str(int(params_list[2])))
            return result
        case 2001: 
            # recolte
            result['values'] = [int(params_list[0])]
            if int(params_list[2]):
                result['jobs_id'] = [int(params_list[2])]
                result["display"]["fr"] = '[#1]% Quantité Récolte en [#2]'.replace('[#1]', str(int(params_list[0]))).replace('[#2]', str(int(params_list[2])))
                result["display"]["en"] = '[#1]% Harvesting Quantity in [#2]'.replace('[#1]', str(int(params_list[0]))).replace('[#2]', str(int(params_list[2])))
            else:
                result["display"]["fr"] = '[#1]% Quantité Récolte'
                result["display"]["en"] = '[#1]% Harvesting Quantity'
            return result
        case action_id if action_id in [39, 40]:
            # perte avec custom charac2
            if int(params_list[2]):

                result["display"]["fr"] = "-[#1] [#3]"
            return result

    return result



def format_json(filename):
    with open(filename, 'r', encoding='utf-8') as scrapped_file:
        scrapped_data = json.load(scrapped_file)

    with open("items.json", 'r', encoding='utf-8') as all_items_file:
        all_items_data = json.load(all_items_file)

    with open('actions.json', 'r', encoding='utf-8') as stats_file:
        actions_data = json.load(stats_file)

    new_items = []

    for scrapped_item in scrapped_data:
        for original_item in all_items_data:
            if int(scrapped_item["item"]["id"]) == int(original_item["definition"]["item"]["id"]):
                new_item_format = {
                    "title": {
                        "fr": original_item["title"]["fr"],
                        "en": original_item["title"]["en"]
                    },
                    "description": {
                        "fr": original_item.get("description", {}).get("fr", ""),
                        "en": original_item.get("description", {}).get("en", "")
                    },
                    "droprates": scrapped_item["droprates"],
                    "id": int(original_item["definition"]["item"]["id"]),
                    "level": int(original_item["definition"]["item"]["level"]),
                    "baseParams": {
                        "itemTypeId": int(original_item["definition"]["item"]["baseParameters"]["itemTypeId"]),
                        "itemSetId": int(original_item["definition"]["item"]["baseParameters"]["itemSetId"]),
                        "rarity": int(original_item["definition"]["item"]["baseParameters"]["rarity"])
                    },
                    "useParams": {
                        "useCostAp": int(original_item["definition"]["item"]["useParameters"]["useCostAp"]),
                        "useCostMp": int(original_item["definition"]["item"]["useParameters"]["useCostMp"]),
                        "useCostWp": int(original_item["definition"]["item"]["useParameters"]["useCostWp"]),
                        "useRangeMin": int(original_item["definition"]["item"]["useParameters"]["useRangeMin"]),
                        "useRangeMax": int(original_item["definition"]["item"]["useParameters"]["useRangeMax"]),
                    },
                    "gfxId": int(original_item["definition"]["item"]["graphicParameters"]["gfxId"]),
                    "equipEffects": [],
                    "item_url": scrapped_item["item_url"]
                }

                if "equipEffects" in original_item["definition"]:
                    for effect_entry in original_item["definition"]["equipEffects"]:
                        if "effect" in effect_entry:
                            effect_definition = effect_entry["effect"].get(
                                "definition", {})
                            params_list = effect_definition.get("params", [])
                            first_param_value = int(
                                params_list[0]) if params_list else None
                            action_id = effect_definition.get("actionId", "")
                            stat_info = next(
                                (stat for stat in actions_data if stat["definition"]["id"] == action_id), {})
                            stat_description_fr = stat_info.get(
                                "description", {}).get("fr", "")
                            stat_description = stat_info.get(
                                "description", {})
                            stat_description = interpret_description(action_id, params_list, stat_description)
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
                                            "fr": stat_description["display"]["fr"],
                                            "en": stat_description["display"]["en"]  
                                        },
                                        "property": stat_description["property"],
                                        "values": stat_description["values"],
                                    }
                                }
                            }
                            # print(modified_effect_entry)
                            new_item_format["equipEffects"].append(
                                modified_effect_entry)
                new_items.append(new_item_format)

    file_path = os.path.join(os.path.dirname(os.path.realpath(
        __file__)), 'FormatedData', f'{filename}_formated.json')
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(new_items, file, ensure_ascii=False,
                  indent=2)  # type: ignore


cli.add_command(format_items)
# cli.add_command(crawl)


if __name__ == '__main__':
    format_items()


# for item in data:
#     new_item_format = {
#         "title": {
#             "fr": item["title"]["fr"],
#             "en": item["title"]["en"]
#         },
#         "description": {
#             "fr": item.get("description", {}).get("fr", ""),
#             "en": item.get("description", {}).get("en", "")
#         },
#         "id": int(item["definition"]["item"]["id"]),
#         "level": int(item["definition"]["item"]["level"]),
#         "baseParams": {
#             "itemTypeId": int(item["definition"]["item"]["baseParameters"]["itemTypeId"]),
#             "itemSetId": int(item["definition"]["item"]["baseParameters"]["itemSetId"]),
#             "rarity": int(item["definition"]["item"]["baseParameters"]["rarity"])
#         },
#         "useParams": {
#             "useCostAp": int(item["definition"]["item"]["useParameters"]["useCostAp"]),
#             "useCostMp": int(item["definition"]["item"]["useParameters"]["useCostMp"]),
#             "useCostWp": int(item["definition"]["item"]["useParameters"]["useCostWp"]),
#             "useRangeMin": int(item["definition"]["item"]["useParameters"]["useCostAp"]),
#             "useRangeMax": int(item["definition"]["item"]["useParameters"]["useCostAp"]),
#         },
#         "gfxId": int(item["definition"]["item"]["graphicParameters"]["gfxId"]),
#         "equipEffects": []
#     }

#     if "equipEffects" in item["definition"]:
#         for effect_entry in item["definition"]["equipEffects"]:
#             if "effect" in effect_entry:
#                 effect_definition = effect_entry["effect"].get(
#                     "definition", {})
#                 params_list = effect_definition.get("params", [])
#                 first_param_value = int(
#                     params_list[0]) if params_list else None
#                 action_id = effect_definition.get("actionId", "")
#                 stat_info = next(
#                     (stat for stat in actions_data if stat["definition"]["id"] == action_id), {})
#                 stat_description_fr = stat_info.get(
#                     "description", {}).get("fr", "")
#                 stat_description_fr_cleaned = re.sub(
#                     r'[-\[]#(\d+)\]', '', stat_description_fr).strip()
#                 stat_value_fr = f"{first_param_value} {stat_description_fr_cleaned}" if first_param_value else ""

#                 stat_description_en = stat_info.get(
#                     "description", {}).get("en", "")
#                 stat_description_en_cleaned = re.sub(
#                     r'\[#\d+\]', '', stat_description_en).strip()
#                 stat_value_en = f"{first_param_value} {stat_description_en_cleaned}" if first_param_value else ""

#                 del effect_entry["effect"]["definition"]["areaShape"]
#                 del effect_entry["effect"]["definition"]["areaSize"]
#                 del effect_entry["effect"]["definition"]["params"]

#                 modified_effect_entry = {
#                     "effect": {
#                         "definition": {
#                             "id": effect_definition.get("id", ""),
#                         },
#                         "stats": {
#                             "display": {
#                                 "fr": stat_value_fr,
#                                 "en": stat_value_en
#                             },
#                             "property": action_id,
#                             "value": first_param_value
#                         }
#                     }
#                 }
#                 new_item_format["equipEffects"].append(modified_effect_entry)

#     matching_droprate_item = None
#     # Check each file for droprates
#     for file_to_check in files_to_check:
#         file_path = os.path.join(script_dir, file_to_check)
#         if os.path.exists(file_path):
#             with open(file_path, 'r', encoding='utf-8') as droprate_file:
#                 droprate_data = json.load(droprate_file)

#                 for droprate_item in droprate_data:
#                     # print(str(droprate_item["item"]["id"]), new_item_format["id"])
#                     if str(droprate_item["item"]["id"]) == str(new_item_format["id"]):
#                         matching_droprate_item = droprate_item
#                         break  # Stop searching further since we found a match

#                 if matching_droprate_item:  # type: ignore
#                     new_item_format["droprates"] = matching_droprate_item.get(
#                         "droprates", [])
#                     print(
#                         f"Match found in {file_to_check}: {new_item_format['droprates']}")
#                     break  # Stop searching further since we found a match
#                 else:
#                     print(
#                         f"No match found in {file_to_check} for item ID {new_item_format['id']}")

#         else:
#             print(f"File not found: {file_path}")

#     new_items.append(new_item_format)
