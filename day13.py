# day 13
from getinput import fetch_input

data = fetch_input(2022, 13)
data1 = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
""".strip()

PacketData = list[int | list]


def pad_list(alist, blist):
    if len(alist) < len(blist):
        return alist + [None] * (len(blist) - len(alist)), blist
    if len(alist) > len(blist):
        return alist, blist + [None] * (len(alist) - len(blist))
    return alist, blist


class Sorter:
    def __init__(self, item):
        if isinstance(item, str):
            item = eval(item)
        self.item = item

    def __lt__(self, other):
        return checklist(self.item, other.item)

    def __repr__(self):
        return repr(self.item)

    def __eq__(self, other):
        return other == self.item


def checklist(alist: PacketData, blist: PacketData, indent_level=0):
    indent = '  ' * indent_level

    def out(*msg: str):
        pass
        # print(indent + '- ', *msg)

    out(f'Compare {repr(alist)} vs {repr(blist)}')

    indent = '  ' * (indent_level + 1)

    for a, b in zip(*pad_list(alist, blist)):
        aislist = isinstance(a, list)
        bislist = isinstance(b, list)
        result = None

        if a is None:
            out('Left side ran out of items, so inputs are in the right order')
            result = True
        elif b is None:
            out('Right side ran out of items, so inputs are not in the right order')
            result = False
        elif aislist and not bislist:
            out(f'Compare {a} vs {b}')
            out(f'Mixed types; convert right to [{b}] and retry comparison')
            result = checklist(a, [b], indent_level + 2)
        elif not aislist and bislist:
            out(f'Compare {a} vs {b}')
            out(f'Mixed types; convert left to [{a}] and retry comparison')
            result = checklist([a], b, indent_level + 2)
        elif not aislist and not bislist:
            out(f'Compare {a} vs {b}')
            if a > b:
                out(f'  Right side is smaller, so inputs are not in the right order')
                result = False
            if a < b:
                out(f'  Left side is smaller, so inputs are in the right order')
                result = True
        else:
            result = checklist(a, b, indent_level + 2)

        if result is not None:
            return result

    return None


in_correct_order = 0
for index, packet in enumerate(data.split('\n\n')):
    first, second = map(eval, packet.splitlines())
    first: PacketData
    second: PacketData
    # print(f'\n== Pair {index + 1} ==')
    if checklist(first, second):
        in_correct_order += index + 1

print(in_correct_order)

part_2_data = data + """
[[2]]
[[6]]
"""

all_packets = [
    Sorter(packet)
    for packet in part_2_data.splitlines()
    if packet
]

all_packets.sort()

for p in all_packets:
    print(p)

div1 = all_packets.index([[2]]) + 1
div2 = all_packets.index([[6]]) + 1
print(div1, div2, div1 * div2)
