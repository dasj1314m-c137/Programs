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

# ============================================================================
# FUNCIÓN: match_response → OBTIENE RESPUESTA BASADA EN ESTADO DE ÁNIMO
# ============================================================================
async def match_response(action):
    # """
    # Pregunta el estado de ánimo del usuario y muestra una respuesta coincidente.

    # Esta función es ASYNC porque usa diálogos Flet.

    # Args:
    #     action: Diccionario con configuración de la acción

    # Returns:
    #     bool: True si se completó exitosamente
    # """
    mood = await ask.open_question(action["prompt"])
    response = search.read_p(action["path"], mood)
    await render.show_match(response, action["path"])
    return True

async def writing_files(action):
    # Función ASYNC porque usa diálogos de Flet
    d = date.today()
    writing = await ask.open_question("Escribe: ")
    if writing == "exit":
        return None
    if writing is None:
        render.smooth_print("Entrada de diario cancelada.")
        return None
    write_files.wadd_file(action["path"], str(d) + "\n" + writing)
    render.smooth_print("Archivo escrito correctamente")
    return True

async def duesMD_render(action):
    dues_dir = search.get_json_value("data/data.json", "actions_paths", "dues_dir")
    # Función ASYNC porque lista_dues es async
    render.smooth_print("Tus pendientes son: ")
    choice = await list_dues(action["path"], True)
    if choice is None:
        return None
    # estructura del choice: (all, [file.md, heading, date]) p.ej.
    # ('recursos_socioemocionales Triptico Infografia Tabla  miercoles 6 mayo', ['recursos_socioemocionales.md', 'Triptico Infografia Tabla', ' miercoles 6 mayo'])
    path = search.locate_get_file(dues_dir + "/", choice[1][0])
    content = search.getMD_block(path, choice[1][1])
    render.smooth_print(choice[1][2].strip() + "\n" + content.strip())
    return None

async def list_dues(path, ask_select):
    # Función ASYNC porque usa diálogos de Flet para seleccionar
    with open(path, 'r') as f:
        tasks = {}
        for line in f:
            if line.strip() == "":
                continue
            key, value = search.getNH_md(line.strip())
            tasks[key] = value
        options = list(tasks.keys())
        choice = await ask.select_option(options, ask_select=ask_select)
        if choice is None:
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

async def check_status_json(action):
    # Función ASYNC porque llama a funciones async
    status = search.get_json_value("data/data.json", "daily_status", action["json_key"])
    if status:
        return None
    else:
        if action["dir_question"]:
            await action["func"](action)
            write_files.set_var_json("data/data.json", "daily_status", action["json_key"], True)
        else:
            path = await check_actions_path(action)
            if not path:
                return None
            resolve_action_path(action)
            execute = await ask.questionSN(action["prompt"])
            write_files.add_counter_json("data/data.json", "times_asked", "daily_status", action["json_key"])
            if execute:
                result = await action["func"](action)
                if result:
                    write_files.set_var_json("data/data.json", "daily_status", action["json_key"], True)

async def add_due(action):
    # Función ASYNC porque usa diálogos de Flet
    dues_file = search.get_json_value("data/data.json", "actions_paths", "dues_file")
    while True:
        while True:
            name_file = await ask.open_question("Escribe nombre del archivo donde quieres agregar el pendiente: ")
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
        title_due = await ask.open_question("Escribe titulo del pendiente que quieres agregar: ")
        title_due = title_due.replace(",", "")
        date_due = await ask.ask_date_hybrid("¿Para cuándo es el pendiente? ")
        if date_due is None:
            render.smooth_print("Agregación de pendiente cancelada.")
            return None
        content_due = await ask.open_question("Escribe contenido del pendiente que quieres agregar: ")
        link_due = utils.linkHeading_md(name_file, title_due)
        link_due = link_due + " " + date_due
        new_due = f"## {title_due}\n{content_due}"
        complete_add = await ask.questionSN(f"¿Quieres agregar el pendiente '{title_due}' al archivo '{name_file}.md'?")
        if not complete_add:
            return None
        write_files.wadd_file(path_file, new_due)
        write_files.wadd_file(dues_file, link_due)
        render.smooth_print("Pendiente agregado exitosamente.")
        another = await ask.questionSN("¿Quieres agregar otro pendiente?")
        if not another:
            return None

async def rm_due(action):
    # Función ASYNC porque usa diálogos de Flet
    dues_file = search.get_json_value("data/data.json", "actions_paths", "dues_file")
    while True:
        render.smooth_print("Selecciona el pendiente que quieres eliminar: ")
        choice = await list_dues(dues_file, False)
        if choice is None:
            return None
        # estructura del choice: (all, [file.md, heading, date]) p.ej.
        # ('recursos_socioemocionales Triptico Infografia Tabla  miercoles 6 mayo', ['recursos_socioemocionales.md', 'Triptico Infografia Tabla', ' miercoles 6 mayo'])
        path_file = search.locate_get_file(action["path"] + "/", choice[1][0])
        link = utils.linkHeading_md(choice[1][0].replace(".md", ""), choice[1][1])
        complete_rm = await ask.questionSN(f"¿Quieres eliminar el pendiente '{choice[1][1]}' del archivo '{choice[1][0]}'?")
        if not complete_rm:
            return None
        rm_link = write_files.rm_MD_block(dues_file, link[2:], "[[")
        rm_due = write_files.rm_MD_block(path_file, choice[1][1])
        if not rm_due or not rm_link:
            render.smooth_print("Sin coincidencias en el archivo del pendiente o en el archivo de links")
            return None
        render.smooth_print("Pendiente eliminado exitosamente.")
        another = await ask.questionSN("¿Quieres eliminar otro pendiente?")
        if not another:
            return None

