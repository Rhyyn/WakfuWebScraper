import json
import os
import re


def replace_elements(input_string, mapping, lang):
    # Regular expression to match placeholders like [el0], [el1], etc.
    pattern = r'\[el(\d+)\]'

    def replace(match):
        el_number = match.group(1)
        placeholder = f'el{el_number}'
        values = mapping.get(placeholder, {})
        return values.get(lang, '')

    # Replace placeholders like [el0], [el1], etc. using the regular expression
    result_string = re.sub(pattern, replace, input_string)
    return result_string


element_mapping = {
    'el0': {'fr': 'Neutre', 'en': 'Neutral'},
    'el1': {'fr': 'Feu', 'en': 'Fire'},
    'el2': {'fr': 'Eau', 'en': 'Water'},
    'el3': {'fr': 'Terre', 'en': 'Earth'},
    'el4': {'fr': 'Air', 'en': 'Air'},
    'el6': {'fr': 'Lumière', 'en': 'Light'},
}
# el0 = fr = Neutre / en = Neutral
# el1 = fr = Feu / en = Fire
# el2 = fr = Eau / en = Water
# el3 = fr = Terre / en = Earth
# el4 = fr = Air / en = Air
# el6 = fr = Lumière / en = Light

actionIds = [130, 132, 1020, 400, 20, 149, 150, 21, 26, 1052, 1053, 31, 160, 1055, 161, 162, 1056, 1061, 166, 39, 168, 41, 1063, 171, 1068, 173, 174, 175, 176, 1069, 304, 177, 180, 172, 181, 184, 56, 57, 191, 192, 832, 71, 40, 80, 2001, 82, 83, 84, 85, 979, 1060, 1059, 42, 90, 988, 96, 97, 98, 1062, 100, 875, 876, 120, 122, 123, 124, 125]

new_actions = {}

with open('actions.json', 'r', encoding='utf-8') as file:
    actions_data = json.load(file)

    for action in actions_data:
        if (
            "definition" in action
            and "description" in action
            and "id" in action["definition"]
            and "effect" in action["definition"]
            and int(action["definition"]["id"]) in actionIds
        ):
            for lang in ["fr", "en"]:
                new_action_format = {
                    "id": action["definition"]["id"],
                    "effect": replace_elements(action["definition"]["effect"], element_mapping, lang)
                }

                if "description" in action:
                    new_description_format = {
                        lang: replace_elements(action["description"].get(lang, ""), element_mapping, lang),
                    }
                else:
                    new_description_format = {lang: ""}

                if new_action_format["id"] not in new_actions:
                    new_actions[new_action_format["id"]] = {
                        "definition": new_action_format,
                        "description": new_description_format
                    }
                else:
                    new_actions[new_action_format["id"]]["definition"]["effect"] = new_action_format["effect"]
                    new_actions[new_action_format["id"]]["description"][lang] = new_description_format[lang]

with open("actions_refactored.json", 'w', encoding='utf-8') as file:
    json.dump(list(new_actions.values()), file, ensure_ascii=False, indent=2)