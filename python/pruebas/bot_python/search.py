import json

def search_p(line, pattern):
    responses = line.split("|", 1)
    if not pattern == responses[0]:
        return False
    else:
        return responses[1]

def read_p(path, pattern):
    with open(path, 'r') as f:
        for line in f:
            answer = search_p(line, pattern)
            if answer:
                return answer
        return False

def getNH_md(content):
    content = content.replace("[", ",").replace("]", ",")
    content = content.replace(",", "", 3)
    content = content.replace("#", ",")
    content = content.split(",")
    key = " ".join(content)
    content[0] = f"{content[0]}.md"
    return key, content

def getMD_block(path, heading):
    with open(path, 'r') as f:
        for line in f:
            if line.startswith("## " + heading):
                block = []
                for line in f:
                    if line.startswith("## "):
                        break
                    block.append(line)
                return "".join(block)

def get_json_data(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def get_json_value(path, key1, key2):
    with open(path, 'r') as f:
        data = json.load(f)
    return data[key1][key2]

if __name__ == "__main__":
    clean = getNH_md("[[Recursos Socioemocional#Triptico Infografia Tabla]] miercoles 6 mayo")
    print(clean)