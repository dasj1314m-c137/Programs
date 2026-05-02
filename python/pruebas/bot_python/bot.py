import manager

acts = ["Leer", "Entrenar box", "Meditar", "Editar videos", "Programar", "Escribir", "Aburrirse", "Jugar ajedrez", "Aprender"]

questions = {
    "mood": ("¿Como estas el dia de hoy? ", r"responses/mood_responses.txt"),
    "write_day": ("¿Quieres escribir tu dia? ", r"/home/dasj/documents/works/obsidian_vault/diary/may.md")
}

def main():
    manager.match_response(questions["mood"])
    manager.writing_files(questions["write_day"])

main()