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
        if not isinstance(open_response, str) or not open_response:
            render.smooth_print("Por favor, escribe una respuesta válida.")
            continue
        else:
            return open_response

def select_option(options):
    while True:
        render.smooth_print("Lista:")
        for i, option in enumerate(options, 1):
            render.smooth_print(f"{i}. {option}")
        select = questionSN("¿Quieres seleccionar una opción?")
        if not select:
            return False
        try:
            choice = int(render.smooth_input("Ingresa el número de tu elección: "))
            if 1 <= choice <= len(options):
                return choice - 1 # Devuelve el índice de la opción seleccionada
            else:
                render.smooth_print("Número fuera de rango. Intenta nuevamente.")
        except ValueError:
            render.smooth_print("Entrada no válida. Por favor, ingresa un número.")