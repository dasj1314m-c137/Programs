import ask
import render
import search
import write_files
import utils
from datetime import date
import flet as ft
from pathlib import Path
import audio_processor
import os
import objects


_audio_buffer = bytearray()
_page = None
_output_column = None
_audio_recorder = None
_history_ia_bot = []

data_base = objects.DataBase_Path()
messages = objects.Messages()

def init_manager(page: ft.Page, output_column: ft.Column, audio_recorder):
    global _page, _output_column, _audio_recorder
    _page = page
    _output_column = output_column
    _audio_recorder = audio_recorder

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
    writing = await ask.open_question("Escribe:")
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
    messages.set_select_msj("Selecciona un pendiente para ver detalles:")
    choice = await list_links_heading(action["path"])
    if choice is None:
        return None
    # estructura del choice: (all, [file.md, heading, date]) p.ej.
    # ('recursos_socioemocionales Triptico Infografia Tabla  miercoles 6 mayo', ['recursos_socioemocionales.md', 'Triptico Infografia Tabla', ' miercoles 6 mayo'])
    path = search.locate_get_file(dues_dir + "/", choice[1][0])
    content = search.getMD_block(path, choice[1][1])
    render.smooth_print(choice[1][2].strip() + "\n" + content.strip())
    return None

async def list_links_heading(path):
    # Función ASYNC porque usa diálogos de Flet para seleccionar
    with open(path, 'r') as f:
        tasks = {}
        for line in f:
            if line.strip() == "":
                continue
            key, value = search.getNH_md(line.strip())
            tasks[key] = value
        options = list(tasks.keys())
        choice = await ask.select_option(options, messages)
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
        file_name = None
        path_file = None
        while True:
            file_name = await ask.open_question("Escribe nombre del archivo donde quieres agregar el pendiente: ")
            path_file = search.locate_get_file(action["path"] + "/", file_name + ".md")
            if not path_file:
                render.smooth_print("Archivo no encontrado.")
                create_file = await ask.questionSN("¿Quieres crear un nuevo archivo con este nombre?")
                if create_file:
                    await folder_picker(prompt="Selecciona la carpeta donde quieres guardar el nuevo archivo")
                    folder_path = data_base.get_dir_path()
                    if not folder_path:
                        render.smooth_print("No se seleccionó una carpeta. No se podrá crear el archivo.")
                        continue
                    path_file = folder_path + "/" + file_name + ".md"
                    break
                files = search.locate_files_suffix(action["path"] + "/", ".md")
                files.remove("dues")
                messages.set_select_msj("Estos son los archivos disponibles para agregar el pendiente:")
                choice = await ask.select_option(files, messages)
                if choice is None:
                    return None
                file_name = files[choice]
                path_file = f"{action["path"]}/{file_name}.md"
                break
            break
        title_due = await ask.open_question("Escribe titulo del pendiente que quieres agregar: ")
        title_due = title_due.replace(",", "")
        date_due = await ask.ask_date_hybrid("¿Para cuándo es el pendiente? ")
        if date_due is None:
            render.smooth_print("Agregación de pendiente cancelada.")
            return None
        content_due = await ask.open_question("Escribe contenido del pendiente que quieres agregar: ")
        link_due = utils.linkHeading_md(file_name, title_due)
        link_due = link_due + " " + date_due
        new_due = f"## {title_due}\n{content_due}"
        complete_add = await ask.questionSN(f"¿Quieres agregar el pendiente '{title_due}' al archivo '{file_name}.md'?")
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
        messages.set_select_msj("Selecciona el pendiente que quieres eliminar:")
        choice = await list_links_heading(dues_file)
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
    messages.set_select_msj("¿Qué acción quieres realizar con tus pendientes?")
    act = await ask.select_option(["Agregar pendiente", "Eliminar pendiente"], messages)
    if act is None:
        return None
    if act == 0:
        await add_due(action)
    elif act == 1:
        await rm_due(action)

