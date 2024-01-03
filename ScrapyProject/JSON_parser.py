import json
import math
import re

# Load the items JSON file
with open('items.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


# Filter items with definition.item.baseParameters.itemTypeId equal to 120
# filtered_items = [item['definition']['item']['id'] for item in data if
#                   item.get('definition', {}).get('item', {}).get('baseParameters', {}).get('itemTypeId') in [812]]

# Filter items with definition.item.baseParameters.itemTypeId equal to 120
# filtered_items = [item['definition']['item']['id'] for item in data if
#                   any('equipEffects' in item['definition'] and any('actionId' in effect['effect']['definition'] and effect['effect']['definition']['actionId'] == 1083 for effect in item['definition']['equipEffects']) for item in data)]

# print equip_effect based on ID 
# equip_effects_items = [
#     item['definition']['item']['id']
#     for item in data
#     if 'equipEffects' in item['definition'] and any(
#         'actionId' in effect['effect']['definition'] and effect['effect']['definition']['actionId'] == 1068
#         for effect in item['definition']['equipEffects']
#     )
# ]
# # Print the filtered item IDs
# print(equip_effects_items)


# same as above but different 

# equip_effects_items = [
#     {
#         'id': item['definition']['item']['id'],
#         'params': effect['effect']['definition']['params']
#     }
#     for item in data
#     for effect in item['definition']['equipEffects']
#     if effect['effect']['definition']['actionId'] == 39
# ]

# for item in equip_effects_items:
#     print(f"Item ID: {item['id']}")
#     print(f"Params: {item['params']}")
#     print()
    

## LEVLE
# equip_effects_items = [
#     {
#         'id': item.get('definition', {}).get('item', {}).get('id', ''),
#         'effects': [
#             effect.get('effect', {})
#             for effect in item.get('definition', {}).get('equipEffects', [])
#         ]
#     }
#     for item in data
#     if item.get('definition', {}).get('item', {}).get('baseParameters', {}).get('itemTypeId', '') == 582
# ]

# for item in equip_effects_items:
#     print(item)



for item in data:
    if item['definition']['equipEffects']:
        equip_effects = item['definition']['equipEffects']
        if item['definition']['item']['baseParameters']['itemTypeId'] == 582:
            for effect in equip_effects:
                if effect['effect']['definition']['actionId'] in [39]:
                    fourth_param = effect['effect']['definition']['params'][4]
                    # if fourth_param not in [121.0]: #type: ignore
                    print("---------------------")
                    print(f"Item ID : {item['definition']['item']['id']}")
                    print(f"Effect : ")
                    print(f"actionId = {effect['effect']['definition']['actionId']}")
                    print(f"params = {effect['effect']['definition']['params']}")
                    print(f"4th param = {effect['effect']['definition']['params'][4]}")
                    description = effect['effect'].get('description', None)
                    if description is not None:
                        print(f"description = {description}")
                    else:
                        print("No description available")







# equip_effects_items_params = [
#     item['definition']['item']['id']
#     for item in data
#     if 'equipEffects' in item['definition'] and any(
#         'actionId' in effect['effect']['definition'] and
#         effect['effect']['definition']['actionId'] == 304 and
#         int(effect['effect']['definition']['params'][3]) == 1.0
#         for effect in item['definition']['equipEffects']
#     )
# ]
# # Print the filtered item IDs
# print(equip_effects_items_params)


# ACTIONS IDS
# all_action_ids = set()

# for item in data:
#     if 'equipEffects' in item['definition']:
#         for effect in item['definition']['equipEffects']:
#             if 'effect' in effect and 'definition' in effect['effect'] and 'actionId' in effect['effect']['definition']:
#                 action_id = effect['effect']['definition']['actionId']
#                 all_action_ids.add(action_id)

# # Convert the set to a list if needed
# all_action_ids_list = list(all_action_ids)

# print("All unique actionIds:", all_action_ids_list)


# Load the monstersURL JSON file
# with open('monstersURL.json', 'r', encoding='utf-8') as file:
#     monsters = json.load(file)
# monsters_ids = []
# for monster in monsters:
#     # monster_id = monster['href'].split("/")[-1]
#     match = re.search(r'\d+', monster["href"])
#     if match:
#         monster_id = match.group()
#         monsters_ids.append(monster_id)

# with open('monsters_IDs.json', 'w') as json_file:
#     json.dump(monsters_ids, json_file)

# print(monsters_ids)







# filtered_ids = [item
#                 for item in data if
#                 item.get('definition', {}).get('item', {}).get('id', {}) == 30924]

# print(filtered_ids)


# ids = [2037, 2058, 2198, 3812, 3833, 3849, 3941, 3959, 4615, 5197, 5580, 6121, 6556, 6570, 6571, 7041, 7055, 7056, 9243, 9252, 9274, 9354, 9359, 9362, 9370, 9376, 9963, 9966, 9969, 9971, 10264, 10274, 10564, 11632, 12183, 12184, 12185, 12186, 12187, 12576, 12601, 12624, 12637, 12836, 12896, 13582, 14039, 14119, 14120, 14279, 14281, 14282, 14283, 14361, 14429, 14437, 14485, 14642, 14644, 14647, 14648, 14649, 14650, 14651, 14656, 14661, 14662, 14663, 14716, 14829, 14880, 14881, 14889, 15031, 15033, 15161, 15212, 15215, 15405, 15740, 16038, 16085, 16117, 16119, 16139, 16764, 16773, 16821, 16825, 16826, 17236, 17243, 17284, 17312, 17314, 17345, 17347, 17350, 17488, 17533, 17732, 17733, 17736, 17737, 17792, 17818, 17856, 18171, 18180, 18284, 18445, 18446, 18447, 18448, 18449, 18561, 18563, 18566, 18633, 18769, 19037, 19061, 19130, 19141, 19146, 19242, 19243, 19246, 19248, 19249, 19356, 19453, 19454, 19518, 19519, 19520, 19884, 19899, 20198, 20199, 20200, 20222, 20223, 20224, 20402, 20567, 20569, 20790, 20978, 20987, 20988, 21165, 21169, 21204, 21254, 21443, 21480, 21486, 21487, 21497, 21506, 21507, 21537, 21539, 21564, 21585, 21588, 21727, 21761, 21807, 21809, 21928, 21929, 21930, 21992, 21993, 21994, 22007, 22008, 22205, 22222, 22242, 22243, 22244, 22245, 22246, 22247, 22362, 22364, 22394, 22407, 22408, 22409, 22630, 22647, 22648, 22662, 22663, 22695, 22696, 22697, 22698, 22712, 22713, 22714, 22719, 22720, 22736, 22753, 22754, 22779, 22780, 22839, 22840, 22873, 22874, 22881, 22893, 22894, 22895, 22910, 22916, 22990, 23007, 23008, 23009, 23031, 23032, 23067, 23068, 23071, 23072, 23126,
#        23127, 23171, 23189, 23241, 23242, 23254, 23259, 23300, 23304, 23316, 23320, 23351, 23353, 23365, 23380, 23381, 23382, 23496, 23530, 23568, 23572, 23596, 23625, 23626, 23653, 23828, 24001, 24006, 24010, 24011, 24012, 24015, 24020, 24024, 24025, 24026, 24051, 24301, 24324, 24339, 24355, 24626, 24627, 24628, 24629, 24630, 24631, 24632, 24644, 24645, 24646, 24647, 24648, 24649, 24660, 24661, 24662, 24663, 24664, 24665, 24666, 24667, 24678, 24679, 24680, 24681, 24688, 24689, 24690, 24691, 24692, 24693, 24694, 24718, 24724, 24729, 24799, 24805, 24822, 24830, 25069, 25275, 25276, 25307, 25308, 25326, 25330, 25359, 25360, 25372, 25391, 25392, 25403, 25455, 25457, 25458, 25487, 25497, 25641, 25642, 25643, 25661, 25662, 25663, 25664, 25665, 25666, 25784, 25785, 25786, 25902, 25903, 25904, 25929, 25930, 25986, 25987, 25988, 25995, 25996, 26007, 26008, 26263, 26265, 26266, 26295, 26316, 26494, 26495, 26496, 26497, 26530, 26531, 26545, 26546, 26593, 26609, 26635, 26636, 26637, 26638, 26639, 26640, 26815, 26816, 26861, 26862, 26863, 26913, 26914, 26915, 26957, 26958, 26978, 26979, 26980, 26981, 26982, 26983, 26984, 26988, 26989, 26990, 27022, 27023, 27299, 27300, 27371, 27372, 27377, 27378, 27622, 27623, 27624, 27680, 27681, 27682, 27741, 27742, 27743, 27744, 27799, 27800, 27801, 27802, 28078, 28079, 28088, 28194, 28195, 28202, 28203, 28240, 28241, 28255, 28256, 29297, 29298, 29473, 29474, 29483, 29484, 29487, 29488, 29622, 29623, 29630, 29631, 29638, 29639, 29640, 29641, 29642, 29643, 29823, 29825, 29826, 29828, 29829, 29861, 30146, 30215, 30216, 30227, 30328, 30329, 30330, 30429, 30703, 30913]
# scrap_per_min = 16

# time_to_scrap = 0

# print("Numbers of url to crawl : ", len(ids))
# if math.ceil(len(ids) / scrap_per_min) > 100:
#     min = len(ids) / scrap_per_min
#     h = min//60
#     m = min % 60
#     if h > 1:
#         print("Estimated time of scrapping :", h,"hrs", m,"mn")
#     else:
#         print("Estimated time of scrapping :", h,"hr", m,"mn")
# else:
#     print("Estimated time of scrapping : ", math.ceil(len(ids) / scrap_per_min), "mn")


# for item in filtered_items:
#     print(item)

# 29942


# Items :
#   Armes :
# 	Arme a 1 main : 254, 108, 110, 115, 113 / Type is : 254,108,110,115,113| After Loop - usedIds: (10) [175, 26, 150, 20, 173, 875, 1068, 160, 31, 41]
# 	Arme a 2 main : 223, 114, 101, 111, 253, 117 / Type is : 223,114,101,111,253,117| After Loop - usedIds: (9) [150, 173, 20, 175, 1068, 31, 160, 191, 875]
# 	Seconde main : 112, 189  / Type is : 112,189| After Loop - usedIds: (9) [20, 120, 41, 150, 175, 173, 149, 180, 1068]
#   Armures :
# 	Amulette : 120 / Type is : 120| After Loop - usedIds: (10) [31, 20, 71, 150, 175, 173, 168, 120, 1068, 26]
# 	Anneau : 103 / Type is : 103| After Loop - usedIds: (11) [20, 120, 175, 2001, 149, 1052, 26, 173, 1020, 304, 1068]
# 	Bottes : 119 / Type is : 119| After Loop - usedIds: (7) [20, 173, 80, 41, 120, 175, 84]
# 	Cape : 132 / Type is : 132| After Loop - usedIds: (7) [31, 20, 120, 150, 173, 1068, 175]
# 	Casque : 134 / Type is : 134| After Loop - usedIds: (9) [175, 20, 1068, 160, 120, 173, 875, 80, 150]
# 	Ceinture : 133 / Type is : 133| After Loop - usedIds: (10) [184, 20, 120, 150, 175, 80, 173, 31, 1052, 180]
# 	Epaulettes : 138 / Type is : 138| After Loop - usedIds: (9) [150, 20, 120, 123, 175, 173, 875, 1068, 184]
# 	Plastron : 136 / Type is : 136| After Loop - usedIds: (8) [20, 875, 173, 184, 175, 1052, 1068, 26]

# usedActionsIds : 175,26,150,20,173,875,1068,160,31,41,191,120,149,180,71,168,2001,1052,1020,304,80,84,184,123


# check 2001, 1020, 304

#   Sublimation : 812
#   Emblemes : 646
#   Familier : 582
#   Montures : 611

# Torches : 480
# Costumes : 647
# Outils : 537


