import json

def dump_to_json(data, out_file):
    with open(out_file, 'w') as fd:
        json.dump(data, fd)

def load_from_json(json_file):
    with open(json_file, 'r') as fd:
        return json.load(fd)

def printgreen(s):
    print('\x1b[6;30;42m' + s + '\x1b[0m')

def printhigh(s):
    print('\x1b[6;30;47m' + s + '\x1b[0m')

def printred(s):
    print('\x1b[6;30;41m' + s + '\x1b[0m')

def printerror(s):
    print('\x1b[6;30;43m' + s + '\x1b[0m')

def cprint(s, color):
    if color == 'g':
        printgreen(s)
    elif color == 'r':
        printred(s)
    elif color == 'err':
        printerror(s)
    elif color == 'hi':
        printhigh(s)
    else:
        print(s)