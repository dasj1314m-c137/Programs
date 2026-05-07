import json
import utils
import os
from pathlib import Path

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

def rm_MD_block(path, heading, delimiter="## "):
    path = Path(path)
    tmp_path = path.with_suffix('.tmp')
    match = False
    # print(f"Attempting to remove block with heading '{heading}' and delimiter '{delimiter}' from file: {path}")
    try:
        with path.open('r') as f_in, tmp_path.open('w') as f_out:
            skip = False
            for line in f_in:
                if line.startswith(delimiter + heading):
                    skip = True
                    match = True
                    continue
                elif skip and line.startswith(delimiter):
                    skip = False
                    f_out.write(line)
                    continue
                if not skip:
                    f_out.write(line)
        if not match:
            tmp_path.unlink()
            return False
        os.replace(tmp_path, path)
        return True
    except Exception as e:
        print(f"Error occurred while removing MD block: {e}")
        if tmp_path.exists():
            tmp_path.unlink()
        return None