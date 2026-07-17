import manager as mg
import flet as ft
import render
import flet_audio_recorder as far

acts = ["Leer", "Entrenar box", "Meditar", "Editar videos", "Programar", "Escribir", "Aburrirse", "Jugar ajedrez", "Aprender"]

# Mantenemos el diccionario global, pero dejamos las funciones en None para asignarlas dinámicamente en main
actions = {
    "mood": {
        "prompt": "¿Como estas el dia de hoy?",
        "path": r"data/mood_responses.txt",
        "json_key": "mood_asked",
        "func": None,
        "dir_question": True
    },
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
    }
}

async def main(page: ft.Page):

    page.title = "Bot"
    page.window_width = 1200
    page.window_height = 700
    page.window_resizable = True
    page.vertical_alignment = ft.MainAxisAlignment.START

    # 1. Creamos el contenedor para la Terminal Visual
    terminal_output = ft.Column(
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True,
        auto_scroll=True
    )

    # 2. Inicializamos el manager sin el grabador de audio para resolver la dependencia circular
    bot_manager = mg.BotManager(page, terminal_output, None)

    # 3. Creamos el grabador de audio apuntando directamente al buffer de la instancia de BotManager
    audio_recorder = far.AudioRecorder(
        configuration=far.AudioRecorderConfiguration(
            encoder=far.AudioEncoder.PCM16BITS,
            sample_rate=16000,
            channels=1
        ),
        on_stream=lambda e: bot_manager.audio_buffer.extend(e.chunk)
    )

    # Inyectamos la referencia del grabador ya configurado de vuelta al manager
    bot_manager.audio_recorder = audio_recorder

    # 4. Asignamos los métodos de la instancia de BotManager a nuestro diccionario de acciones
    actions["mood"]["func"] = bot_manager.match_response
    actions["write_day"]["func"] = bot_manager.writing_files
    actions["show_dues"]["func"] = bot_manager.duesMD_render
    actions["modify_dues"]["func"] = bot_manager.dues_manager
    actions["book_learn"]["func"] = bot_manager.book_learn
    actions["measures_central_tendency"]["func"] = bot_manager.measures_central_tendency

    # Inicializamos renders y agregamos servicios
    render.init_render(page, terminal_output)
    page.services.append(audio_recorder)

    # Mostrar menú principal con botones usando la instancia del BotManager
    await bot_manager.main_menu(actions)

    # Rutinas diarias de estado
    bot_manager.daily_check()
    await bot_manager.check_status_json(actions["show_dues"])
    await bot_manager.check_status_json(actions["modify_dues"])
    await bot_manager.check_status_json(actions["write_day"])

if __name__ == "__main__":
    ft.run(main)