# ============================================================================
# FUNCIÓN: main_menu → MENÚ PRINCIPAL DE BOTONES (REEMPLAZA terminal_listening)
# ============================================================================
async def main_menu(actions):
    # Variables para almacenar referencias de botones y estado
    button_write = None
    button_dues_show = None
    button_dues_modify = None
    button_book_learn = None
    button_exit = None

    # ========== HANDLERS DE BOTONES ==========

    async def on_write_day(e):
        # """Ejecuta la acción de escribir en diario"""
        try:
            result = await writing_files(actions["write_day"])
            if result:
                render.smooth_print("✓ Entrada de diario guardada")
        except Exception as ex:
            print(f"✗ Error: {str(ex)}")

    async def on_show_dues(e):
        # """Ejecuta la acción de ver pendientes"""
        # try:
        await duesMD_render(actions["show_dues"])
        # except Exception as ex:
        #     print(f"✗ Error: {str(ex)}")

    async def on_modify_dues(e):
        # """Ejecuta la acción de modificar pendientes"""
        try:
            await dues_manager(actions["modify_dues"])
        except Exception as ex:
            print(f"✗ Error: {str(ex)}")

    async def on_book_learn(e):
        # """Ejecuta la acción de agregar aprendizajes de libros"""
        try:
            await book_learn(actions["book_learn"])
        except Exception as ex:
            print(f"✗ Error: {str(ex)}")

    async def on_practice_english(e):
        # """Ejecuta la acción de practica speaking english"""
        try:
            await practice_english()
        except Exception as ex:
            print(f"✗ Error: {str(ex)}")

    async def on_exit(e):
        # """Cierra la aplicación"""
        await _page.window.close()

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

    button_book_learn = ft.ElevatedButton(
        content="📚 Aprendizajes de libros",
        on_click=on_book_learn,
        width=250,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN_ACCENT,
            color=ft.Colors.BLACK
        )
    )

    button_practice_english = ft.ElevatedButton(
        content="🎤 Practicas ingles",
        on_click=on_practice_english,
        width=250,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.YELLOW_ACCENT,
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
                button_book_learn,
                button_practice_english,
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
        content=_output_column,
        border_radius=10,
        padding=20,
        expand=True,
        bgcolor="#1e1e1e",
        margin=10,
    )

    _page.add(
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
    _page.update()

    # Mensaje de bienvenida
    render.smooth_print("Sistema listo. Usa los botones del panel derecho para interactuar.")
    for key in actions:
        if actions[key].get("path") is None:
            continue
        path = await check_actions_path(actions[key])
        if path:
            resolve_action_path(actions[key])

async def check_actions_path(action):
    # Función ASYNC porque usa diálogos de Flet
    if Path(action["path"]).exists():
        return True
    path = search.get_json_value("data/data.json", "actions_paths", action["path"])
    if not path:
        file = "un archivo" if action["path_file"] else "una carpeta"
        act = "modificar"
        render.smooth_print(f"No tenemos {file} para {act} {action['name']}.")
        add_path = await ask.questionSN(f"Quieres ingresar una ruta para este {file.split()[1]}?")
        if add_path:
            if action["path_file"]:
                await file_picker([".md"], multiple=False)
                file_path = data_base.get_file_path()
                if file_path is None:
                    render.smooth_print("No se seleccionó un archivo. No se podrá realizar la acción.")
                    return False
                write_files.set_var_json("data/data.json", "actions_paths", action["path"], file_path)
            else:
                await folder_picker()
                folder_path = data_base.get_dir_path()
                if folder_path is None:
                    render.smooth_print("No se seleccionó una carpeta. No se podrá realizar la acción.")
                    return False
                write_files.set_var_json("data/data.json", "actions_paths", action["path"], folder_path)
        else:
            render.smooth_print("No se podrá realizar la acción sin un archivo asociado.")
            return False
    return True

async def file_picker(posfix, multiple=False, prompt="Selecciona un archivo"):
    picker = ft.FilePicker()
    path = await picker.pick_files(dialog_title=prompt, allowed_extensions=posfix, allow_multiple=multiple)
    if path:
        file_path = path[0].path
        data_base.save_file_path(file_path)
        render.smooth_print("Ruta de archivo seleccionada exitosamente")
    else:
        pass

async def folder_picker(prompt="Selecciona una carpeta"):
    picker = ft.FilePicker()
    # async def main(page: ft.Page):
    path = await picker.get_directory_path(dialog_title=prompt)
    if path:
        folder_path = path
        data_base.save_dir_path(folder_path)
        render.smooth_print("Ruta de carpeta seleccionada exitosamente")
    else:
        pass

async def book_learn(action):
    # Función ASYNC porque usa diálogos de Flet
    path = await check_actions_path(action)
    if not path:
        return None
    files_learnings = search.locate_files_suffix(action["path"] + "/", ".md")
    if not files_learnings:
        render.smooth_print("No se encontraron archivos de aprendizajes de libros.")
        add_file = await ask.questionSN("¿Quieres agregar un archivo de aprendizajes de libros?")
        if add_file:
            file_name = await ask.open_question("Escribe el nombre del libro: ")
            content = await ask.open_question("Escribe el aprendizaje: ")
            new_file = f"{file_name}.md"
            write_files.wadd_file(action["path"] + "/" + new_file, content)
            render.smooth_print("Aprendizaje de libro agregado exitosamente.")
        else:
            render.smooth_print("No se podrán registrar aprendizajes sin un archivo asociado.")
            return None
    else:
        messages.set_select_msj("Estos son los archivos de aprendizajes de libros disponibles: ")
        choice = await ask.select_option(files_learnings, messages)
        if choice is None:
            return None
        content = await ask.open_question("Escribe el aprendizaje que quieres agregar: ")
        if content is None:
            render.smooth_print("Agregación de aprendizaje cancelada.")
            return None
        choice = files_learnings[choice]
        file_name = choice + ".md"
        write_files.wadd_file(action["path"] + "/" + file_name, content)
        render.smooth_print("Aprendizaje de libro agregado exitosamente.")

async def practice_english():
    await audio_manager()

# ============================================================================
# FUNCIÓN: process_recorded_audio → PROCESA EL AUDIO GRABADO
# ============================================================================
async def talk_audio_ia(path):
    # """Procesa el audio grabado, lo transcribe y muestra la respuesta del coach."""
    # try:
    if len(_history_ia_bot) == 0:
        instructions_bot = {
            "role": "system",
            "content": (
                "You are a chill, friendly American English coach with a relaxed, YouTuber-like vibe. "
                "Your goal is to help the user practice natural, everyday spoken English through a fluid conversation.\n\n"

                "STRICT RULES:\n"
                "1. ALWAYS reply in English, even if the user speaks in Spanish.\n"
                "2. Keep answers short and punchy (max 2-3 sentences) to maintain a fast conversational pace.\n"
                "3. Use casual language, contractions (gonna, wanna, context-appropriate slang), and a friendly tone. Avoid sounding formal or academic.\n\n"

                "CONVERSATION FLOW:\n"
                "- Start by asking the user how their day is going.\n"
                "- If the user shares something, actively follow up on their story and ask engaging questions about it.\n"
                "- If the user gives a short answer or doesn't suggest a topic, smoothly introduce a new, interesting everyday topic (e.g., tech, pop culture, animals, history, daily life) to keep the chat alive.\n\n"

                "CORRECTION STYLE (SUBTLE):\n"
                "- NEVER correct natural, informal greetings or casual phrasing like 'How's it going?'. That is correct for this context.\n"
                "- Only correct major grammatical errors that hurt clarity (e.g., wrong verb tenses or broken structures).\n"
                "- Do NOT use bullet points, bold text, or formal grammar explanations for corrections. Instead, embed the correction subtly in your natural response (e.g., 'Oh, you went to the store yesterday? That's awesome, what did you buy?')."
            )
        }
        _history_ia_bot.append(instructions_bot)

    render.smooth_print("Procesando audio...")
    _page.update()

    transcribed_text = await audio_processor.transcribe_audio(path)

    if not transcribed_text or transcribed_text.strip() == "":
        render.smooth_print("[⚠️] No se detectó audio en la grabación")
        return

    usr_msj = {
        "role": "user",
        "content": transcribed_text
    }
    _history_ia_bot.append(usr_msj)

    user_message_card = ft.Card(
        content=ft.Container(
            content=ft.Text(
                value=transcribed_text,
                size=14,
                color=ft.Colors.BLUE_ACCENT,
                selectable=True
            ),
            padding=12,
            bgcolor=ft.Colors.GREY_900,
            border_radius=5
        ),
        margin=8
    )

    _output_column.controls.append(user_message_card)
    _page.update()

    coach_response = await audio_processor.talk_with_coach(_history_ia_bot)

    assistant_msj = {
        "role": "assistant",
        "content": coach_response
    }
    _history_ia_bot.append(assistant_msj)

    coach_message_card = ft.Card(
        content=ft.Container(
            content=ft.Text(
                value=coach_response,
                size=14,
                color=ft.Colors.GREEN_ACCENT,
                selectable=True
            ),
            padding=12,
            bgcolor=ft.Colors.BLACK,
            border_radius=5
        ),
        margin=8
    )
    _output_column.controls.append(coach_message_card)
    _page.update()

    try:
        os.remove(path)
    except Exception as ex:
        print(f"algo salio mal ->: {ex}")

    # except Exception as ex:
    #     render.smooth_print(f"[ERROR] Error procesando audio: {ex}")

async def audio_manager():
    buttons = []
    current_audio_path = None

    async def toggle_recording(e):
        is_recording = e.control.data
        nonlocal current_audio_path

        if not is_recording:
            e.control.data = True
            e.control.icon = ft.Icons.STOP_CIRCLE
            e.control.icon_color = ft.Colors.RED
            e.control.update()

            _audio_buffer.clear()
            render.smooth_print("Iniciando grabacion..")
            current_audio_path = utils.create_stamp_path("record", "wav")
            current_audio_path = f"audios/{current_audio_path}"
            await _audio_recorder.start_recording(output_path=current_audio_path)


        else:
            try:
                # Modo: DETENER GRABACIÓN
                e.control.data = False
                e.control.icon = ft.Icons.MIC
                e.control.icon_color = ft.Colors.GREEN_ACCENT
                e.control.update()

                render.smooth_print("Grabacion terminada")
                await _audio_recorder.stop_recording()

                raw_bytes = bytes(_audio_buffer)
                _audio_buffer.clear()

                if not raw_bytes:
                    render.smooth_print("Sin entrada de audio")
                    return

                utils.save_pcm_to_wav(raw_bytes, current_audio_path)

                await talk_audio_ia(current_audio_path)

                _output_column.controls.remove(btn_row)
                _output_column.controls.append(btn_row)
                _page.update()

            except Exception as ex:
                print(f"🚨 ¡TE CACHÉ! El grabador explotó por esto: {ex}")

    # async def handle_pause(e):
    #     if await audio_recorder.is_recording():
    #         await audio_recorder.pause_recording()

    # async def handle_resume(e):
    #     if await audio_recorder.is_paused():
    #         await audio_recorder.resume_recording()

    # async def handle_record(e):
    #     nonlocal current_audio_path
    #     _audio_buffer.clear()
    #     render.smooth_print("Iniciando grabacion..")
    #     current_audio_path = utils.create_stamp_path("record", "wav")
    #     current_audio_path = f"audios/{current_audio_path}"
    #     await _audio_recorder.start_recording(output_path=current_audio_path)

    # async def handle_stop(e):
    #     render.smooth_print("Grabacion terminada")
    #     # try:
    #     await _audio_recorder.stop_recording()

    #     raw_bytes = bytes(_audio_buffer)
    #     _audio_buffer.clear()

    #     if not raw_bytes:
    #         render.smooth_print("Sin entrada de audio")
    #         return

    #     utils.save_pcm_to_wav(raw_bytes, current_audio_path)

    #     await talk_audio_ia(current_audio_path)

    #     _output_column.controls.remove(btn_row)
    #     _output_column.controls.append(btn_row)
    #     _page.update()
        # except Exception as ex:
        #     render.smooth_print(f"[ERROR] o grabación: {ex}")

    async def cancel(e):
        _audio_buffer.clear()
        _history_ia_bot.clear()
        render.smooth_print("Chat cerrado nos vemos")
        _output_column.controls.remove(btn_row)
        _page.update()

    btn_grabar = ft.IconButton(
        icon=ft.Icons.MIC,
        icon_color=ft.Colors.GREEN_ACCENT,
        bgcolor=ft.Colors.BLACK,
        on_click=toggle_recording,
        data=False
    )

    # btn_stop = ft.IconButton(
    #     icon=ft.Icons.STOP_CIRCLE,
    #     icon_color=ft.Colors.RED,
    #     bgcolor=ft.Colors.BLACK,
    #     on_click=handle_stop
    # )

    btn_cancel = ft.ElevatedButton(
        content=ft.Text("Cancel"),
        color=ft.Colors.GREEN_ACCENT,
        bgcolor=ft.Colors.BLACK,
        on_click=cancel
    )

    # btn_pause = ft.IconButton(
    #     icon=ft.Icons.PAUSE,
    #     icon_color=ft.Colors.GREEN_ACCENT,
    #     bgcolor=ft.Colors.BLACK,
    #     on_click=handle_pause
    # )
    # btn_resume = ft.IconButton(
    #     icon=ft.Icons.PLAY_ARROW,
    #     icon_color=ft.Colors.GREEN_ACCENT,
    #     bgcolor=ft.Colors.BLACK,
    #     on_click=handle_resume
    # )

    buttons.append(btn_grabar)
    # buttons.append(btn_stop)
    buttons.append(btn_cancel)
    # buttons.append(btn_pause)
    # buttons.append(btn_resume)

    btn_row = ft.Row(
        controls=buttons,
        spacing=8,
        alignment=ft.MainAxisAlignment.CENTER
    )

    render.smooth_print("Puedes iniciar grabacion")
    _output_column.controls.append(btn_row)
    _page.update()
