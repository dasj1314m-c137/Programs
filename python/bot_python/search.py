import json
from pathlib import Path
import flet as ft
import render

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

async def file_picker(posfix, data_base, multiple=False, prompt="Selecciona un archivo"):
    picker = ft.FilePicker()
    path = await picker.pick_files(dialog_title=prompt, allowed_extensions=posfix, allow_multiple=multiple)
    if path:
        file_path = path[0].path
        data_base.save_file_path(file_path)
        render.smooth_print("Ruta de archivo seleccionada exitosamente")
    else:
        pass

async def folder_picker(data_base, prompt="Selecciona una carpeta"):
    picker = ft.FilePicker()
    # async def main(page: ft.Page):
    path = await picker.get_directory_path(dialog_title=prompt)
    if path:
        folder_path = path
        data_base.save_dir_path(folder_path)
        render.smooth_print("Ruta de carpeta seleccionada exitosamente")
    else:
        pass