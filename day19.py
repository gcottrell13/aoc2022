# day 19
from getinput import fetch_input

data = fetch_input(2022, 19)

data = """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
""".strip()

blueprints = []
for line in data.splitlines():
    parts = line.split()
    id = parts[1]
    ore_robot = int(parts[6])
    clay_robot = int(parts[12])
    obs_robot = int(parts[18]), int(parts[21])
    geode_robot = int(parts[27]), int(parts[30])
    blueprints.append((ore_robot, clay_robot, obs_robot, geode_robot))


def _state_to_bin(orebot, claybot, obsbot, geobot, ore, clay, obs, geo):
    return orebot + \
        claybot << 10 + \
        obsbot << 20 + \
        geobot << 30 + \
        ore << 40 + \
        clay << 50 + \
        obs << 60 + \
        geo << 70


def visit(budget: int, state: dict[int, int], mk_orebot, mk_claybot, mk_obsbot, mk_geobot):
    queue = [(budget, 1, 0, 0, 0, 0, 0, 0, 0)]

    while queue:
        time, orebot, claybot, obsbot, geobot, ore, clay, obs, geo = queue.pop(0)
        d = _state_to_bin(orebot, claybot, obsbot, geobot, ore, clay, obs, geo)

        state[d] = max(state.get(d, 0), geo)

        if time <= 0:
            continue

        if ore >= mk_geobot[0] and obs >= mk_geobot[1]:
            queue.append((time - 1, orebot, claybot, obsbot, geobot + 1,  # make geobot
                          ore + orebot - mk_geobot[0], clay + claybot,
                          obs + obsbot - mk_geobot[1], geo + geobot))

        if ore >= mk_obsbot[0] and clay >= mk_obsbot[1]:
            queue.append((time - 1, orebot, claybot, obsbot + 1, geobot,  # make obsbot
                          ore + orebot - mk_obsbot[0],
                          clay + claybot - mk_obsbot[1],
                          obs + obsbot, geo + geobot))

        if ore >= mk_claybot:
            queue.append((time - 1,  # -------------------------------------make claybot
                          orebot, claybot + 1, obsbot, geobot,
                          ore + orebot - mk_claybot, clay + claybot,
                          obs + obsbot, geo + geobot))

        elif ore >= mk_orebot:
            queue.append((time - 1, orebot + 1, claybot, obsbot, geobot,  # make orebot
                          ore + orebot - mk_orebot, clay + claybot,
                          obs + obsbot, geo + geobot))

        queue.append((time - 1, orebot, claybot, obsbot, geobot,  # ------- wait
                      ore + orebot, clay + claybot,
                      obs + obsbot, geo + geobot))

    return state


def getroutes(t):
    for i, blueprint in enumerate(blueprints):
        m = max(visit(t, {}, *blueprint).values())
        print(i + 1, m)
        yield (i + 1) * m


print(sum(getroutes(19)))
