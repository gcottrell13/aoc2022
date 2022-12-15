
from getinput import fetch_input
data = fetch_input(2022, 6)

marker_size = 14

for i in range(marker_size, len(data)):
    if len(set(data[i-marker_size:i])) == marker_size:
        print(i)
        break
