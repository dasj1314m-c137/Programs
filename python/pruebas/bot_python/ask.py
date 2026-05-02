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