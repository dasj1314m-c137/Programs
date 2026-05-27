import ask
import write_files
import time
import random

def show_match(matches, path):
    if not matches:
        smooth_print("No hay coincidencias")
        add_response = ask.questionSN("Quieres añadir otra posible respuesta?")
        if add_response:
            new_pattern = smooth_input("Escribe la nueva etiqueta: ")
            new_response = smooth_input("Escribe la nueva respuesta: ")
            write_files.add_response(path, new_pattern, new_response)
    else:
        smooth_print(matches)

def smooth_print(txt):
    for char in txt:
        print(char, end="", flush=True)
        time.sleep(random.uniform(0.02, 0.06))
    print()

def smooth_input(txt):
    print(txt)
    try:
        return input()
    except KeyboardInterrupt:
        print()
        return None
