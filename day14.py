# day 14
import math
import sys, time
from collections import defaultdict

from getinput import fetch_input

data = fetch_input(2022, 14)
data1 = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
""".strip()

last_window = ''


def output_window(s: str | list[str]):
    global last_window
    if isinstance(s, list):
        s = '\n'.join(s)
    # if last_window:
    #     sys.stdout.write('\b' * len(last_window))
    s += '\n\n'
    sys.stdout.write(s)
    sys.stdout.flush()
    last_window = s


SOURCE = (500, 0)

rocks: dict[int, set[int]] = defaultdict(set)
sand: dict[int, set[int]] = defaultdict(set)
min_x = 10000
max_x = 0
min_y = 0
max_y = 0

for line in data.splitlines():
    coords = list(map(lambda x: tuple(map(int, x.split(','))), line.split(' -> ')))
    for start, end in zip(coords[:-1], coords[1:]):
        x0, y0 = start
        x1, y1 = end
        dx = int(math.copysign(1, x1 - x0)) if x1 - x0 else 0
        dy = int(math.copysign(1, y1 - y0)) if y1 - y0 else 0
        dist = max(abs(x1 - x0), abs(y1 - y0)) + 1
        # print(start, end, dist)
        for _ in range(dist):
            rocks[x0].add(y0)
            if x0 < min_x:
                min_x = x0
            if x0 > max_x:
                max_x = x0
            if y0 < min_y:
                min_y = y0
            if y0 > max_y:
                max_y = y0
            x0 += dx
            y0 += dy


def print_config(current_sand: tuple[int, int]):
    for y in range(min_y, max_y + 1):
        line = []
        for x in range(min_x, max_x + 1):
            if (x, y) == current_sand:
                line.append('o')
            elif (x, y) == SOURCE:
                line.append('+')
            elif y in sand[x]:
                line.append('o')
            elif y in rocks[x]:
                line.append('#')
            elif y == max_y:
                line.append('#')
            else:
                line.append('.')
        yield ''.join(line)


max_y += 2
min_x -= 3
max_x += 3
output_window(list(print_config((0, 0))))


def is_empty(x, y):
    if y >= max_y:
        return False
    return y not in rocks[x] and y not in sand[x]


def run_simulation(delay: float):
    sands_at_rest = 0
    global min_x, max_x

    while True:
        current_sand = SOURCE
        while True:

            x, y = current_sand
            if delay > 0:
                time.sleep(delay)
                output_window(list(print_config(current_sand)))

            # if y > max_y:
            #     return sands_at_rest

            if x < min_x:
                min_x -= 3
            if x > max_x:
                max_x += 3

            if is_empty(x, y + 1):
                current_sand = (x, y + 1)
            elif is_empty(x - 1, y + 1):
                current_sand = (x - 1, y + 1)
            elif is_empty(x + 1, y + 1):
                current_sand = (x + 1, y + 1)
            else:
                sands_at_rest += 1
                sand[x].add(y)
                if current_sand == SOURCE:
                    return sands_at_rest
                break


r = run_simulation(0)
output_window(list(print_config((0, 0))))
print(r)
