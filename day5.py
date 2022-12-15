
from getinput import fetch_input
data = fetch_input(2022, 5)

config, steps = data.split('\n\n')

config = config.splitlines()

num_buckets = len(config[-1].split())
state = [[] for _ in range(num_buckets)]

for line in reversed(config[:-1]):
    for stack_num, box in enumerate(line[1::4]):
        if box.strip():
            state[stack_num].append(box)

for i, s in enumerate(state):
    print(f'{i+1}: {s}')

for action in steps.splitlines():
    move, N, _from, src, _to, dest = action.split()
    N = int(N)
    src = int(src) - 1
    dest = int(dest) - 1
    # for _ in range(N):
    #     box = state[src].pop()
    #     state[dest].append(box)
    state[dest].extend(state[src][-N:])
    state[src] = state[src][:-N]


for i, s in enumerate(state):
    print(f'{i+1}: {s}')

print(''.join(map(lambda x: x[-1], state)))
