import os, pathlib

for i in range(25):
    fname = pathlib.Path(__file__).with_name(f'day{i+1}.py').absolute()
    if not os.path.exists(str(fname)):
        with open(fname, 'w') as f:
            f.write(f"""
# day {i+1}
from getinput import fetch_input
data = fetch_input(2022, {i+1})
""".strip())
