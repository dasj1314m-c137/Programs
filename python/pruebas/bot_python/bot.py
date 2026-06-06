import manager as mg
import flet as ft
import render
import flet_audio_recorder as far

acts = ["Leer", "Entrenar box", "Meditar", "Editar videos", "Programar", "Escribir", "Aburrirse", "Jugar ajedrez", "Aprender"]

actions = {
    "mood": {
        "prompt": "¿Como estas el dia de hoy?",
        "path": r"data/mood_responses.txt",
        "json_key": "mood_asked",
        "func": mg.match_response,
        "dir_question": True
    },
    "write_day": {
        "name": "Diario",
        "prompt": "¿Quieres escribir tu dia?",
        "path": "diary",
        "path_file": True,
        "json_key": "day_written",
        "func": mg.writing_files,
        "dir_question": False
    },
    "show_dues": {
        "name": "Pendientes",
        "prompt": "¿Quieres revisar tus pendientes?",
        "path": "dues_file",
        "path_file": True,
        "json_key": "dues_shown",
        "func": mg.duesMD_render,
        "dir_question": False
    },
    "modify_dues": {
        "name": "Pendientes",
        "prompt": "¿Quieres agregar o eliminar un pendiente?",
        "path": "dues_dir",
        "path_file": False,
        "json_key": "dues_modified",
        "func": mg.dues_manager,
        "dir_question": False
    },
    "book_learn": {
        "name": "Aprendizajes libros",
        "path": "books_dir",
        "path_file": False,
        "func": mg.book_learn,
    }
}

async def main(page: ft.Page):

    page.title = "Bot"
    page.window_width = 1200
    page.window_height = 700
    page.window_resizable = True
    page.vertical_alignment = ft.MainAxisAlignment.START

    # 2. Creamos un contenedor de texto que simulará nuestra "Terminal Visual"
    # Aquí es a donde mandaremos los prints en la Fase 2
    terminal_output = ft.Column(
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True,
        auto_scroll=True
        )

    audio_recorder = far.AudioRecorder(
        configuration=far.AudioRecorderConfiguration(
            encoder=far.AudioEncoder.PCM16BITS,
            sample_rate=16000,
            channels=1
            ),
            on_stream=lambda e: mg._audio_buffer.extend(e.chunk)
    )

    render.init_render(page, terminal_output) # Inicializamos render con la página y el widget de salida
    mg.init_manager(page, terminal_output, audio_recorder) # Inicializamos manager con la página y el widget de salida
    page.services.append(audio_recorder)
    # No agregamos el contenedor aquí, lo hacemos en main_menu para construir
    # una vista dividida con dos secciones (mensajes y opciones).
    # Mostrar menú principal con botones (reemplaza terminal_listening)
    await mg.main_menu(actions)

    mg.daily_check() # Verificar si es un nuevo día y resetear estados si es necesario
    await mg.check_status_json(actions["mood"])
    await mg.check_status_json(actions["show_dues"])
    await mg.check_status_json(actions["modify_dues"])
    await mg.check_status_json(actions["write_day"])

if __name__ == "__main__":
    ft.run(main)