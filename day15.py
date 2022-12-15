# day 15
import math

from getinput import fetch_input, Point

data = fetch_input(2022, 15)
data = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
""".strip()

part_1 = False
print_grid = True
part_1_y = 2_000_000
part_2_max = 4_000_000


class Sensor:
    def __init__(self, pos: Point, beacon: Point):
        self.pos = pos
        self.beacon = beacon
        self.distance = (pos - beacon).manhattan()


sensors: list[Sensor] = []
row_part_1 = set()

for line in data.splitlines():
    _, _, sx, sy, _, _, _, _, bx, by = line.split()
    _, sensor_x = sx.strip(',').split('=')
    _, sensor_y = sy.strip(':').split('=')
    _, beacon_x = bx.strip(',').split('=')
    _, beacon_y = by.split('=')
    print(line)
    sensor = Sensor(
        pos=Point(int(sensor_x), int(sensor_y)),
        beacon=Point(int(beacon_x), int(beacon_y)),
    )
    sensors.append(sensor)

    if part_1 and abs(sensor.pos.y - part_1_y) <= sensor.distance:
        min_x = int(min(
            sensor.pos.x + math.copysign(sensor.distance - abs(sensor.pos.y - part_1_y), sign)
            for sign in [1, -1]
        ))

        max_x = int(max(
            sensor.pos.x + math.copysign(sensor.distance - abs(sensor.pos.y - part_1_y), sign)
            for sign in [1, -1]
        ))
        for x in range(min_x, max_x + 1):
            c = Point(x, part_1_y)
            for sensor in sensors:
                in_sensor_range = (sensor.pos - c).manhattan() <= sensor.distance
                if in_sensor_range and (x, part_1_y) != sensor.beacon:
                    row_part_1.add((x, part_1_y))
    print(f'\tfinished')

if print_grid:
    _x = [
        sensor.pos.x + math.copysign(sensor.distance, sign)
        for sensor in sensors
        for sign in [1, -1]
    ]
    _y = [
        sensor.pos.y + math.copysign(sensor.distance, sign)
        for sensor in sensors
        for sign in [1, -1]
    ]
    min_x = int(min(_x)) - 1
    max_x = int(max(_x)) + 1
    min_y = int(min(_y)) - 1
    max_y = int(max(_y)) + 1
    print(min_x, max_x, min_y, max_y)

    y_axis_size = max(len(str(min_y)), len(str(max_y)))
    x_axis_size = max(len(str(min_x)), len(str(max_x)))
    x_markers = {
        n: list(str(n).rjust(x_axis_size))
        for n in range(min_x - min_x % 5, max_x + 1, 5)
    }


    def print_line(line: list[str], y_value=None):
        col_padding = ' '
        pre = ' ' * y_axis_size
        if y_value is not None:
            pre = str(y_value).rjust(y_axis_size)
        print(pre, col_padding.join(line))


    for r in range(x_axis_size):
        line = []
        for n in range(min_x, max_x + 1):
            line.append(x_markers.get(n, [' '] * x_axis_size)[r])
        print_line(line)

    for y in range(min_y, max_y + 1):
        line = []
        for x in range(min_x, max_x + 1):
            p = Point(x, y)
            marker = '.'
            for sensor in sensors:
                if p == sensor.beacon:
                    marker = 'B'
                elif p == sensor.pos:
                    marker = 'S'
                elif (sensor.pos - p).manhattan() <= sensor.distance:
                    marker = '~'
                else:
                    continue
                break
            line.append(marker)
        print_line(line, y)

if part_1:
    print(len(row_part_1))
else:
    def find_hole():
        for x in range(0, part_2_max + 1):
            if x % 100000 == 0:
                print(x)
            pos = Point(x, 0)
            # print(pos)
            while pos.y < part_2_max:
                # print(pos, '<', part_2_max)
                for sensor in sensors:
                    # print('\tsensor at', sensor.pos, sensor.distance, (sensor.pos - pos).manhattan())
                    if (sensor.pos - pos).manhattan() <= sensor.distance:
                        distance_to_sensor_y = sensor.distance - abs(sensor.pos.x - x)
                        next_y = distance_to_sensor_y + sensor.pos.y + 1
                        pos = Point(x, next_y)
                        # print(f'\t\tjump to', pos)
                        break
                else:
                    if pos.y < part_2_max:
                        return pos


    x, y = find_hole()
    print(x * 4_000_000 + y)
