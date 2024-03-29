import os
import json
import click
import re
import typing
from typing import Any, Union, List, Dict, Type, Optional


# TODO : fix :
#             "pluriels"

@click.group()
def cli():
    pass


@click.command()
def format_items():
    blacklist = ['items.json', 'formated-items.json', 'actions.json']
    current_directory = os.getcwd()
    formated_data_path = os.path.join(current_directory, "FormatedData")
    scraped_items_data_path = os.path.join(current_directory, "ScrapedFiles", "ScrapedItems")
    json_files = []
    for file in os.listdir(scraped_items_data_path):
        if file.endswith('.json'):
            json_files.append(file)


    formated_json_files = []
    for file in os.listdir(formated_data_path):
        if file.endswith('.json'):
            formated_json_files.append(file)

    if not json_files:
        click.echo("No JSON files found in the current directory.")
        return
    
    def get_prefix(file_name):
        return file_name.split('_')[0]
    
    click.echo(f"Available files to format: ")
    for file in json_files:
        formated_file = re.sub('.json', '_formated.json', file)
        if (formated_file in formated_json_files) and (file not in blacklist):
            click.echo(f" - {get_prefix(file)} - !! already exists in FormatedData !!")
        elif file not in blacklist:
            click.echo(f" - {get_prefix(file)}")

    selected_prefix = click.prompt("Enter the prefix of the file to format", 
                                    type=click.Choice(list(map(get_prefix, json_files)),
                                    case_sensitive=False), 
                                    show_choices=False)
    
    selected_file = ''
    for file in json_files:
        if get_prefix(file) == selected_prefix:
            selected_file = file

    if selected_file not in json_files:
        click.echo(f"Error: File '{selected_file}' not found.")
        return


    try:
        format_json(selected_file)
        click.echo(f"File '{selected_file}' formatted successfully.")
    except Exception as e:
        click.echo(f"Error while formatting File '{selected_file}' :")
        click.echo(str(e))



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

class FormatedParams:
    defId:int = 0
    fr:str = ''
    en:str = ''
    property:int = 0
    values:int = 0
    job_id:Optional[int]
    droprates:Optional[dict]
    value:int = 0
    random_element:Optional[int] = 0
    stat_string_fr:str = ''
    stat_string_en:str = ''
    stat_string_value:str = ''


def replace_element(match: re.Match, lang_key) -> str:
    element_key = match.group(1)
    if element_key in element_mapping:
        return element_mapping[element_key][lang_key]
    
    return match.group(0)

def starts_with_hyphen(s):
    pattern = re.compile(r'^-')
    return bool(pattern.match(s))


def check_return_values(params_list:list[int]) -> int:
    if len(params_list) >= 3 and params_list[2] is not None: 
        return int(params_list[0]) + (int(params_list[1]) * 50)
    else:
        return int(params_list[0])


def format_flat_stat_gain(action_id:int, params_list:list[int], stat_description:dict[str, str]) -> FormatedParams:
    formated_params = FormatedParams()
    value = check_return_values(params_list)
    formated_params.value = value
    formated_params.property = action_id
    for lang_key, lang_description in stat_description.items():
        if lang_key in ['fr', 'en'] and isinstance(lang_description, str):
            updated_description = re.sub(r'\[#1\]', str(value), lang_description)
            updated_description = element_pattern.sub(lambda match: replace_element(match, lang_key), updated_description)

            # This separates the value from the stat string
            # Aswell as separating the special characters such as - or % 
            # From the value 
            match = re.search(r'([^\d]?)' + re.escape(str(value)) + r'([^\d]?)', updated_description)
            
            if match:
                prefix, suffix = match.groups()
                value_str = f"{prefix}{value}{suffix}"
                new_value = value
                if prefix:
                    new_value = (value) - (value * 2)
                
                updated_description_without_value = updated_description.replace(value_str, "").strip()
                
                setattr(formated_params, 'stat_string_' + lang_key, updated_description_without_value)
                setattr(formated_params, 'value', new_value)
                setattr(formated_params, 'stat_string_value', value_str.strip())
                setattr(formated_params, lang_key, updated_description)
            else:
                setattr(formated_params, 'stat_string_' + lang_key, 'Error parsing flat_stat_gain')
                setattr(formated_params, 'value', None)
                setattr(formated_params, lang_key, updated_description.strip())

    return formated_params


