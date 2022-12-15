
from getinput import fetch_input
data = fetch_input(2022, 7)
MAX_SPACE = 70000000
NEED_SPACE = 30000000

all_directories = []
def directory(name, parent):
    if parent:
        name = f'{parent["__name"]}/{name}'
    d = {'..': parent, '__size': 0, '__name': name}
    all_directories.append(d)
    return d

root = directory('', None)
cwd_dict = root

stream = data.splitlines()
current_line = 0

def cd(to):
    global cwd_dict
    match to:
        case '/':
            cwd_dict = root
        case _:
            cwd_dict = cwd_dict[to]


def add_size(size, directory):
    directory['__size'] += size
    if directory['..']:
        add_size(size, directory['..'])


def ls():
    while (line := nextline()) and not line[0] == '$':
        type, name, *_ = line
        if type == 'dir':
            cwd_dict[name] = directory(name, cwd_dict)
        else:
            size = int(type)
            cwd_dict[name] = size
            add_size(size, cwd_dict)
    rewind()
            
        

def nextline():
    global current_line
    current_line += 1
    try:
        return stream[current_line].split()
    except IndexError:
        raise StopIteration()

def rewind():
    global current_line
    current_line -= 1


def process():
    _prompt, cmd, *args = nextline()
    match cmd:
        case 'cd':
            cd(*args)
        case 'ls':
            ls()
            
            
while True:
    try:
        process()
    except StopIteration:
        break

def print_dir(directory):
    d = {}
    for k, v in directory.items():
        if k == '..':
            continue
        elif isinstance(v, dict):
            d[k] = f'dir (size={v["__size"]})'
        else:
            d[k] = v
    return d
        
    
small_directories = [
    print_dir(d)
    for d in all_directories
    #if d['__size'] <= 100_000
]
print("\n".join(map(str, small_directories)))
print(sum(
d['__size'] for d in small_directories
))
current_empty_space = MAX_SPACE - root['__size']
need_to_delete = NEED_SPACE - current_empty_space
larger_dirs = [
    d['__size']
    for d in all_directories
    if d['__size'] >= need_to_delete
]
print(sorted(larger_dirs)[0])
