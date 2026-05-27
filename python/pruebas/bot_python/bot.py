import manager as mg

acts = ["Leer", "Entrenar box", "Meditar", "Editar videos", "Programar", "Escribir", "Aburrirse", "Jugar ajedrez", "Aprender"]

actions = {
    "mood": {
        "prompt": "¿Como estas el dia de hoy? ",
        "path": r"data/mood_responses.txt",
        "json_key": "mood_asked",
        "func": mg.match_response,
        "dir_question": True
    },
    "write_day": {
        "name": "Diario",
        "prompt": "¿Quieres escribir tu dia? ",
        "path": "diary",
        "path_file": True,
        "json_key": "day_written",
        "func": mg.writing_files,
        "dir_question": False
    },
    "show_dues": {
        "name": "Pendientes",
        "prompt": "¿Quieres revisar tus pendientes? ",
        "path": "dues_file",
        "path_file": True,
        "json_key": "dues_shown",
        "func": mg.duesMD_render,
        "dir_question": False
    },
    "modify_dues": {
        "name": "Pendientes",
        "prompt": "¿Quieres agregar o eliminar un pendiente? ",
        "path": "dues_dir",
        "path_file": False,
        "json_key": "dues_modified",
        "func": mg.dues_manager,
        "dir_question": False
    }
}

def main():
    mg.daily_check()
    mg.check_status_json(actions["mood"])
    mg.check_status_json(actions["show_dues"])
    mg.check_status_json(actions["modify_dues"])
    mg.check_status_json(actions["write_day"])
    mg.terminal_listening(actions)

main()