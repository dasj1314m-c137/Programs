import os
import ask
import render
import search
import write_files
import utils
from datetime import date
import flet as ft
from pathlib import Path
import audio_processor
import objects
from utility import math_oprs

class BotManager:
    def __init__(self, page: ft.Page, output_column: ft.Column, audio_recorder, responsive=None):
        self.page = page
        self.output_column = output_column
        self.audio_recorder = audio_recorder
        self.responsive = responsive

        self.audio_buffer = bytearray()
        self.history_ia_bot = []

        self.data_base = objects.DataBase_Path()
        self.messages = objects.Messages()


    def daily_check(self):
        data = search.get_json_data("data/data.json")
        today = date.today().strftime("%d/%m/%y")
        if data["metadata"]["last_update"] != today:
            data["metadata"]["last_update"] = today
            for key in data["daily_status"]:
                data["daily_status"][key] = False
            for key in data["times_asked"]:
                data["times_asked"][key] = 0
            utils.save_json_data("data/data.json", data)

    def resolve_action_path(self, action):
        path = action["path"]
        if Path(path).exists():
            return None
        resolved_path = search.get_json_value("data/data.json", "actions_paths", path)
        if resolved_path:
            action["path"] = resolved_path
        return None

    async def check_actions_path(self, action):
        # Función ASYNC porque usa diálogos de Flet
        if Path(action["path"]).exists():
            return True
        path = search.get_json_value("data/data.json", "actions_paths", action["path"])
        if not path or not Path(path).exists():
            file = "un archivo" if action["path_file"] else "una carpeta"
            act = "modificar"
            render.smooth_print(f"No tenemos {file} para {act} {action['name']}.")
            add_path = await ask.questionSN(f"Quieres ingresar una ruta para este {file.split()[1]}?")
            if add_path:
                if action["path_file"]:
                    await search.file_picker([".md"], self.data_base, render, ft, multiple=False)
                    file_path = self.data_base.get_file_path()
                    if file_path is None:
                        render.smooth_print("No se seleccionó un archivo. No se podrá realizar la acción.")
                        return False
                    write_files.set_var_json("data/data.json", "actions_paths", action["path"], file_path)
                else:
                    await search.folder_picker(self.data_base, render, ft)
                    folder_path = self.data_base.get_dir_path()
                    if folder_path is None:
                        render.smooth_print("No se seleccionó una carpeta. No se podrá realizar la acción.")
                        return False
                    write_files.set_var_json("data/data.json", "actions_paths", action["path"], folder_path)
            else:
                render.smooth_print("No se podrá realizar la acción sin un archivo asociado.")
                return False
        return True

    async def check_status_json(self, action):
        # Función ASYNC porque llama a funciones async
        status = search.get_json_value("data/data.json", "daily_status", action["json_key"])
        if status:
            return None
        else:
            if action["dir_question"]:
                await action["func"](action)
                write_files.set_var_json("data/data.json", "daily_status", action["json_key"], True)
            else:
                path = await self.check_actions_path(action)
                if not path:
                    return None
                self.resolve_action_path(action)
                execute = await ask.questionSN(action["prompt"])
                write_files.add_counter_json("data/data.json", "times_asked", "daily_status", action["json_key"])
                if execute:
                    result = await action["func"](action)
                    if result:
                        write_files.set_var_json("data/data.json", "daily_status", action["json_key"], True)

    async def match_response(self,action):
        mood = await ask.open_question(action["prompt"])
        response = search.read_p(action["path"], mood)
        await render.show_match(response, action["path"])
        return True

    async def writing_files(self, action):
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

    async def list_links_heading(self, path):
        obj_opts = objects.OptionsManager()
        # Función ASYNC porque usa diálogos de Flet para seleccionar
        with open(path, 'r') as f:
            for line in f:
                if line.strip() == "":
                    continue
                _, value = search.getNH_md(line.strip())
                utils.creating_obj_due(obj_opts, value[1], value[0], value[2])
            choice = await ask.select_option(obj_opts, self.messages)
            if choice is None:
                return None
            return choice

    async def duesMD_render(self, action):
        dues_dir = search.get_json_value("data/data.json", "actions_paths", "dues_dir")
        # Función ASYNC porque lista_dues es async
        self.messages.set_select_msj("Selecciona un pendiente para ver detalles:")
        choice = await self.list_links_heading(action["path"])
        if choice is None:
            return None
        # choice es un objeto Due con name=file, description=heading y date=fecha
        # `description` ahora contiene el archivo, `name` el heading
        path = search.locate_get_file(dues_dir + "/", choice.description)
        content = search.getMD_block(path, choice.name)
        date_text = choice.date.strip() if choice.date else ""
        render.smooth_print(date_text + "\n" + content.strip())
        return None

    async def add_due(self, action):
        # Función ASYNC porque usa diálogos de Flet
        dues_file = search.get_json_value("data/data.json", "actions_paths", "dues_file")
        while True:
            while True:
                files = search.locate_files_suffix(action["path"] + "/", ".md")
                files.remove("dues")
                self.messages.set_select_msj("Estos son los archivos disponibles para agregar el pendiente:")
                file_name = await ask.select_option(files, self.messages, opt_other=True)
                if file_name is None:
                    return None
                elif file_name == "Otro":
                    file_name = await ask.open_question("Escribe nombre del nuevo archivo donde quieres agregar el pendiente: ")
                    create_file = await ask.questionSN("¿Quieres crear un nuevo archivo con este nombre?")
                    if create_file:
                        await search.folder_picker(self.data_base, render, ft, prompt="Selecciona la carpeta donde quieres guardar el nuevo archivo")
                        folder_path = self.data_base.get_dir_path()
                        if not folder_path:
                            render.smooth_print("No se seleccionó una carpeta. No se podrá crear el archivo.")
                            continue
                        path_file = folder_path + "/" + file_name + ".md"
                        break
                path_file = search.locate_get_file(action["path"] + "/", file_name + ".md")
                break
            title_due = await ask.open_question("Escribe titulo del pendiente que quieres agregar: ")
            title_due = title_due.replace(",", "")
            date_due = await ask.ask_date_hybrid("Fecha del pendiente")
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

    async def rm_due(self, action):
        # Función ASYNC porque usa diálogos de Flet
        dues_file = search.get_json_value("data/data.json", "actions_paths", "dues_file")
        while True:
            self.messages.set_select_msj("Selecciona el pendiente que quieres eliminar:")
            choice = await self.list_links_heading(dues_file)
            if choice is None:
                return None
            # choice es un objeto Due con name=file, description=heading y date=fecha
            path_file = search.locate_get_file(action["path"] + "/", choice.description)
            link = utils.linkHeading_md(choice.description.replace(".md", ""), choice.name)
            complete_rm = await ask.questionSN(f"¿Quieres eliminar el pendiente '{choice.name}' del archivo '{choice.description}'?")
            if not complete_rm:
                return None
            rm_link = write_files.rm_MD_block(dues_file, link[2:], "[[")
            # El heading es ahora `choice.name`
            rm_due = write_files.rm_MD_block(path_file, choice.name)
            if not rm_due or not rm_link:
                render.smooth_print("Sin coincidencias en el archivo del pendiente o en el archivo de links")
                return None
            render.smooth_print("Pendiente eliminado exitosamente.")
            another = await ask.questionSN("¿Quieres eliminar otro pendiente?")
            if not another:
                return None

    async def dues_manager(self, action):
        # Función ASYNC porque usa diálogos y llama a funciones async
        self.messages.set_select_msj("¿Qué acción quieres realizar con tus pendientes?")
        act = await ask.select_option(["Agregar pendiente", "Eliminar pendiente"], self.messages)
        if act is None:
            return None
        if act == "Agregar pendiente":
            await self.add_due(action)
        elif act == "Eliminar pendiente":
            await self.rm_due(action)
        else:
            render.smooth_print("revisa tus condicionales chaufa")

    async def book_learn(self, action):
        # Función ASYNC porque usa diálogos de Flet
        path = await self.check_actions_path(action)
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
            self.messages.set_select_msj("Estos son los archivos de aprendizajes de libros disponibles: ")
            choice = await ask.select_option(files_learnings, self.messages, opt_other=True)
            if choice is None:
                return None
            elif choice == "Otro":
                file_name = await ask.open_question("Escribe el nombre del libro: ")
                content = await ask.open_question("Escribe el aprendizaje: ")
                new_file = f"{file_name}.md"
                write_files.wadd_file(action["path"] + "/" + new_file, content)
                render.smooth_print("Aprendizaje de libro agregado exitosamente.")
            else:
                content = await ask.open_question("Escribe el aprendizaje que quieres agregar: ")
                if content is None:
                    render.smooth_print("Agregación de aprendizaje cancelada.")
                    return None
                file_name = choice + ".md"
                write_files.wadd_file(action["path"] + "/" + file_name, content)
                render.smooth_print("Aprendizaje de libro agregado exitosamente.")

    async def measures_central_tendency(self):
        # Función ASYNC porque usa diálogos de Flet
        while True:
            self.messages.set_select_msj("Selecciona la medida de tendencia central que quieres calcular:")
            opr = await ask.select_option(["Media", "Mediana", "Moda", "Todas"], self.messages)
            if opr is None:
                render.smooth_print("Cálculo de medidas de tendencia central cancelado.")
                return None
            while True:
                data = await ask.open_question("Ingresa los números separados por comas (ej: 1,2,3,4): ")
                if not data:
                    render.smooth_print("No se ingresaron datos")
                    continue
                if data.lower() == "exit":
                    render.smooth_print("Cálculo de medidas de tendencia central cancelado.")
                    return None
                try:
                    numbers = [float(num.strip()) for num in data.split(",")]
                    break
                except ValueError:
                    render.smooth_print("Error: Asegúrate de ingresar solo números válidos separados por comas.")
                    continue

            if opr == "Todas":
                measures = math_oprs.calculate_all_measures(numbers)
                if measures['mode'] is None:
                    measures['mode'] = "No hay moda"
                else:
                    measures['mode'] = ", ".join(map(str, measures['mode']))  # Convertir la lista de modas a cadena
                result = f"Media: {measures['mean']}\nMediana: {measures['median']}\nModa: {measures['mode']}"
            else:
                if opr == "Media":
                    value = math_oprs.mean(numbers)
                elif opr == "Mediana":
                    value = math_oprs.median(numbers)
                elif opr == "Moda":
                    value = math_oprs.mode(numbers)
                    if value is None:
                        value = "No hay moda"
                    else:
                        value = ", ".join(map(str, value))  # Convertir la lista de modas a cadena
                else:
                    render.smooth_print("Operación no válida")
                    return None
                result = f"{opr}: {value}"
            render.smooth_print(result)
            another = await ask.questionSN("¿Quieres calcular otra medida de tendencia central?")
            if not another:
                render.smooth_print("Cálculo de medidas de tendencia central finalizado.")
                return None

    async def audio_manager(self, func):
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

                self.audio_buffer.clear()
                render.smooth_print("Iniciando grabacion..")
                current_audio_path = utils.create_stamp_path("record", "wav")
                current_audio_path = f"audios/{current_audio_path}"
                await self.audio_recorder.start_recording(output_path=current_audio_path)


            else:
                try:
                    # Modo: DETENER GRABACIÓN
                    e.control.data = False
                    e.control.icon = ft.Icons.MIC
                    e.control.icon_color = ft.Colors.GREEN_ACCENT
                    e.control.update()

                    render.smooth_print("Grabacion terminada")
                    await self.audio_recorder.stop_recording()

                    raw_bytes = bytes(self.audio_buffer)
                    self.audio_buffer.clear()

                    if not raw_bytes:
                        render.smooth_print("Sin entrada de audio")
                        return

                    utils.save_pcm_to_wav(raw_bytes, current_audio_path)

                    self.data_base.save_audio_path(current_audio_path)
                    await func(self.data_base)

                    self.output_column.controls.remove(btn_row)
                    self.output_column.controls.append(btn_row)
                    self.page.update()

                except Exception as ex:
                    print(f"🚨 ¡TE CACHÉ! El grabador explotó por esto: {ex}")

        async def cancel(e):
            self.audio_buffer.clear()
            self.history_ia_bot.clear()
            render.smooth_print("Chat cerrado nos vemos")
            self.output_column.controls.remove(btn_row)
            self.page.update()

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
        buttons.append(btn_cancel)
        # buttons.append(btn_stop)
        # buttons.append(btn_pause)
        # buttons.append(btn_resume)

        btn_row = ft.Row(
            controls=buttons,
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER
        )

        render.smooth_print("Puedes iniciar grabacion")
        self.output_column.controls.append(btn_row)
        self.page.update()

    async def talk_audio_ia(self, data_base):
        # """Procesa el audio grabado, lo transcribe y muestra la respuesta del coach."""
        # try:
        path = data_base.get_audio_path()

        if len(self.history_ia_bot) == 0:
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
            self.history_ia_bot.append(instructions_bot)

        render.smooth_print("Procesando audio...")
        self.page.update()

        transcribed_text = await audio_processor.transcribe_audio(path)

        if not transcribed_text or transcribed_text.strip() == "":
            render.smooth_print("[⚠️] No se detectó audio en la grabación")
            return

        usr_msj = {
            "role": "user",
            "content": transcribed_text
        }
        self.history_ia_bot.append(usr_msj)

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

        self.output_column.controls.append(user_message_card)
        self.page.update()

        coach_response = await audio_processor.talk_with_coach(self.history_ia_bot)

        assistant_msj = {
            "role": "assistant",
            "content": coach_response
        }
        self.history_ia_bot.append(assistant_msj)

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
        self.output_column.controls.append(coach_message_card)
        self.page.update()

        try:
            os.remove(path)
        except Exception as ex:
            print(f"algo salio mal ->: {ex}")

    async def practice_english(self):
        await self.audio_manager(self.talk_audio_ia)


    async def main_menu(self, actions):
        self.page.drawer = None
        self.page.appbar = None

        # ========== HANDLERS DE BOTONES ==========

        async def on_write_day(e):
            try:
                result = await self.writing_files(actions["write_day"])
                if result:
                    render.smooth_print("✓ Entrada de diario guardada")
            except Exception as ex:
                print(f"✗ Error: {str(ex)}")

        async def on_show_dues(e):
            await self.duesMD_render(actions["show_dues"])

        async def on_modify_dues(e):
            try:
                await self.dues_manager(actions["modify_dues"])
            except Exception as ex:
                print(f"✗ Error: {str(ex)}")

        async def on_math_oprs(e):
            try:
                await self.measures_central_tendency()
            except Exception as ex:
                print(f"✗ Error: {str(ex)}")

        async def on_book_learn(e):
            try:
                await self.book_learn(actions["book_learn"])
            except Exception as ex:
                print(f"✗ Error: {str(ex)}")

        async def on_practice_english(e):
            try:
                await self.practice_english()
            except Exception as ex:
                print(f"✗ Error: {str(ex)}")

        async def on_exit(e):
            await self.page.window.close()

        async def close_drawer(e=None):
            await self.page.close_drawer()

        def on_menu_item_click(handler):
            async def handler_wrapper(e):
                await close_drawer()
                await handler(e)
            return handler_wrapper

        is_mobile = self.responsive.is_mobile if self.responsive else False
        btn_w = self.responsive.get_button_width() if self.responsive else 250
        btn_h = self.responsive.get_button_height() if self.responsive else 50
        title_sz = self.responsive.get_title_size() if self.responsive else 20
        content_pad = self.responsive.get_content_padding() if self.responsive else 20

        # ========== CREAR BOTONES ==========
        menu_items = [
            ("📝 Escribir día", on_write_day, ft.Colors.BLUE_ACCENT),
            ("📋 Ver pendientes", on_show_dues, ft.Colors.AMBER_ACCENT),
            ("✏️ Modificar pendientes", on_modify_dues, ft.Colors.ORANGE_ACCENT),
            ("📚 Aprendizajes de libros", on_book_learn, ft.Colors.GREEN_ACCENT),
            ("🎤 Practicas ingles", on_practice_english, ft.Colors.YELLOW_ACCENT),
            ("🧮 Operaciones matemáticas", on_math_oprs, ft.Colors.PURPLE_ACCENT),
            ("🚪 Salir", on_exit, ft.Colors.RED_ACCENT),
        ]

        def make_button(label, handler, color):
            return ft.ElevatedButton(
                content=label,
                on_click=on_menu_item_click(handler),
                width=btn_w,
                height=btn_h,
                style=ft.ButtonStyle(bgcolor=color, color=ft.Colors.BLACK)
            )

        buttons = [make_button(label, handler, color) for label, handler, color in menu_items]

        menu_column = ft.Column(
            controls=[
                ft.Text(
                    "🤖 MENÚ PRINCIPAL",
                    size=title_sz,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREEN_ACCENT
                ),
                ft.Divider(height=10, color=ft.Colors.GREEN_ACCENT),
                ft.Text(
                    "Selecciona una acción:",
                    size=14,
                    color=ft.Colors.GREY_300
                ),
                *buttons,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )

        output_container = ft.Container(
            content=self.output_column,
            border_radius=10,
            padding=content_pad,
            expand=True,
            bgcolor="#1e1e1e",
            margin=10,
        )

        if is_mobile:

            async def handle_show_drawer(e):
                await self.page.show_drawer()

            async def handle_drawer_change(e):
                await self.page.close_drawer()
            # ========== MÓVIL: NavigationDrawer + AppBar ==========
            drawer = ft.NavigationDrawer(
                on_change=handle_drawer_change,
                controls=[
                    ft.Container(
                        content=menu_column,
                        padding=20,
                        bgcolor=ft.Colors.GREY_900,
                    )
                ],
                bgcolor=ft.Colors.GREY_900,
            )

            self.page.drawer = drawer

            self.page.appbar = ft.AppBar(
                leading=ft.IconButton(
                    icon=ft.Icons.MENU,
                    icon_color=ft.Colors.GREEN_ACCENT,
                    icon_size=28,
                    tooltip="Menú",
                    on_click=handle_show_drawer,
                ),
                title=ft.Text(
                    "🤖 Bot",
                    color=ft.Colors.GREEN_ACCENT,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
                bgcolor=ft.Colors.GREY_900,
                center_title=False,
            )

            self.page.add(
                ft.SafeArea(
                    content=output_container,
                    expand=True,
                )
            )
        else:
            # ========== DESKTOP: sidebar fijo a la derecha ==========
            menu_panel = ft.Container(
                content=menu_column,
                width=290,
                padding=20,
                border_radius=10,
                bgcolor=ft.Colors.GREY_900,
                margin=10,
            )

            self.page.add(
                ft.Row(
                    controls=[output_container, menu_panel],
                    expand=True,
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    spacing=10,
                )
            )

        self.page.update()

        render.smooth_print("Sistema listo. Usa los botones del panel derecho para interactuar.")
        for action in actions:
            if actions[action].get("path") is None:
                continue
            path = await self.check_actions_path(actions[action])
            if path:
                self.resolve_action_path(actions[action])

# _audio_buffer = bytearray()
# _page = None
# _output_column = None
# _audio_recorder = None
# _history_ia_bot = []

# data_base = objects.DataBase_Path()
# messages = objects.Messages()

# def init_manager(page: ft.Page, output_column: ft.Column, audio_recorder):
#     global _page, _output_column, _audio_recorder
#     _page = page
#     _output_column = output_column
#     _audio_recorder = audio_recorder
