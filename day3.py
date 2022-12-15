
from getinput import fetch_input
data = fetch_input(2022, 3)

sacks = data.splitlines()
step_1_answer = 0

def get_prio(letter):
    if letter.lower() == letter:
        return ord(letter) - (ord('a') - 1)
    else:
        return ord(letter) - (ord('A') - 1) + 26

for line in sacks:
    sack1 = line[:len(line) // 2]
    sack2 = line[len(line) // 2:]

    common_item = list(set(sack1) & set(sack2))[0]

    step_1_answer += get_prio(common_item)

print('step 1', step_1_answer)


step_2_answer = 0
for one, two, three in zip(
    sacks[::3],
    sacks[1::3],
    sacks[2::3]
):
    step_2_answer += get_prio(list(set(one)&set(two)&set(three))[0])

print('step 2', step_2_answer)