def format_flat_stat_deboost(action_id:int, params_list:list[int], stat_description:dict[str, str]) -> FormatedParams:
    formated_params = FormatedParams()
    value = check_return_values(params_list)
    value = (value) - (value * 2)
    formated_params.value = value
    formated_params.property = action_id
    formated_params.fr = f'-{int(params_list[0])} PV'
    formated_params.en = f'-{int(params_list[0])} HP'
    formated_params.stat_string_fr = 'PV'
    formated_params.stat_string_en = 'HP'
    formated_params.stat_string_value = f'-{str(int(params_list[0]))}'
    return formated_params


def format_random_stat(action_id:int, params_list:list[int]) -> FormatedParams:
    formated_params = FormatedParams()
    value = check_return_values(params_list)
    formated_params.value = value
    formated_params.stat_string_value = str(value)
    formated_params.property = action_id
    strings = {
        1068 : {
            0: {
                'fr' : '[#1] Maîtrise dans [#2] élément aléatoire',
                'en' : '[#1] Mastery in [#2] random element'
            },
            1: {
                'fr' : '[#1] Maîtrise dans [#2] éléments aléatoires',
                'en' : '[#1] Mastery in [#2] random elements'
            }
        },
        1069 : {
            0: {
                'fr' : '[#1] Résistances dans [#2] élément aléatoire',
                'en' : '[#1] Resistance in [#2] random element'
            }, 
            1 : {
                'fr' : '[#1] Résistance dans [#2] éléments aléatoires',
                'en' : '[#1] Resistance in [#2] random elements'
            }
        }
    }
    if int(params_list[2]) == 1 :
        formated_params.fr = strings[action_id][0]['fr'].replace('[#1]', str(int(params_list[0]))).replace('[#2]', str(int(params_list[2])))
        formated_params.en = strings[action_id][0]['en'].replace('[#1]', str(int(params_list[0]))).replace('[#2]', str(int(params_list[2])))
        formated_params.stat_string_fr = formated_params.fr.split(' ', 1)[1]
        formated_params.stat_string_en = formated_params.en.split(' ', 1)[1]
        formated_params.random_element = int(params_list[2])
    else :
        formated_params.fr = strings[action_id][1]['fr'].replace('[#1]', str(int(params_list[0]))).replace('[#2]', str(int(params_list[2])))
        formated_params.en = strings[action_id][1]['en'].replace('[#1]', str(int(params_list[0]))).replace('[#2]', str(int(params_list[2])))
        formated_params.stat_string_fr = formated_params.fr.split(' ', 1)[1]
        formated_params.stat_string_en = formated_params.en.split(' ', 1)[1]
        formated_params.random_element = int(params_list[2])
    return formated_params


def format_gathering_stat(action_id:int, params_list:list[int]) -> FormatedParams:
    # 2% + (niv du familier + multiplicateur) = total %
    # 2% + (25 * 0.16 )% = 6%
    formated_params = FormatedParams()
    value = check_return_values(params_list)
    formated_params.value = value
    formated_params.stat_string_value = str(value) + "%"
    formated_params.property = action_id
    if int(params_list[2]):
        formated_params.job_id = int(params_list[2])
        formated_params.fr = '[#1]% Quantité Récolte en [#2]'.replace('[#1]', str(int(params_list[0]))).replace('[#2]', jobs[str(formated_params.job_id)]['fr'])
        formated_params.en = '[#1]% Harvesting Quantity in [#2]'.replace('[#1]', str(int(params_list[0]))).replace('[#2]', jobs[str(formated_params.job_id)]['en'])
        formated_params.stat_string_fr = formated_params.fr.split(' ', 1)[1]
        formated_params.stat_string_en = formated_params.en.split(' ', 1)[1]
    else:
        formated_params.fr = '[#1]% Quantité Récolte'.replace('[#1]', str(int(params_list[0])))
        formated_params.en = '[#1]% Harvesting Quantity'.replace('[#1]', str(int(params_list[0])))
        formated_params.stat_string_fr = formated_params.fr.split(' ', 1)[1]
        formated_params.stat_string_en = formated_params.en.split(' ', 1)[1]
    return formated_params


