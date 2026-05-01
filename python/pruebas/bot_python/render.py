import ask
import write_files
import time

def show_match(matches, path):
    if not matches:
        print("No hay coincidencias")
        add_response = ask.questionSN("Quieres añadir otra posible respuesta?")
        if add_response:
            new_pattern = input("Escribe la nueva etiqueta: ")
            new_response = input("Escribe la nueva respuesta: ")
            write_files.add_response(path, new_pattern, new_response)
    else:
        print(matches.strip())

def smooth_print(txt):
    for char in txt:
        print(char, end="", flush=True)
        time.sleep(0.05)
    print()

def smooth_input(txt):
    smooth_print(txt)
    return input()