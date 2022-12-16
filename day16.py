# day 16
import functools

from getinput import fetch_input

data = fetch_input(2022, 16)
data1 = """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
""".strip()

valves = {}
valves_with_flow: list[str] = []


@functools.lru_cache
def get_shortest_path(start, end):
    visited = []
    queue: list[tuple[int, str]] = [(0, start)]
    while queue:
        dist, name = queue.pop(0)
        visited.append(name)
        if name == end:
            return dist
        for neighbor in valves[name][1]:
            if neighbor not in visited:
                queue.append((dist + 1, neighbor))


for line in data.splitlines():
    _, name, _, _, raw_rate, _, _, _, _, raw_neighbors = line.split(' ', maxsplit=9)
    rate = int(raw_rate[len('rate='):-1])
    neighbors: list[str] = raw_neighbors.split(', ')
    valves[name] = (rate, neighbors)
    if rate > 0:
        valves_with_flow.append(name)


def get_max_flow(at: str, visited: list[str], time: int):
    flow, _neighbors = valves[at]
    if time >= 30:
        return 0
    visited = visited + [at]

    neighbors = [
        (valve, valves[valve][0] / get_shortest_path(at, valve))
        for valve in valves_with_flow
        if valve != at and valve not in visited
    ]

    plans = sorted(neighbors, key=lambda x: x[1], reverse=True)[:3]
    remaining_time = 30 - time
    if plans:
        m = max(
            get_max_flow(name, visited, time + get_shortest_path(at, name) + 1)
            for name, _value in plans
        )
        released = flow * remaining_time
        # print(' '.join(visited), m, '+', flow, '* remaining', remaining_time)
        return m + released
    # print(' '.join(visited), '+', flow, '* remaining', remaining_time)
    return flow * remaining_time


flow = get_max_flow('AA', [], 0)
# flow = get_max_flow(['DD','BB','JJ','HH','EE','CC'])
print(flow)