def format_old_deboost(action_id:int, params_list:list[int]) -> FormatedParams:
    formated_params = FormatedParams()
    value = check_return_values(params_list)
    newValue = (value) - (value * 2)
    match int(action_id):
        case action_id if action_id in [42]:
            formated_params.value = newValue
            formated_params.stat_string_value = str(newValue)
            formated_params.fr = '-[#1] PM max'.replace('[#1]', str(value))
            formated_params.en = '-[#1] max MP'.replace('[#1]', str(value))
            formated_params.stat_string_fr = formated_params.fr.split(' ', 1)[1].strip()
            formated_params.stat_string_en = formated_params.en.split(' ', 1)[1].strip()
            formated_params.property = 57
    return formated_params


def format_custom_charac(action_id:int, params_list:list[int]) -> FormatedParams:
    # only works for Armor, lack the IDs for more stats support
    # may lead to undesirable behavior
    # subject to crash
    formated_params = FormatedParams()
    value = check_return_values(params_list)
    formated_params.value = value
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
    if fourth_param in {120, 121}: 
        if params_list[2] is not None:
            formated_params.value = int(params_list[0]) + int(params_list[1]) * 50
        else:
            formated_params.value = int(params_list[0])

        if action_id == 40:
            formated_params.fr = f'-{formated_params.value}{strings[fourth_param]["fr"]}'
            formated_params.en = f'-{formated_params.value}{strings[fourth_param]["en"]}'
            formated_params.stat_string_fr = formated_params.fr.split(' ', 1)[1].strip()
            formated_params.stat_string_en = formated_params.en.split(' ', 1)[1].strip()
            formated_params.value = value - (value * 2)
        else:
            formated_params.fr = f'{formated_params.value}{strings[fourth_param]["fr"]}'
            formated_params.en = f'{formated_params.value}{strings[fourth_param]["en"]}'
            formated_params.stat_string_fr = formated_params.fr.split(' ', 1)[1].strip()
            formated_params.stat_string_en = formated_params.en.split(' ', 1)[1].strip()
    formated_params.stat_string_value = str(formated_params.value) + "%"
    return formated_params
    
gain_flat_ids = [20, 26, 31, 41, 71, 80, 82, 83, 84, 85, 120, 122, 123, 124, 125, 149, 160, 161, 162, 166, 168, 171, 173, 175, 177, 180, 184, 191, 988, 1052, 1053, 1055, 150, 875, 56, 57, 90, 96, 97, 98, 100, 130, 132, 172, 174, 176, 181, 192, 876, 1056, 1059, 1060, 1061, 1062, 1063, 979]

def interpret_description(action_id:int, params_list:list[int], stat_description:dict[str, str], type_id:int, name) -> FormatedParams:
    if type_id == 582 and int(action_id) != 2001:
        formated_params = format_flat_stat_gain(action_id, params_list, stat_description)
        return formated_params
    else:
        match int(action_id):
            case action_id if action_id in gain_flat_ids:
                # flat gain / gain flat
                formated_params = format_flat_stat_gain(action_id, params_list, stat_description)
                return formated_params

            case action_id if action_id in [21]:
                # deboost flat / perte
                formated_params = format_flat_stat_deboost(action_id, params_list, stat_description)
                return formated_params
            
            case action_id if action_id in [1068, 1069]:
                # random mastery / resists
                formated_params = format_random_stat(action_id, params_list)
                return formated_params

            case 2001: 
                # gathering / recolte
                formated_params = format_gathering_stat(action_id, params_list)
                return formated_params
                
            case action_id if action_id in [39, 40]:
                # custom stat in param
                formated_params = format_custom_charac(action_id, params_list)
                return formated_params
            case action_id if action_id in [42]:
                formated_params = format_old_deboost(action_id, params_list)
                return formated_params
            case _:
                print(action_id, " not supported")
                print(name)
                print(stat_description)
                print(params_list)

    return FormatedParams()

