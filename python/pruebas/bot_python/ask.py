import render

def questionSN(question):
    while True:
        responseSN = ""
        responseSN = render.smooth_input(question + " (Si/No) ").lower()
        if responseSN != "si" and responseSN != "no":
            render.smooth_print("Por favor, responde con 'Si' o 'No'.")
            continue
        elif responseSN == "no":
            return False
        else:
            return True

def open_question(question):
    while True:
        open_response = render.smooth_input(question)
        if not open_response.strip():
            render.smooth_print("Por favor, ingresa una respuesta válida.")
            continue
        else:
            return open_response

def select_option(options, ask_select=True):
    while True:
        render.smooth_print("Lista:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        if ask_select:
            select = questionSN("¿Quieres seleccionar una opción?")
            if not select:
                return False
        try:
            choice = render.smooth_input("Ingresa el número de tu elección o ingresa 'exit' para salir: ")
            if choice.lower() == 'exit':
                return None
            choice = int(choice)
            if 1 <= choice <= len(options):
                return choice - 1 # Devuelve el índice de la opción seleccionada
            else:
                render.smooth_print("Número fuera de rango. Intenta nuevamente.")
        except ValueError:
            render.smooth_print("Entrada no válida. Por favor, ingresa un número.")