from getinput import fetch_input
data = fetch_input(2022, 2)
total = 0

ROCK = 1
PAPER = 2
SCISSORS = 3
WIN = 6
LOSS = 0
TIE = 3
score = {
    'x': ROCK,
    'y': PAPER,
    'z': SCISSORS,
}

for line in data.splitlines():
    a, b = line.lower().split()
    total += score[b]
    match a:
        case 'a':
            total += {'x': TIE, 'y': WIN, 'z': LOSS}[b]
        case 'b':
            total += {'x': LOSS, 'y': TIE, 'z': WIN}[b]
        case 'c':
            total += {'x': WIN, 'y': LOSS, 'z': TIE}[b]

print(f'total score of incorrect decryption: {total}')

score = {
    'x': LOSS,
    'y': TIE,
    'z': WIN,
}
total = 0
for line in data.splitlines():
    a, b = line.lower().split()
    total += score[b]
    match a:
        case 'a':
            total += {'x': SCISSORS, 'y': ROCK, 'z': PAPER}[b]
        case 'b':
            total += {'x': ROCK, 'y': PAPER, 'z': SCISSORS}[b]
        case 'c':
            total += {'x': PAPER, 'y': SCISSORS, 'z': ROCK}[b]
print(f'total score of correct decryption: {total}')