def format_droprates(en_monsters_data, scraped_droprates):
    formated_params = FormatedParams()
    droprates = {"fr": {}, "en": {}}
    en_monsters_dict = {str(monster.get('monster_id')): monster for monster in en_monsters_data}

    for fr_monster_name, fr_data in scraped_droprates.items():
        drop_rate = fr_data.get("drop_rate")
        monster_id = str(fr_data.get("monster_id", None)) 
        droprates["fr"][fr_monster_name] = {"drop_rate": drop_rate, "monster_id": monster_id}
        en_monster = en_monsters_dict.get(monster_id)
        if en_monster:
            en_monster_name = en_monster.get('monster_name', fr_monster_name)
        else:
            en_monster_name = fr_monster_name

        droprates["en"][en_monster_name] = {"drop_rate": drop_rate, "monster_id": monster_id}

    formated_params.droprates = droprates
    return formated_params


def format_json(filename):
    current_directory = os.getcwd()
    scraped_items_data_path = os.path.join(current_directory, "ScrapedFiles", "ScrapedItems", f'{filename}')
    scraped_monsters_data_path = os.path.join(current_directory, "ScrapedFiles", "ScrapedMonsters", "en_monsters_stats_data.json")
    static_items = os.path.join(current_directory, "..","StaticData", "items.json")
    static_actions = os.path.join(current_directory, "..","StaticData", "actions.json")
    with open(scraped_items_data_path, 'r', encoding='utf-8') as scraped_file:
        scraped_data = json.load(scraped_file)

    with open(static_items, 'r', encoding='utf-8') as all_items_file:
        all_items_data = json.load(all_items_file)

    with open(static_actions, 'r', encoding='utf-8') as stats_file:
        actions_data = json.load(stats_file)

    with open(scraped_monsters_data_path, 'r', encoding='utf-8') as monster_file:
        en_monsters_data = json.load(monster_file)

    

    new_items = []
    
    for scraped_item in scraped_data:
        for original_item in all_items_data:
            if int(scraped_item["item"]["id"]) == int(original_item["definition"]["item"]["id"]):
                new_item_format = {
                    "title": {
                        "fr": original_item["title"]["fr"],
                        "en": original_item["title"]["en"]
                    },
                    "description": {
                        "fr": original_item.get("description", {}).get("fr", ""),
                        "en": original_item.get("description", {}).get("en", "")
                    },
                    "droprates": scraped_item["droprates"],
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
                    "item_url": str(scraped_item["item_url"])
                }


                scraped_droprates = scraped_item["droprates"]
                drop_rates = format_droprates(en_monsters_data,scraped_droprates)
                new_item_format["droprates"] = drop_rates.droprates


                if "equipEffects" in original_item["definition"]:
                    for effect_entry in original_item["definition"]["equipEffects"]:
                        if "effect" in effect_entry:
                            effect_definition = effect_entry["effect"].get(
                                "definition", {})
                            type_id = int(original_item["definition"]["item"]["baseParameters"]["itemTypeId"])
                            params_list:list[int] = effect_definition.get("params", [])
                            action_id:int = effect_definition.get("actionId", "")
                            action_desc:dict[str, dict] = {}
                            for action in actions_data:
                                if action["definition"]["id"] == action_id:
                                    action_desc = action
                            stat_description:dict[str, str] = action_desc.get(
                                "description", {})
                            def_id = effect_definition.get("id", "")
                            formated_params = interpret_description(action_id, params_list, stat_description, type_id, original_item["title"]["fr"])
                            formated_params.defId = def_id
                            modified_effect_entry = {
                                "effect": {
                                    "definition": {
                                        "id": formated_params.defId,
                                    },
                                    "stats": {
                                        "display": {
                                            "fr": formated_params.fr,
                                            "en": formated_params.en,  
                                        },
                                        "stat_string_desc": {
                                              "fr": formated_params.stat_string_fr,
                                              "en": formated_params.stat_string_en
                                        },
                                        "stat_string_value": formated_params.stat_string_value,
                                        "property": formated_params.property,
                                        "value": formated_params.value,
                                        
                                    }
                                }
                            }
                            if formated_params.random_element != 0:
                                modified_effect_entry["effect"]["stats"]["random_element"] = formated_params.random_element
                            new_item_format["equipEffects"].append(modified_effect_entry)
                new_items.append(new_item_format)

    filename = re.sub('.json', '', filename)
    file_path = os.path.join(os.path.dirname(os.path.realpath(
        __file__)), 'FormatedData', f'{filename}_formated.json')
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(new_items, file, ensure_ascii=False, indent=2)  # type: ignore


cli.add_command(format_items)


if __name__ == '__main__':
    format_items()