import os
import shutil

project_dir = os.path.abspath(os.getcwd())
formated_data_folder = os.path.join(project_dir, '..', 'ScrapedData', 'FormatedData')
prefix_formated_data_folder = os.path.join(project_dir, '..', 'ScrapedData', 'FormatedDataFilesPrefixOnly')
formated_json_files = []

def get_prefix(file_name):
    return file_name.split('_')[0]

for file in os.listdir(formated_data_folder):
    if file.endswith('.json') and file.__contains__("_scraped_data_formated"):
        old_file = os.path.join(formated_data_folder, file)
        newName = get_prefix(file) + ".json"
        new_file = os.path.join(prefix_formated_data_folder, newName)
        print(file, " copied to : ", new_file)
        shutil.copy2(old_file, new_file)
