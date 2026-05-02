import ask
import render
import search_response
import write_files
from datetime import date

def match_response(question):
    mood = ask.open_question(question[0])
    response = search_response.read_p(question[1], mood)
    render.show_match(response, question[1])

def writing_files(question):
    response = ask.questionSN(question[0])
    if response:
        d = date.today()
        writing = ask.open_question("Escribe: ")
        if writing == "exit":
            return None
        write_files.wadd_file(question[1], str(d) + "\n" + writing)