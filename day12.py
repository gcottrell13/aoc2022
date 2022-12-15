# day 12
from getinput import fetch_input

data = fetch_input(2022, 12)
data1 = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""".strip()

lines = data.splitlines()


class Path:
    def __init__(self, x, y, dir, dist, neighbor):
        self.neighbor = neighbor
        self.x = x
        self.y = y
        self.dir = dir
        self.dist = dist


def get_start_part1():
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == 'S':
                return x, y
    raise ValueError('did not find start')


def get_starts_part2():
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == 'S' or char == 'a':
                yield x, y


cant_reach_the_end = set()


def check_from_start_pos(start_x, start_y):
    path_lengths: dict[(int, int), Path] = {}  # [x, y] => Path
    frontier: list[(int, int, int)] = []  # (x, y, height value)

    frontier.append((start_x, start_y, ord('a')))
    path_lengths[start_x, start_y] = Path(start_x, start_y, 'S', 0, None)

    while frontier:
        x0, y0, height = frontier.pop(0)
        current_distance = path_lengths[x0, y0]
        if lines[y0][x0] == 'E':
            return current_distance
        for dx, dy, dstr in [(1, 0, '>'), (0, 1, 'v'), (-1, 0, '<'), (0, -1, '^')]:
            x = x0 + dx
            y = y0 + dy
            if x < 0 or y < 0 or x >= len(lines[0]) or y >= len(lines):
                continue
            v = lines[y][x]
            h = ord(v)
            if lines[y][x] == 'E':
                h = ord('z')
            if (x, y) in path_lengths:
                continue
            if h > height + 1:
                continue
            frontier.append((x, y, h))
            path_lengths[x, y] = Path(x, y, dstr, current_distance.dist + 1, current_distance)

    cant_reach_the_end.update(path_lengths.keys())


# p1x, p1y = get_start_part1()
# current_lowest = check_from_start_pos(p1x, p1y)

current_lowest = None
for x, y in get_starts_part2():
    if (x, y) in cant_reach_the_end:
        continue
    path = check_from_start_pos(x, y)
    if path and (current_lowest is None or path.dist < current_lowest.dist):
        current_lowest = path

dirmap = []
for line in lines:
    dirmap.append(['.'] * len(line))
c = current_lowest
marker = 'E'
while c:
    dirmap[c.y][c.x] = marker
    marker = c.dir
    c = c.neighbor

for line in dirmap:
    print(''.join(line))

print(current_lowest.dist)
