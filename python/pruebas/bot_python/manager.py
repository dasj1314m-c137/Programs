import ask
import render
import search
import write_files
import utils
from datetime import date

def match_response(action):
    mood = ask.open_question(action["prompt"])
    response = search.read_p(action["path"], mood)
    render.show_match(response, action["path"])
    return True

def writing_files(action):
    response = ask.questionSN(action["prompt"])
    if response:
        d = date.today()
        writing = ask.open_question("Escribe: ")
        if writing == "exit":
            return None
        write_files.wadd_file(action["path"], str(d) + "\n" + writing)
        return True

def duesMD_render(action):
    dues = ask.questionSN("¿Quieres ver tus pendientes?")
    if dues:
        render.smooth_print(action["prompt"])
        choice = list_dues(action["path"])
        if choice is None:
            return None
        path = search.locate_get_file("/home/dasj/documents/works/obsidian_vault/dues/", choice[1][0])
        content = search.getMD_block(path, choice[1][1])
        render.smooth_print(choice[1][2].strip() + "\n" + content.strip())

def list_dues(path):
    with open(path, 'r') as f:
        tasks = {}
        for line in f:
            key, value = search.getNH_md(line.strip())
            tasks[key] = value
        choice = ask.select_option(list(tasks.keys()), ask_select=False)
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
        utils.save_json_data("data/data.json", data)

def check_status_json(func, action):
    status = search.get_json_value("data/data.json", "daily_status", action["json_key"])
    if status:
        return None
    else:
        result = func()
        if result is None:
            return None
        write_files.set_var_json("data/data.json", "daily_status", action["json_key"], True)

def add_due(action):
    while True:
        name_file = ask.open_question("Escribe nombre del archivo donde quieres agregar el pendiente: ")
        path_file = search.locate_get_file("/home/dasj/documents/works/obsidian_vault/dues/", name_file + ".md")
        if not path_file:
            render.smooth_print("Archivo no encontrado.")
            files = search.locate_files_suffix("/home/dasj/documents/works/obsidian_vault/dues/", ".md")
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
    link_due = utils.linkHeading_md(title_due, name_file)
    link_due = link_due + " " + date_due
    new_due = f"## {title_due}\n{content_due}"
    write_files.wadd_file(path_file, new_due)
    write_files.wadd_file(action["path"], link_due)
    render.smooth_print("Pendiente agregado exitosamente.")

def rm_due(action):
    while True:
        render.smooth_print("Selecciona el pendiente que quieres eliminar: ")
        choice = list_dues(action["path"])
        if choice is None:
            return None
        # estructura del choice: (all, [file.md, heading, date]) p.ej.
        # ('recursos_socioemocionales Triptico Infografia Tabla  miercoles 6 mayo', ['recursos_socioemocionales.md', 'Triptico Infografia Tabla', ' miercoles 6 mayo'])
        path_file = search.locate_get_file("/home/dasj/documents/works/obsidian_vault/dues/", choice[1][0])
        link = utils.linkHeading_md(choice[1][0].replace(".md", ""), choice[1][1])
        complete_rm = ask.questionSN(f"¿Quieres eliminar el pendiente '{choice[1][1]}' del archivo '{choice[1][0]}'?")
        if not complete_rm:
            return None
        rm_link = write_files.rm_MD_block(action["path"], link[2:], "[[")
        rm_due = write_files.rm_MD_block(path_file, choice[1][1])
        if not rm_due or not rm_link:
            render.smooth_print("Sin coincidencias en el archivo del pendiente o en el archivo de links")
            return None
        render.smooth_print("Pendiente eliminado exitosamente.")
        return True

def dues_manager(action):
    while True:
        do_act = ask.questionSN(action["prompt"])
        if not do_act:
            return None
        render.smooth_print("¿Qué quieres hacer?")
        act = ask.select_option(["Agregar pendiente", "Eliminar pendiente"], ask_select=False)
        if not act:
            return None
        if act == 0:
            add_due(action)
        elif act == 1:
            rm_due(action)