# day 17
import itertools
import math

from getinput import fetch_input

data = fetch_input(2022, 17)

data1 = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

rock_text = """
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
""".strip()

WIDTH = 7

rocks = [list(reversed(n.splitlines())) for n in rock_text.split('\n\n')]
rock_maps = [
    sum(
        1 << (y * WIDTH + x)
        for y, row in enumerate(rock)
        for x, i in enumerate(row)
        if i == '#'
    )
    for rock in rocks
]

next_jet = 0

REMOVE_ROWS = 50
TRIGGER_REMOVE = 150

trigger = ((1 << WIDTH) - 1) << (TRIGGER_REMOVE * WIDTH)
remove = REMOVE_ROWS * WIDTH

removed_rows = 0

BOTTOM_ROW = (1 << WIDTH) - 1
state = 0


def get_jet():
    global next_jet
    while True:
        d = next_jet
        next_jet = (next_jet + 1) % len(data)
        yield data[d]


jets = get_jet()


def print_board(state: int, falling_rock: int = 0):
    line = ['|']
    rock_length = (falling_rock.bit_length() // WIDTH) * WIDTH + WIDTH
    state_length = (state.bit_length() // WIDTH) * WIDTH + WIDTH
    for i in reversed(range(max(rock_length, state_length))):
        s = 1 << i
        if falling_rock & s:
            line.append('@')
        elif state & s:
            line.append('#')
        else:
            line.append('.')
        if i % WIDTH == 0:
            line.append('|')
            print(''.join(reversed(line)))
            line = ['|']

    print('')


def do_rock(rock: int, rock_width: int, print_intermediate: bool):
    global state, removed_rows
    rocksize = rock.bit_count()
    x = 2
    rock <<= (3 + math.ceil(state.bit_length() / 7)) * 7 + x

    while True:

        if print_intermediate:
            print_board(state, rock)

        jet = next(jets)
        old_rock = rock
        old_x = x
        if jet == '<' and x > 0:
            rock >>= 1
            x -= 1
        if jet == '>' and x < WIDTH - rock_width:
            rock <<= 1
            x += 1

        if rock & state:
            rock = old_rock
            x = old_x

        newrock = rock >> WIDTH
        if newrock.bit_count() < rocksize:
            break
        if newrock & state:
            break
        rock = newrock

    state += rock
    if state & trigger:
        state >>= remove
        removed_rows += REMOVE_ROWS


TOTAL = int(1e12)
limit = TOTAL

height_at_beginning_of_cycle = 0
added_height_during_cycle = 0

cycle_length = 1
cache_i = {}
rev_cache_i = {}
cache_height = {}
data_length_bit_length = len(data).bit_length()

for i, _rock in enumerate(zip(itertools.cycle(rock_maps), itertools.cycle(rocks))):
    rock_map, rock = _rock
    if i % 1e6 == 0:
        print(i)
    if i >= limit:
        break

    do_rock(rock_map, len(rock[0]), False)

    c = ((state >> 700) << data_length_bit_length) + next_jet

    if state >> 700 and (n := cache_i.get(c)):
        cycle_length = i - n
        print(f'found cycle from', n, 'to', i, 'length', cycle_length)
        height = math.ceil(state.bit_length() / WIDTH)
        height_at_cycle = height + removed_rows
        print('found cycle at i=', i)
        height_at_beginning_of_cycle = cache_height[n]
        added_height_during_cycle = height_at_cycle - height_at_beginning_of_cycle
        number_of_cycles = (TOTAL - n) // cycle_length
        remaining_iterations = (TOTAL % cycle_length) - n
        extra_height = cache_height[n + remaining_iterations - 1] - height_at_beginning_of_cycle
        print('extra height', extra_height)
        print('number_of_cycles', number_of_cycles)
        print('total calculated iterations=', n + remaining_iterations + (number_of_cycles * cycle_length))
        print('block i:', i)
        print(i, 'height:', height_at_cycle)
        print_board(state >> max(0, ((state.bit_length() // WIDTH) - 10) * WIDTH))
        print('block n:', n)
        print('height at beginning of cycle:', height_at_beginning_of_cycle)
        print_board(rev_cache_i[n])
        print('one after:', n + 1)
        print(n + 1, 'height:', cache_height[n + 1])
        print_board(rev_cache_i[n + 1])
        print('remaining_iterations', remaining_iterations)
        print('height at extra i=', n + remaining_iterations, 'h=', cache_height[n + remaining_iterations])
        print(extra_height + height_at_beginning_of_cycle + (added_height_during_cycle * number_of_cycles))
        break
    else:

        cache_i[c] = i
        rev_cache_i[i] = state >> max(0, ((state.bit_length() // WIDTH) - 10) * WIDTH)
        cache_height[i] = math.ceil(state.bit_length() / WIDTH) + removed_rows


if added_height_during_cycle == 0:
    print_board(state, 0)
    height = math.ceil(state.bit_length() / WIDTH) + removed_rows
    print(height)
