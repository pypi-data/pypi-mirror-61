import datetime


def get_snippet(path, from_line, to_line):

    with open(path, 'rb') as f:
        data = f.read().splitlines()

    snippet = [(line_number, data[line_number]) for line_number
               in range(from_line, to_line+1)]

    ts = str(datetime.datetime.now())

    return dict(snippet=snippet, ts=ts)


def print_snippet(snippet):

    print(snippet['ts'])
    for line_number, line in snippet['snippet']:
        print(line_number, line)
