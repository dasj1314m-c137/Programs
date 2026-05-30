import json
from pathlib import Path

def search_p(line, pattern):
    responses = line.split("|", 1)
    if not pattern == responses[0]:
        return False
    else:
        return responses[1]

def read_p(path, pattern):
    with open(path, 'r') as f:
        for line in f:
            answer = search_p(line, pattern)
            if answer:
                return answer.strip()
        return False

def getNH_md(content):
    content = content.replace("[", ",").replace("]", ",")
    content = content.replace(",", "", 3)
    content = content.replace("#", ",")
    content = content.split(",")
    key = "-".join(content)
    content[0] = f"{content[0]}.md"
    return key, content

def getMD_block(path, heading):
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        return None
    with open(p, 'r') as f:
        for line in f:
            if line.startswith("## " + heading):
                block = []
                block.append(line)
                for line in f:
                    if line.startswith("## "):
                        break
                    block.append(line)
                return "".join(block)

def get_json_data(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def get_json_value(path, key1, key2):
    with open(path, 'r') as f:
        data = json.load(f)
    return data[key1][key2]

def locate_get_file(main_path, filename):
    main_path = Path(main_path)
    for path in main_path.rglob(filename):
        return path
    return None

def locate_files_suffix(main_path, suffix):
    main_path = Path(main_path)
    files = []
    for path in main_path.rglob(f"*{suffix}"):
        files.append(path)
    for file in files:
        file_name = file.stem
        file_name = file_name.split(".")[0]
        files[files.index(file)] = file_name
    return files
