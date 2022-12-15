import sys
from getinput import fetch_input

data = """
30373
25512
65332
33549
35390
""".strip()
data = fetch_input(2022, 8)

lines = data.splitlines()
visible_tree_count = 0
width = len(lines[0])
height = len(lines)

lines = [
    list(map(int, line))
    for line in lines
]


def fmttree(t, dir):
    return f' {t}{dir}'


def is_tree_visible(t, x0, y0):
    if y0 == 0 or y0 == height - 1 or x0 == 0 or x0 == width - 1:
        return fmttree(t, 'X')

    for dx, dy, direction in [
        (1, 0, '>'), (0, 1, 'V'), (-1, 0, '<'), (0, -1, '^')
    ]:
        x = x0
        y = y0
        while True:
            x += dx
            y += dy
            if y < 0 or y >= height or x < 0 or x >= width:
                return fmttree(t, direction)
            if lines[y][x] >= t:
                break
    return False


def tree_score(t, x0, y0):
    if y0 == 0 or y0 == height - 1 or x0 == 0 or x0 == width - 1:
        return 0
    score = 1
    for dx, dy, direction in [
        (1, 0, '>'), (0, 1, 'V'), (-1, 0, '<'), (0, -1, '^')
    ]:
        x = x0
        y = y0
        d = 0
        while True:
            x += dx
            y += dy
            d += 1
            if y < 0 or y >= height or x < 0 or x >= width:
                d -= 1
                break
            if lines[y][x] >= t:
                break
        score *= d
    return score


# for y, line in enumerate(lines):
#     for x, tree in enumerate(line):
#         visible = is_tree_visible(tree, x, y)
#         sys.stdout.write(visible or fmttree(tree, '_'))
#         if visible:
#             visible_tree_count += 1
#     sys.stdout.write('\n')

print(visible_tree_count)
print(max(
    tree_score(tree, x, y)
    for y, line in enumerate(lines)
    for x, tree in enumerate(line)
))
