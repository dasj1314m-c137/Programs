import render

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

if __name__ == "__main__":
     response = read_p("mood_responses.txt", "feliz")
     render.show_match(response)