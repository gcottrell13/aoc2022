from getinput import fetch_input
data = fetch_input(2022, 1)
elfs = []

for chunk in data.split('\n\n'):
    elfs.append(sum(map(int, chunk.splitlines())))

print(f'max elf is: {max(elfs)}')
        
top_three = list(sorted(elfs))[-3:]

print(f'top three elfs: {sum(top_three)}')
