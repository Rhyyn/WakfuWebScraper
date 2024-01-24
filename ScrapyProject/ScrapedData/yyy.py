import json
import os
from re import L 


current_directory = os.getcwd()
formated_data_path = os.path.join(current_directory, "FormatedData")
scraped_items_data_path = os.path.join(current_directory, "ScrapedFiles", "ScrapedItems")
static_data_path = os.path.join(current_directory, "StaticData")


json_files = []
for file in os.listdir(scraped_items_data_path):
    if file.endswith('.json'):
        json_files.append(file)

formated_json_files = []

for file in os.listdir(formated_data_path):
    if file.endswith('.json'):
        formated_json_files.append(file)


file_path = os.path.join(os.path.dirname(os.path.realpath(
        __file__)), 'FormatedData', f'test_formated.json')

print(static_data_path)