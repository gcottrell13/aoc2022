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


@functools.lru_cache
def get_shortest_path(start, end):
    if start == end:
        return 100000
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

flags = {x: 2 ** i for i, x in enumerate(valves.keys())}
flows = {x: v[0] for x, v in valves.items()}
paths = {x: {y: get_shortest_path(x, y) for y in flags} for x in flags}
g = {x: v for x, v in flows.items() if v > 0}


def get_max_flow(at: str, visited: int, values: dict[int, int], time: int, summ: int):
    values[visited] = max(values.get(visited, 0), summ)

    for valve in g:
        T = paths[at][valve]
        newtime = time - T - 1
        if not flags[valve] & visited and newtime >= 0:
            get_max_flow(valve, visited | flags[valve], values, int(newtime), summ + flows[valve] * newtime)

    return values


print(max(get_max_flow('AA', 0, {}, 30, 0).values()))
part2 = get_max_flow('AA', 0, {}, 26, 0)
print(max(
    v1 + v2
    for k1, v1 in part2.items()
    for k2, v2 in part2.items()
    if not k1 & k2
))
