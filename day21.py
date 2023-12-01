# day 21
from getinput import fetch_input

data = fetch_input(2022, 21)

monkeys = {}

for line in data.splitlines():
    name, *job = line.split()
    monkeys[name[:-1]] = job


def get_monkey_value(name: str):
    if name == 'humn':
        return 'h'

    job = monkeys[name]

    if len(job) == 1:
        return int(job[0])

    a, op, b = job
    ar, br = get_monkey_value(a), get_monkey_value(b)

    if name == 'root':
        return f'{ar} = {br}'

    if op == '+':
        if isinstance(ar, str) or isinstance(br, str):
            return f'({ar} + {br})'
        return ar + br
    if op == '-':
        if isinstance(ar, str) or isinstance(br, str):
            return f'({ar} - {br})'
        return ar - br
    if op == '*':
        if isinstance(ar, str) or isinstance(br, str):
            return f'({ar} * {br})'
        return ar * br
    if op == '/':
        if isinstance(ar, str) or isinstance(br, str):
            return f'({ar} / {br})'
        return ar // br


print(get_monkey_value('root'))
