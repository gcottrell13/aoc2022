# day 20
from getinput import fetch_input

data = fetch_input(2022, 20)

data = """
15
2
-10
3
-2
0
4
""".strip()


class Node:
    def __init__(self, value: int, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next

    def set_next(self, other):
        # print('swapping', self, other)
        # print('\tother:', other.prev, other, other.next)
        # print('\tself:', self.prev, self, self.next)

        if other == self.prev:
            other.prev.next = self
            self.next.prev = other
            other.next = self.next
            self.prev = other.prev
            self.next = other
            other.prev = self
        elif other == self.next:
            pass
        else:
            other.prev.next = other.next
            other.next.prev = other.prev
            self.next.prev = other
            other.next = self.next
            self.next = other
            other.prev = self

        # print('\tresult')
        # print('\tother:', other.prev, other, other.next)
        # print('\tself:', self.prev, self, self.next)

    def __str__(self):
        return f'[{self.value}]'

    def __iter__(self):
        c = self
        while True:
            yield c.value
            c = c.next
            if c == self:
                break


nodes = []
zero = None
first = None
for line in data.splitlines():
    prev = nodes[-1] if nodes else None
    node = Node(int(line), prev)
    if prev:
        prev.next = node
    else:
        first = node
    nodes.append(node)
    if line == '0':
        zero = node

print('number of nodes before mix', len(nodes))

nodes[0].prev = nodes[-1]
nodes[-1].next = nodes[0]

if len(nodes) <= 10:
    print(', '.join(map(str, first)), '\n')

for node in list(nodes):
    current = node

    if node.value == 0:
        print('0 does not move\n')
        continue

    if node.value < 0:
        r = (node.value % len(nodes)) - 1
    else:
        r = node.value % len(nodes)

    for _ in range(r):
        current = current.next

    print(node.value, f'(%{len(nodes)}={r})', 'moves between', current, current.next)
    if len(nodes) <= 10:
        if current != node:
            current.set_next(node)
        else:
            print('but no movement')
        print(', '.join(map(str, first)), '\n')

# print(', '.join(map(str, nodes[0])))
if not zero:
    zero = first

t = list(zero)
print(len(t), t[:20])
first = 1000 % len(t)
second = 2000 % len(t)
third = 3000 % len(t)
print('indexes', first, second, third)
items = t[first], t[second], t[third]
print(items)
print(sum(items))
