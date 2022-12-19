# day 18
from getinput import fetch_input

data = fetch_input(2022, 18)

data1 = """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5

""".strip()


def _to_bitwise(x, y, z):
    x += 1
    y += 1
    z += 1
    if x < 0 or y < 0 or z < 0:
        return 0
    dx = (max_y + 2) * (max_z + 2) * x
    dy = (max_z + 2) * y
    # print(x, y, z, dx, dy)
    return 1 << (dx + dy + z)


blocks = set()
max_x = 0
max_y = 0
max_z = 0
for line in data.splitlines():
    x, y, z = map(int, line.split(','))
    blocks.add((x, y, z))
    if x > max_x:
        max_x = x
    if y > max_y:
        max_y = y
    if z > max_z:
        max_z = z

reachable_from_surface = []
visited = 0
frontier = [(-1, -1, -1)]

print('max', max_x, max_y, max_z)

max_x += 1
max_y += 1
max_z += 1
#
# for x in range(-1, max_x + 1):
#     for y in range(-1, max_y + 1):
#         for z in range(-1, max_z + 1):
#             print(x, y, z, '---', _to_bitwise(x, y, z))

blocks_bits = 0
for x, y, z in blocks:
    d = _to_bitwise(x, y, z)
    # print('block bits', x, y, z, d)
    blocks_bits |= d

while frontier:
    x, y, z = frontier.pop(0)
    d = _to_bitwise(x, y, z)
    if blocks_bits & d:
        # print('block at', x, y, z, d)
        continue
    if visited & d:
        continue
    visited |= d
    reachable_from_surface.append((x, y, z))
    if x > -1:
        frontier.append((x - 1, y, z))
    if x < max_x:
        frontier.append((x + 1, y, z))
    if y > -1:
        frontier.append((x, y - 1, z))
    if y < max_y:
        frontier.append((x, y + 1, z))
    if z > -1:
        frontier.append((x, y, z - 1))
    if z < max_z:
        frontier.append((x, y, z + 1))

surface_area = 0

# for x in range(-1, max_x + 2):
#     for y in range(-1, max_y + 2):
#         for z in range(-1, max_z + 2):
#             if (x, y, z) in blocks:
#                 continue
for x, y, z in reachable_from_surface:
    surface_area += int(_to_bitwise(x - 1, y, z) & blocks_bits).bit_count() + \
                    int(_to_bitwise(x + 1, y, z) & blocks_bits).bit_count() + \
                    int(_to_bitwise(x, y - 1, z) & blocks_bits).bit_count() + \
                    int(_to_bitwise(x, y + 1, z) & blocks_bits).bit_count() + \
                    int(_to_bitwise(x, y, z - 1) & blocks_bits).bit_count() + \
                    int(_to_bitwise(x, y, z + 1) & blocks_bits).bit_count()
print(surface_area)
