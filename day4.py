
from getinput import fetch_input
data = fetch_input(2022, 4)


def get_sections(low, high):
    return set(range(int(low), int(high) + 1))

subsets = 0
overlaps = 0

for line in data.splitlines():
    range1r, range2r = line.split(',')
    range1 = get_sections(*range1r.split('-'))
    range2 = get_sections(*range2r.split('-'))
    
    if range1.issubset(range2) or range2.issubset(range1):
        subsets += 1
    if range1 & range2:
        overlaps += 1

print('number of subsets:', subsets)
print('number of overlaps:', overlaps)
