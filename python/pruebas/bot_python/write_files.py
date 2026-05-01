def add_response(path, pattern, reponse):
    with open(path, 'a') as f:
        f.write("\n" + pattern + "|" + reponse)

def wadd_file(path, content):
    with open(path, 'a') as f:
        f.write("\n" + content)