import ask
import render
import search
import write_files
import utils
from datetime import date
import flet as ft
from pathlib import Path


def resolve_action_path(action):
    path = action["path"]
    if Path(path).exists():
        return None
    resolved_path = search.get_json_value("data/data.json", "actions_paths", path)
    if resolved_path:
        action["path"] = resolved_path
    return None

def match_response(action):
    mood = ask.open_question(action["prompt"])
    response = search.read_p(action["path"], mood)
    render.show_match(response, action["path"])
    return True

def writing_files(action):
    d = date.today()
    writing = ask.open_question("Escribe: ")
    if writing == "exit":
        return None
    write_files.wadd_file(action["path"], str(d) + "\n" + writing)
    render.smooth_print("Archivo escrito correctamente")
    return True

def duesMD_render(action):
    render.smooth_print("Tus pendientes son: ")
    choice = list_dues(action["path"], True)
    if choice is None:
        return None
    # estructura del choice: (all, [file.md, heading, date]) p.ej.
    # ('recursos_socioemocionales Triptico Infografia Tabla  miercoles 6 mayo', ['recursos_socioemocionales.md', 'Triptico Infografia Tabla', ' miercoles 6 mayo'])
    path = search.locate_get_file("/home/dasj/documents/works/obsidian_vault/dues/", choice[1][0])
    content = search.getMD_block(path, choice[1][1])
    render.smooth_print(choice[1][2].strip() + "\n" + content.strip())
    return None

def list_dues(path, ask_select):
    with open(path, 'r') as f:
        tasks = {}
        for line in f:
            key, value = search.getNH_md(line.strip())
            tasks[key] = value
        choice = ask.select_option(list(tasks.keys()), ask_select=ask_select)
        if choice is False:
            return None
        choice = utils.dic_index(tasks, choice)
        return choice

def daily_check():
    data = search.get_json_data("data/data.json")
    today = date.today().strftime("%d/%m/%y")
    if data["metadata"]["last_update"] != today:
        data["metadata"]["last_update"] = today
        for key in data["daily_status"]:
            data["daily_status"][key] = False
        for key in data["times_asked"]:
            data["times_asked"][key] = 0
        utils.save_json_data("data/data.json", data)

def check_status_json(action):
    status = search.get_json_value("data/data.json", "daily_status", action["json_key"])
    if status:
        return None
    else:
        if action["dir_question"]:
            action["func"](action)
            write_files.set_var_json("data/data.json", "daily_status", action["json_key"], True)
        else:
            path = check_actions_path(action)
            resolve_action_path(action)
            if not path:
                return None
            execute = ask.questionSN(action["prompt"])
            write_files.add_counter_json("data/data.json", "times_asked", "daily_status", action["json_key"])
            if execute:
                result = action["func"](action)
                if result:
                    write_files.set_var_json("data/data.json", "daily_status", action["json_key"], True)

def add_due(action):
    dues_file = search.get_json_value("data/data.json", "actions_paths", "dues_file")
    while True:
        while True:
            name_file = ask.open_question("Escribe nombre del archivo donde quieres agregar el pendiente: ")
            path_file = search.locate_get_file(action["path"] + "/", name_file + ".md")
            if not path_file:
                render.smooth_print("Archivo no encontrado.")
                files = search.locate_files_suffix(action["path"] + "/", ".md")
                render.smooth_print("Estos son los archivos disponibles: ")
                for file in files:
                    if file == "dues":
                        continue
                    render.smooth_print(f"- {file}")
                continue
            break
        title_due = ask.open_question("Escribe titulo del pendiente que quieres agregar: ").replace(",", "")
        date_due = ask.open_question("Escribe fecha del pendiente que quieres agregar (Dia, 00, Mes): ")
        content_due = ask.open_question("Escribe contenido del pendiente que quieres agregar: ")
        link_due = utils.linkHeading_md(name_file, title_due)
        link_due = link_due + " " + date_due
        new_due = f"## {title_due}\n{content_due}"
        complete_add = ask.questionSN(f"¿Quieres agregar el pendiente '{title_due}' al archivo '{name_file}.md'?")
        if not complete_add:
            return None
        write_files.wadd_file(path_file, new_due)
        write_files.wadd_file(dues_file, link_due)
        render.smooth_print("Pendiente agregado exitosamente.")
        another = ask.questionSN("¿Quieres agregar otro pendiente?")
        if not another:
            return None

