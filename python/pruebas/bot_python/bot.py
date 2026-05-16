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
        "prompt": "¿Quieres escribir tu dia? ",
        "path": r"/home/dasj/documents/works/obsidian_vault/diary/may.md",
        "json_key": "day_written",
        "func": mg.writing_files,
        "dir_question": False
    },
    "show_dues": {
        "prompt": "¿Quieres revisar tus pendientes? ",
        "path": r"/home/dasj/documents/works/obsidian_vault/dues/dues.md",
        "json_key": "dues_shown",
        "func": mg.duesMD_render,
        "dir_question": False
    },
    "modify_dues": {
        "prompt": "¿Quieres agregar o eliminar un pendiente? ",
        "path": r"/home/dasj/documents/works/obsidian_vault/dues/dues.md",
        "json_key": "dues_modified",
        "func": mg.dues_manager,
        "dir_question": False
    }
}

def main():
    mg.daily_check()
    mg.check_status_json(lambda: mg.match_response(actions["mood"]), actions["mood"])
    mg.actions_question(actions["show_dues"])
    mg.actions_question(actions["modify_dues"])
    mg.actions_question(actions["write_day"])
    mg.terminal_listening(actions)

main()