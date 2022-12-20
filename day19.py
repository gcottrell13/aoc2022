# day 19
import math

from getinput import fetch_input

data = fetch_input(2022, 19)

data1 = """
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
    blueprints.append((int(id[:-1]), ore_robot, clay_robot, obs_robot, geode_robot))


def _state_to_bin(time, orebot, claybot, obsbot, geobot, ore, clay, obs, geo, trace):
    return time, orebot, claybot, obsbot, geobot, ore, clay, obs, geo, trace
    return orebot + \
        (claybot << 10) + \
        (obsbot << 20) + \
        (geobot << 30) + \
        (ore << 40) + \
        (clay << 50) + \
        (obs << 60) + \
        (geo << 70) + \
        (time << 90)


def _bin_to_state(d):
    time, orebot, claybot, obsbot, geobot, ore, clay, obs, geo, trace = d
    return time, orebot, claybot, obsbot, geobot, ore, clay, obs, geo, trace
    orebot = d & 0b1111111111
    claybot = d >> 10 & 0b1111111111
    obsbot = d >> 20 & 0b1111111111
    geobot = d >> 30 & 0b1111111111
    ore = d >> 40 & 0b1111111111
    clay = d >> 50 & 0b1111111111
    obs = d >> 60 & 0b1111111111
    geo = d >> 70 & 0b1111111111
    time = d >> 90 & 0b1111111111
    return time, orebot, claybot, obsbot, geobot, ore, clay, obs, geo


import sys


def out(n: int):
    s = str(n)
    sys.stdout.write('\r' + s + ' ')


def visit(budget: int, state: dict[int, int], mk_orebot, mk_claybot, mk_obsbot, mk_geobot):
    queue = [_state_to_bin(budget, 1, 0, 0, 0, 0, 0, 0, 0, '')]
    best = 0
    while queue:
        d = queue.pop(0)
        time, orebot, claybot, obsbot, geobot, ore, clay, obs, geo, trace = _bin_to_state(d)
        if len(queue) > 10000 and len(queue) % 100 == 0:
            out(len(queue))

        if geo > best:
            best = geo
            state[trace] = max(state.get(trace, 0), geo)
        if time <= 0:
            continue

        # make geobot
        step = math.ceil(max(0, (mk_geobot[0] - ore) / orebot, (mk_geobot[1] - obs) / max(1, obsbot))) + 1
        if time > step and obsbot:
            queue.append(_state_to_bin(time - step,
                                       orebot, claybot, obsbot,
                                       geobot + 1,  # make geobot
                                       ore + (orebot * step) - mk_geobot[0], clay + claybot * step,
                                       obs + (obsbot * step) - mk_geobot[1], geo + geobot * step, trace + 'g'))

        step = math.ceil(max(0, (mk_obsbot[0] - ore) / orebot, (mk_obsbot[1] - clay) / max(1, claybot))) + 1
        if time > step and claybot and obsbot < mk_geobot[1]:
            queue.append(_state_to_bin(time - step, orebot, claybot, obsbot + 1, geobot,  # make obsbot
                                       ore + orebot * step - mk_obsbot[0],
                                       clay + claybot * step - mk_obsbot[1],
                                       obs + obsbot * step, geo + geobot * step, trace + 'o'))

        step = math.ceil(max(0, (mk_claybot - ore) / orebot)) + 1
        if time > step and claybot < mk_obsbot[1]:
            queue.append(_state_to_bin(time - step,  # -------------------------------------make claybot
                                       orebot, claybot + 1, obsbot, geobot,
                                       ore + orebot * step - mk_claybot, clay + claybot * step,
                                       obs + obsbot * step, geo + geobot * step, trace + 'c'))

        step = math.ceil(max(0, (mk_orebot - ore) / orebot)) + 1
        if time > step and orebot < max(mk_orebot, mk_claybot, mk_geobot[0], mk_obsbot[0]):
            queue.append(_state_to_bin(time - step, orebot + 1, claybot, obsbot, geobot,  # make orebot
                                       ore + orebot * step - mk_orebot, clay + claybot * step,
                                       obs + obsbot * step, geo + geobot * step, trace + 'r'))

        queue.append(_state_to_bin(0, orebot, claybot, obsbot, geobot,  # wait
                                   ore + orebot * step, clay + claybot * step,
                                   obs + obsbot * step, geo + geobot * time, trace + 'w'))

    return best


def getroutes(t):
    for blueprint in blueprints:
        state = {}
        id, mk_orebot, mk_claybot, mk_obsbot, mk_geobot = blueprint
        m = visit(t, state, mk_orebot, mk_claybot, mk_obsbot, mk_geobot)
        print(id, m)
        yield id * m


print(sum(getroutes(24)))
