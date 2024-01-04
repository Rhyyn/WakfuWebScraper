import os
import json
import click
import re
import typing
from typing import Any, Union, List, Dict, Type, Optional

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

result =  {
                "display": {
                    "fr": '',
                    "en": ''
                },
                "property": "",
                "values": ''
            }
element_pattern = re.compile(r'\[(el\d+)\]')


class FormatedParams:
    fr:str = ''
    en:str = ''
    property:int = 0
    values:list[int] | int = []
    job_id:Optional[int]


def replace_element(match: re.Match) -> str:
    element_key = match.group(1)
    
    if element_key in element_mapping:
        language = 'fr'
        return element_mapping[element_key][language]
    
    return match.group(0)

def starts_with_hyphen(s):
    pattern = re.compile(r'^-')
    return bool(pattern.match(s))


def check_return_values(params_list:list[int]) -> list[int] | int:
    if len(params_list) >= 3 and params_list[2] is not None: 
        return int(params_list[0]) + (int(params_list[1]) * 50)
    else:
        return int(params_list[0])


def format_flat_stat_gain(action_id:int, params_list:list[int], stat_description:dict[str, str]) -> FormatedParams:
    formated_params = FormatedParams()
    values = check_return_values(params_list)
    formated_params.values = values
    formated_params.property = action_id
    for lang_key, lang_description in stat_description.items():
        if lang_key in ['fr', 'en'] and isinstance(lang_description, str):
            updated_description = re.sub(r'\[#1\]', str(values), lang_description)
            updated_description = element_pattern.sub(lambda match: replace_element(match), updated_description)
            setattr(formated_params, lang_key, updated_description)
    return formated_params


def format_flat_stat_deboost(action_id:int, params_list:list[int], stat_description:dict[str, str]) -> FormatedParams:
    formated_params = FormatedParams()
    values = check_return_values(params_list)
    formated_params.values = values
    formated_params.property = action_id
    formated_params.fr = f'-{int(params_list[0])} PV'
    formated_params.en = f'-{int(params_list[0])} HP'
    return formated_params


def format_random_stat(action_id:int, params_list:list[int]) -> FormatedParams:
    formated_params = FormatedParams()
    values = check_return_values(params_list)
    formated_params.values = values
    formated_params.property = action_id
    strings = {
        1068 : {
            'fr' : '[#1] Maîtrise sur [#2] éléments aléatoires',
            'en' : '[#1] Mastery of [#2] randoms elements'
        },
        1069 : {
            'fr' : '[#1] Résistance sur [#2] éléments aléatoires',
            'en' : '[#1] Resistance of [#2] randoms elements'
        }
    }
    formated_params.fr = strings[action_id]['fr'].replace('[#1]', str(int(params_list[0]))).replace('[#2]', str(int(params_list[2])))
    formated_params.en = strings[action_id]['en'].replace('[#1]', str(int(params_list[0]))).replace('[#2]', str(int(params_list[2])))
    return formated_params


def format_gathering_stat(action_id:int, params_list:list[int]) -> FormatedParams:
    formated_params = FormatedParams()
    values = check_return_values(params_list)
    formated_params.values = values
    formated_params.property = action_id
    if int(params_list[2]):
        formated_params.job_id = int(params_list[2])
        formated_params.fr = '[#1]% Quantité Récolte en [#2]'.replace('[#1]', str(int(params_list[0]))).replace('[#2]', str(int(params_list[2])))
        formated_params.en = '[#1]% Harvesting Quantity in [#2]'.replace('[#1]', str(int(params_list[0]))).replace('[#2]', str(int(params_list[2])))
    else:
        formated_params.fr = '[#1]% Quantité Récolte'.replace('[#1]', str(int(params_list[0])))
        formated_params.en = '[#1]% Harvesting Quantity'.replace('[#1]', str(int(params_list[0])))    
    return formated_params


def format_custom_charac(action_id:int, params_list:list[int]) -> FormatedParams:
    formated_params = FormatedParams()
    values = check_return_values(params_list)
    formated_params.values = values
    formated_params.property = action_id
    fourth_param:int = int(params_list[4])
    strings = {
        120 : {
            'fr' : '% Armure donnée',
            'en' : '% Armor given'
        },
        121 : {
            'fr' : '% Armure reçue',
            'en' : '% Armor received'
        }
    }
    # only works for Armor, lack the IDs for more stat support
    if fourth_param in {120, 121}: 
        armor_type = "Armure donnée" if fourth_param == 120 else "Armure reçue"
        if params_list[2] is not None:
            formated_params.values = int(params_list[0]) + int(params_list[1]) * 50
        else:
            formated_params.values = int(params_list[0])

        if action_id == 40:
            formated_params.fr = f'-{formated_params.values}{strings[120]["fr"]}'
            formated_params.en = f'-{formated_params.values}{strings[120]["en"]}'
        else:
            formated_params.fr = f'{formated_params.values}{strings[120]["fr"]}'
            formated_params.en = f'{formated_params.values}{strings[120]["en"]}'
    return formated_params
    

def interpret_description(action_id:int, params_list:list[int], stat_description:dict[str, str], type_id:int) -> FormatedParams:
    if type_id == 582:
        formated_params = format_flat_stat_gain(action_id, params_list, stat_description)
        return formated_params
    else:
        match int(action_id):
            # add IDS to a dict
            case action_id if action_id in [20, 26, 31, 41, 71, 80, 82, 83, 84, 85, 120, 122, 123, 124, 125, 149, 160, 162, 166, 171, 173, 175, 177, 180, 184, 191, 988, 1052, 1053, 1055, 150, 875, 56, 57, 90, 96, 97, 98, 100, 130, 132, 172, 174, 176, 181, 192, 876, 1056, 1059, 1060, 1061, 1062, 1063]:
                # gain flat
                formated_params = format_flat_stat_gain(action_id, params_list, stat_description)
                return formated_params

            case action_id if action_id in [21]:
                # perte / deboost flat
                formated_params = format_flat_stat_deboost(action_id, params_list, stat_description)
                return formated_params
            
            case action_id if action_id in [1068, 1069]:
                # random mastery / resists
                formated_params = format_random_stat(action_id, params_list)
                return formated_params

            case 2001: 
                # recolte
                formated_params = format_gathering_stat(action_id, params_list)
                return formated_params
                
            case action_id if action_id in [39, 40]:
                # perte avec custom charac2
                formated_params = format_custom_charac(action_id, params_list)
                fourth_param: int = int(params_list[4])
                return formated_params
    return FormatedParams()


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
                            type_id = int(original_item["definition"]["item"]["baseParameters"]["itemTypeId"])
                            formated_params = interpret_description(action_id, params_list, stat_description, type_id)
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
                                            "fr": formated_params.fr,
                                            "en": formated_params.en  
                                        },
                                        "property": formated_params.property,
                                        "values": formated_params.values,
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
        json.dump(new_items, file, ensure_ascii=False, indent=2)  # type: ignore


cli.add_command(format_items)
# cli.add_command(crawl)


if __name__ == '__main__':
    format_items()