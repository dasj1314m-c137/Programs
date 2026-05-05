import json
import utils

def add_response(path, pattern, reponse):
    with open(path, 'a') as f:
        f.write("\n" + pattern + "|" + reponse)

def wadd_file(path, content):
    with open(path, 'a') as f:
        f.write("\n" + content)

def set_var_json(path, key1, key2, value):
    with open(path, 'r') as f:
        data = json.load(f)
    data[key1][key2] = value
    utils.save_json_data(path, data)