import ask
import render
import search
import write_files
import utils
from datetime import date

def match_response(action):
    mood = ask.open_question(action["prompt"])
    response = search.read_p(action["path"], mood)
    render.show_match(response, action["path"])
    return True

def writing_files(action):
    response = ask.questionSN(action["prompt"])
    if response:
        d = date.today()
        writing = ask.open_question("Escribe: ")
        if writing == "exit":
            return None
        write_files.wadd_file(action["path"], str(d) + "\n" + writing)
        return True

def duesMD_render(action, task_path):
    dues = ask.questionSN("¿Quieres ver tus pendientes?")
    if dues:
        render.smooth_print(action["prompt"])
        with open(action["path"], 'r') as f:
            tasks = {}
            for line in f:
                key, value = search.getNH_md(line.strip())
                tasks[key] = value
            choice = ask.select_option(list(tasks.keys()))
            if choice is False:
                return None
            choice = utils.dic_index(tasks, choice)
            path = task_path + choice[1][0]
            content = search.getMD_block(path, choice[1][1])
            render.smooth_print(choice[1][2].strip() + "\n" + content.strip())

def daily_check():
    data = search.get_json_data("data/data.json")
    today = date.today().strftime("%d/%m/%y")
    if data["metadata"]["last_update"] != today:
        data["metadata"]["last_update"] = today
        for key in data["daily_status"]:
            data["daily_status"][key] = False
        utils.save_json_data("data/data.json", data)

def check_status_json(func, action):
    status = search.get_json_value("data/data.json", "daily_status", action["json_key"])
    if status:
        return None
    else:
        result = func()
        if result is None:
            return None
        write_files.set_var_json("data/data.json", "daily_status", action["json_key"], True)