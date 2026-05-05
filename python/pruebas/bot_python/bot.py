import manager
# import ask
# import render
# import search
# import utils
# import ask

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
    "dues": {
        "prompt": "Tus pendientes son: ",
        "path": r"/home/dasj/documents/works/obsidian_vault/dues/dues.md",
        "json_key": "dues_asked"
    }
}

paths = {
    "homework": r"/home/dasj/documents/works/obsidian_vault/dues/homework/"
}

def main():
    manager.daily_check()
    manager.check_status_json(lambda: manager.match_response(actions["mood"]), actions["mood"])
    manager.check_status_json(lambda: manager.writing_files(actions["write_day"]), actions["write_day"])
    # manager.duesMD_render(actions["dues"], paths["homework"])

main()