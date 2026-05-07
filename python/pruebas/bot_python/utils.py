import json
import render

def dic_index(dic, index):
    for i, key in enumerate(dic.items()):
        if i == index:
            return key

def list_view(list_content):
    for i, item in enumerate(list_content, 1):
        render.smooth_print(f"{i}. {item}")
    return None

def save_json_data(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def linkHeading_md(md_name, heading_name):
    return f"[[{md_name}#{heading_name}]]"

if __name__ == "__main__":
    list_test = ["item1", "item2", "item3"]
    list_view(list_test)