async def dues_manager(action):
    # Función ASYNC porque usa diálogos y llama a funciones async
    render.smooth_print("¿Qué quieres hacer?")
    act = await ask.select_option(["Agregar pendiente", "Eliminar pendiente"], ask_select=False)
    if act is None:
        return None
    if act == 0:
        await add_due(action)
    elif act == 1:
        await rm_due(action)

# ============================================================================
# FUNCIÓN: main_menu → MENÚ PRINCIPAL DE BOTONES (REEMPLAZA terminal_listening)
# ============================================================================
async def main_menu(page: ft.Page, actions, output_column: ft.Column):
    for key in actions:
        path = await check_actions_path(actions[key])
        if path:
            resolve_action_path(actions[key])
    # Variables para almacenar referencias de botones y estado
    button_write = None
    button_dues_show = None
    button_dues_modify = None
    button_exit = None

    # ========== HANDLERS DE BOTONES ==========

    async def on_write_day(e):
        # """Ejecuta la acción de escribir en diario"""
        try:
            result = await writing_files(actions["write_day"])
            if result:
                render.smooth_print("✓ Entrada de diario guardada")
        except Exception as ex:
            render.smooth_print(f"✗ Error: {str(ex)}")

    async def on_show_dues(e):
        # """Ejecuta la acción de ver pendientes"""
        try:
            await duesMD_render(actions["show_dues"])
        except Exception as ex:
            render.smooth_print(f"✗ Error: {str(ex)}")

    async def on_modify_dues(e):
        # """Ejecuta la acción de modificar pendientes"""
        try:
            await dues_manager(actions["modify_dues"])
        except Exception as ex:
            render.smooth_print(f"✗ Error: {str(ex)}")

    async def on_exit(e):
        # """Cierra la aplicación"""
        render.smooth_print("Saliendo de la aplicación...")
        await page.window.close()

    # ========== CREAR BOTONES ==========

    button_write = ft.ElevatedButton(
        content="📝 Escribir día",
        on_click=on_write_day,
        width=250,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_ACCENT,
            color=ft.Colors.BLACK
        )
    )

    button_dues_show = ft.ElevatedButton(
        content="📋 Ver pendientes",
        on_click=on_show_dues,
        width=250,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.AMBER_ACCENT,
            color=ft.Colors.BLACK
        )
    )

    button_dues_modify = ft.ElevatedButton(
        content="✏️ Modificar pendientes",
        on_click=on_modify_dues,
        width=250,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.ORANGE_ACCENT,
            color=ft.Colors.BLACK
        )
    )

    button_exit = ft.ElevatedButton(
        content="🚪 Salir",
        on_click=on_exit,
        width=250,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.RED_ACCENT,
            color=ft.Colors.BLACK
        )
    )

    # ========== CREAR PANEL DE MENÚ ==========

    menu_panel = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "🤖 MENÚ PRINCIPAL",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREEN_ACCENT
                ),
                ft.Divider(height=10, color=ft.Colors.GREEN_ACCENT),
                ft.Text(
                    "Selecciona una acción:",
                    size=14,
                    color=ft.Colors.GREY_300
                ),
                button_write,
                button_dues_show,
                button_dues_modify,
                button_exit,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        width=300,
        padding=20,
        border_radius=10,
        bgcolor=ft.Colors.GREY_900,
        margin=10
    )

    # Construir layout dividido en dos secciones: mensajes grandes a la izquierda
    # y menú de acciones compacto a la derecha.
    output_container = ft.Container(
        content=output_column,
        border_radius=10,
        padding=20,
        expand=True,
        bgcolor="#1e1e1e",
        margin=10,
    )

    page.add(
        ft.Row(
            controls=[
                output_container,
                menu_panel,
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=10,
        )
    )
    page.update()

    # Mensaje de bienvenida
    render.smooth_print("Sistema listo. Usa los botones del panel derecho para interactuar.")

async def check_actions_path(action):
    # Función ASYNC porque usa diálogos de Flet
    if Path(action["path"]).exists():
        return True
    path = search.get_json_value("data/data.json", "actions_paths", action["path"])
    if not path:
        file = "un archivo" if action["path_file"] else "una carpeta"
        act = "eliminar o agregar" if action["json_key"] == "dues_modified" else "revisar"
        render.smooth_print(f"No tenemos {file} para {act} {action['name']}.")
        add_path = await ask.questionSN(f"Quieres ingresar una ruta para este {file.split()[1]}?")
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
