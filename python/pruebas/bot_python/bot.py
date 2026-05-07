import manager

acts = ["Leer", "Entrenar box", "Meditar", "Editar videos", "Programar", "Escribir", "Aburrirse", "Jugar ajedrez", "Aprender"]

actions = {
    "mood": {
        "prompt": "¿Como estas el dia de hoy? ",
        "path": r"data/mood_responses.txt",
        "json_key": "mood_asked"
    },
    "write_day": {
        "prompt": "¿Quieres escribir tu dia? ",
        "path": r"/home/dasj/documents/works/obsidian_vault/diary/may.md",
        "json_key": "day_written"
    },
    "show_dues": {
        "prompt": "Tus pendientes son: ",
        "path": r"/home/dasj/documents/works/obsidian_vault/dues/dues.md",
        "json_key": "dues_asked"
    },
    "modify_dues": {
        "prompt": "¿Quieres agregar o eliminar un pendiente? ",
        "path": r"/home/dasj/documents/works/obsidian_vault/dues/dues.md",
        "json_key": "dues_added"
    }
}

def main():
    manager.daily_check()
    manager.check_status_json(lambda: manager.match_response(actions["mood"]), actions["mood"])
    manager.check_status_json(lambda: manager.writing_files(actions["write_day"]), actions["write_day"])
    manager.duesMD_render(actions["show_dues"])
    manager.dues_manager(actions["modify_dues"])

main()