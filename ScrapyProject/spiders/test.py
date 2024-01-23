import os


current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
static_data_dir_path = os.path.join(parent_dir, 'StaticData')
items_json_path = os.path.join(static_data_dir_path, 'items.json')


print(static_data_dir_path)
print(parent_dir)