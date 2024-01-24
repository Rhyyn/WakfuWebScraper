import json
from math import e
import os


project_dir = os.path.abspath(os.getcwd())
static_data_dir_path = os.path.join(project_dir, '..', 'StaticData')
subset_data_dir_path = os.path.join(project_dir, '..', 'SubsetDataForTests')
items_data_file_path = os.path.join(static_data_dir_path, 'items.json')
monsters_data_file_path = os.path.join(project_dir, '..', 'ScrapedData', 'ScrappedFiles', 'ScrappedMonsters', 'en_monsters_stats_data.json')

def get_subset_items_data(amountWanted):
    with open(items_data_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    subset_data = data[amountWanted]
    try:
        with open('subset_items.json', 'w', encoding='utf-8') as new_file:
            json.dump(subset_data, new_file, ensure_ascii=False, indent=2)
        print("Subset of items.json written to /SubsetDataForTests/subset_items.json.")
    except Exception as e:
        print("Failed to get subset of items : ", str(e))
        return False
    finally:
        return True
    

def get_subset_monsters_data(amountWanted):
    with open(monsters_data_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    subset_data = data[amountWanted]
    try:
        with open('subset_monsters.json', 'w', encoding='utf-8') as new_file:
            json.dump(subset_data, new_file, ensure_ascii=False, indent=2)
        print("Subset of items.json written to /SubsetDataForTests/subset_monsters.json.")
    except Exception as e:
        print("Failed to get subset of monsters : ", str(e))
        return False
    finally:
        return True