def rm_due(action):
    dues_file = search.get_json_value("data/data.json", "actions_paths", "dues_file")
    while True:
        render.smooth_print("Selecciona el pendiente que quieres eliminar: ")
        choice = list_dues(dues_file, False)
        if choice is None:
            return None
        # estructura del choice: (all, [file.md, heading, date]) p.ej.
        # ('recursos_socioemocionales Triptico Infografia Tabla  miercoles 6 mayo', ['recursos_socioemocionales.md', 'Triptico Infografia Tabla', ' miercoles 6 mayo'])
        path_file = search.locate_get_file(action["path"] + "/", choice[1][0])
        link = utils.linkHeading_md(choice[1][0].replace(".md", ""), choice[1][1])
        complete_rm = ask.questionSN(f"¿Quieres eliminar el pendiente '{choice[1][1]}' del archivo '{choice[1][0]}'?")
        if not complete_rm:
            return None
        rm_link = write_files.rm_MD_block(dues_file, link[2:], "[[")
        rm_due = write_files.rm_MD_block(path_file, choice[1][1])
        if not rm_due or not rm_link:
            render.smooth_print("Sin coincidencias en el archivo del pendiente o en el archivo de links")
            return None
        render.smooth_print("Pendiente eliminado exitosamente.")
        another = ask.questionSN("¿Quieres eliminar otro pendiente?")
        if not another:
            return None

def dues_manager(action):
    render.smooth_print("¿Qué quieres hacer?")
    act = ask.select_option(["Agregar pendiente", "Eliminar pendiente"], ask_select=False)
    if act is None:
        return None
    if act == 0:
        add_due(action)
    elif act == 1:
        rm_due(action)

def terminal_listening(actions):
    funcs = ["exit", "write_day", "show_dues", "modify_dues", "help"]
    while True:
        try:
            standard_input = input("dasj: ")
        except KeyboardInterrupt:
            render.smooth_print("Saliendo...")
            break
        if standard_input in funcs:
            if standard_input == "exit":
                render.smooth_print("Saliendo...")
                break
            elif standard_input == "help":
                render.smooth_print("Comandos posibles")
                utils.list_view(funcs)
                continue
            elif standard_input == "write_day":
                writing_files(actions["write_day"])
            elif standard_input == "show_dues":
                duesMD_render(actions["show_dues"])
            elif standard_input == "modify_dues":
                dues_manager(actions["modify_dues"])
        else:
            render.smooth_print("Comando no reconocido.")

def check_actions_path(action):
    path = search.get_json_value("data/data.json", "actions_paths", action["path"])
    if not path:
        file = "un archivo" if action["path_file"] else "una carpeta"
        act = "eliminar o agregar" if action["json_key"] == "dues_modified" else "revisar"
        render.smooth_print(f"No tenemos {file} para {act} {action['name']}.")
        add_path = ask.questionSN(f"Quieres ingresar una ruta para este {file.split()[1]}?")
        if add_path:
            if action["path_file"]:
                file_picker(action, ".md")
            else:
                folder_picker(action)
        else:
            render.smooth_print("No se podrá realizar la acción sin un archivo asociado.")
            return False
    return True

def file_picker(action, *posfix, multiple=False):
    async def main(page: ft.Page):
        async def handle_pick_file(e):
            picker = ft.FilePicker()
            path = await picker.pick_files(allowed_extensions=posfix, allow_multiple=multiple)
            if path:
                file_path = path[0].path
                write_files.set_var_json("data/data.json", "actions_paths", action["path"], file_path)
            else:
                render.smooth_print("No se seleccionó ningun archivo.")
            await page.window.close()

        button_select = ft.ElevatedButton(content="Seleccionar archivo", on_click=handle_pick_file)
        page.add(button_select)

    ft.app(target=main)

def folder_picker(action):
    async def main(page: ft.Page):
        async def handle_pick_folder(e):
            picker = ft.FilePicker()
            path = await picker.get_directory_path()
            if path:
                folder_path = path
                write_files.set_var_json("data/data.json", "actions_paths", action["path"], folder_path)
            else:
                render.smooth_print("No se seleccionó ninguna carpeta.")
            await page.window.close()

        button_select = ft.ElevatedButton(content="Seleccionar carpeta", on_click=handle_pick_folder)
        page.add(button_select)

    ft.app(target=main)
