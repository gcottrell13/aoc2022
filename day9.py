# day 9

import sys
from getinput import fetch_input

data = fetch_input(2022, 9)
# data = """
# R 5
# U 8
# L 8
# D 3
# R 17
# D 10
# L 25
# U 20
# """.strip()


def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(other.x + self.x, other.y + self.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __len__(self):
        return abs(self.x) + abs(self.y)

    def norm(self):
        return Point(sign(self.x), sign(self.y))

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def set(self, x, y):
        self.x = x
        self.y = y


knots = []

for _ in range(10):
    knots.append(Point(0, 0))

dirs = {
    'u': Point(0, 1),
    'd': Point(0, -1),
    'l': Point(-1, 0),
    'r': Point(1, 0),
}

visited = []
visited.append((0, 0))

for line in data.splitlines():
    direction, count = line.split()
    delta = dirs[direction.lower()]

    for _ in range(int(count)):
        knots[0] += delta
        for previous, current_knot in zip(knots[:-1], knots[1:]):
            d = previous - current_knot
            if previous.x != current_knot.x and previous.y != current_knot.y:
                if len(d) >= 3:
                    new = current_knot + d.norm()
                    current_knot.set(new.x, new.y)
            elif len(d) > 1:
                new = current_knot + d.norm()
                current_knot.set(new.x, new.y)
            # print(direction, count, delta, H, T)
        visited.append((knots[-1].x, knots[-1].y))


lowest_x = min(p[0] for p in visited)
lowest_y = min(p[1] for p in visited)
highest_x = max(p[0] for p in visited)
highest_y = max(p[1] for p in visited)
grid = {}
for x, y in visited:
    grid.setdefault(y, {})[x] = '#'

for y in reversed(range(lowest_y, highest_y + 1)):
    for x in range(lowest_x, highest_x + 1):
        p = grid.get(y, {}).get(x, '.')
        sys.stdout.write(p)
    sys.stdout.write('\n')
    sys.stdout.flush()


# print("\n".join(map(str, visited)))
print(len(set(visited)))