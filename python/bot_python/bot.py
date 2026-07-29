import manager as mg
import flet as ft
import render
import flet_audio_recorder as far
from responsive import ResponsiveLayout
import audio_processor
import objects
import setup

acts = ["Leer", "Entrenar box", "Meditar", "Editar videos", "Programar", "Escribir", "Aburrirse", "Jugar ajedrez", "Aprender"]

# Mantenemos el diccionario global, pero dejamos las funciones en None para asignarlas dinámicamente en main
actions = {
    # "mood": {
    #     "prompt": "¿Como estas el dia de hoy?",
    #     "path": r".data/mood_responses.txt",
    #     "json_key": "mood_asked",
    #     "func": None,
    #     "dir_question": True
    # },
    "write_day": {
        "name": "Diario",
        "prompt": "¿Quieres escribir tu dia?",
        "path": "diary",
        "path_file": True,
        "json_key": "day_written",
        "func": None,
        "dir_question": False
    },
    "show_dues": {
        "name": "Pendientes",
        "prompt": "¿Quieres revisar tus pendientes?",
        "path": "dues_file",
        "path_file": True,
        "json_key": "dues_shown",
        "func": None,
        "dir_question": False
    },
    "modify_dues": {
        "name": "Pendientes",
        "prompt": "¿Quieres agregar o eliminar un pendiente?",
        "path": "dues_dir",
        "path_file": False,
        "json_key": "dues_modified",
        "func": None,
        "dir_question": False
    },
    "book_learn": {
        "name": "Aprendizajes libros",
        "path": "books_dir",
        "path_file": False,
        "func": None,
    },
    "measures_central_tendency": {
        "name": "Medidas de tendencia central",
        "path": None,
        "func": None,
    },
    "transcribe_action": {
        "name": "Transcribir audio",
        "path": None,
        "func": None,
    }
}

async def main(page: ft.Page):

    page.title = "Bot"
    page.window.width = 800
    page.window.height = 620
    page.window.resizable = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # ---- INICIALIZAR RENDER TEMPRANO (necesario para ask/search) ----

    app_platform = page.platform

    responsive = ResponsiveLayout(page, platform=app_platform)

    terminal_output = ft.Column(
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True,
        auto_scroll=True,
        width=float("inf")
    )

    render.init_render(page, terminal_output, responsive)
    page.add(terminal_output)
    page.update()

    # ---- FIRST RUN SETUP ----
    global_config = setup.get_global_config()

    if global_config is None:
        root_path = await setup.show_welcome_screen(page)
        if root_path is None:
            return
    else:
        root_path = global_config["root_path"]
        setup.ensure_structure(root_path)

    page.controls.clear()
    page.update()
    # ---- END SETUP ----
    recorder = audio_processor.AudioRecorder(None)

    audio_recorder = far.AudioRecorder(
        configuration=far.AudioRecorderConfiguration(
            encoder=far.AudioEncoder.PCM16BITS,
            sample_rate=16000,
            channels=1
        ),
        on_stream=lambda e: recorder.audio_buffer.extend(e.chunk)
    )

    data_base = objects.DataBase_Path()
    data_base.save_root_path(root_path)
    recorder.audio_recorder = audio_recorder
    recorder.data_base = data_base
    bot_manager = mg.BotManager(page, terminal_output, recorder, data_base, responsive, platform=app_platform)

    # actions["mood"]["func"] = bot_manager.match_response
    actions["write_day"]["func"] = bot_manager.writing_files
    actions["show_dues"]["func"] = bot_manager.duesMD_render
    actions["modify_dues"]["func"] = bot_manager.dues_manager
    actions["book_learn"]["func"] = bot_manager.book_learn
    actions["measures_central_tendency"]["func"] = bot_manager.measures_central_tendency
    actions["transcribe_action"]["func"] = bot_manager.transcribe_action

    render.init_render(page, terminal_output, responsive)
    render.set_audio_deps(recorder, data_base)
    page.services.append(audio_recorder)

    def rebuild_layout():
        page.controls.clear()
        page.drawer = None
        page.appbar = None
        page.run_task(bot_manager.main_menu, actions)

    responsive.set_rebuild_callback(rebuild_layout)
    page.on_resize = responsive.on_resize

    await bot_manager.main_menu(actions)

    bot_manager.daily_check()
    await bot_manager.check_status_json(actions["show_dues"])
    await bot_manager.check_status_json(actions["modify_dues"])
    await bot_manager.check_status_json(actions["write_day"])

if __name__ == "__main__":
    ft.run(main)