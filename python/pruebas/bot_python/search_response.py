import render

def search(line, pattern):
    responses = line.split("|", 1)
    if not pattern == responses[0]:
        return False
    else:
        return responses[1]

def read(path, pattern):
    with open(path, 'r') as f:
        for line in f:
            answer = search(line, pattern)
            if answer:
                return answer
        return False

if __name__ == "__main__":
     response = read("mood_responses.txt", "feliz")
     render.show_match(response)