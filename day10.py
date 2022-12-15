# day 10
from getinput import fetch_input

data = fetch_input(2022, 10)

X = 1
cycle_number = 1

interesting_values = []

CRT = [[], [], [], [], [], []]


def check_cycle():
    if cycle_number % 40 == 20:
        # print('----', cycle_number, X)
        interesting_values.append(cycle_number * X)

    crt_line = (cycle_number - 1) // 40
    if abs(X - ((cycle_number - 1) % 40)) <= 1:
        CRT[crt_line].append('#')
    else:
        CRT[crt_line].append('.')


for cmd in data.splitlines():
    # print(cmd)
    match cmd.split():
        case ['addx', n]:
            check_cycle()
            cycle_number += 1
            check_cycle()
            cycle_number += 1
            X += int(n)
        case ['noop']:
            check_cycle()
            cycle_number += 1

print(sum(interesting_values[:6]))
for line in CRT:
    print(''.join(line))
