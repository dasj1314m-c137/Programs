#!/usr/bin/env python3
import sys

def add_breaklines(text):
    lines = text.splitlines()
    return '\n\n'.join(lines)

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding="utf-8") as f:
            text = f.read()
    else:
        if sys.stdin.isatty():
            sys.stdout.write('Ingresa texto (doble Enter para finalizar):\n')
            input_lines = []
            empty_count = 0
            while True:
                line = sys.stdin.readline()
                if not line:
                    break
                if line == '\n':
                    empty_count += 1
                    if empty_count == 2:
                        break
                    input_lines.append('')
                else:
                    empty_count = 0
                    input_lines.append(line.rstrip('\n'))
            text = '\n'.join(input_lines)
        else:
            text = sys.stdin.read()

    print(add_breaklines(text))

if __name__ == '__main__':
    main()
