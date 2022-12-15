# day 11

from getinput import fetch_input

data = fetch_input(2022, 11)
data1 = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
""".strip()

monkey_info_text = data.split('\n\n')


def _mul_mod_dicts(one: dict[int, int], two: dict[int, int]):
    return {
        k: (v * two[k]) % k
        for k, v in one.items()
    }


def _add_mod_dicts(one: dict[int, int], two: dict[int, int]):
    return {
        k: (v + two[k]) % k
        for k, v in one.items()
    }


class Worry:

    @classmethod
    def from_int(cls, initial: int):
        return Worry({
            monkeyid: initial % monkey.divmodvalue()
            for monkeyid, monkey in monkeys.items()
        }, othermods={3: initial % 3, 2: initial % 2})

    def __init__(self, mods: dict[str, int], othermods: dict[int, int]):
        """mods: keyed by monkey id, what is the number mod their "divisible by" test value"""
        self.mods = mods
        self.othermods = othermods

    def __mul__(self, other):
        if isinstance(other, int):
            return Worry({
                k: (v * other) % monkeys[k].divmodvalue()
                for k, v in self.mods.items()
            }, _mul_mod_dicts(self.othermods, {k: other % k for k in self.othermods.keys()}))
        elif isinstance(other, Worry):
            return Worry({
                k: (v * other.mods[k]) % monkeys[k].divmodvalue()
                for k, v in self.mods.items()
            }, _mul_mod_dicts(self.othermods, other.othermods))

    def __mod__(self, other: int):
        othermod = self.othermods.get(other, None)
        if othermod is not None:
            return othermod
        for monkey in monkeys.values():
            if monkey.divmodvalue() == other:
                return self.mods[monkey.id]
        raise ValueError(f'cant do "% {other}", not enough info')

    def __add__(self, other):
        if isinstance(other, int):
            return Worry({
                k: (v + other) % monkeys[k].divmodvalue()
                for k, v in self.mods.items()
            },  _add_mod_dicts(self.othermods, {k: other % k for k in self.othermods.keys()}))
        elif isinstance(other, Worry):
            return Worry({
                k: (v + other.mods[k]) % monkeys[k].divmodvalue()
                for k, v in self.mods.items()
            }, _add_mod_dicts(self.othermods, other.othermods))

    def __floordiv__(self, other):
        return Worry.from_int(int(self) // other)


class Monkey:
    def __init__(self, id: str, starting_items: list[int], operation: str, test: str, iftrue: str, iffalse: str):
        self.id = id
        self.items = list(map(Worry.from_int, starting_items))
        self.operation = operation.split()[1:]
        self.test = test.split()[1:]
        self.iftrue = iftrue.split()[2:]
        self.iffalse = iffalse.split()[2:]
        self.inspections = 0

    def divmodvalue(self):
        return int(self.test[-1])

    def inspect_item(self):
        if len(self.items) == 0:
            return
        first, *rest = self.items
        first: Worry
        self.items = rest
        self.inspections += 1
        _new, _equal, one, op, two = self.operation
        match one:
            case 'old':
                lhs = first
            case _:
                lhs = int(one)
        match two:
            case 'old':
                rhs = first
            case _:
                rhs = int(two)
        match op:
            case '*':
                new = lhs * rhs
            case '+':
                new = lhs + rhs
            case _:
                raise ValueError(f'op {op} is invalid')
        # new = new // 3
        test1, _by, test2 = self.test
        match test1:
            case 'divisible':
                test_result = (new % int(test2) == 0)
            case _:
                raise ValueError(f'test {test1} is invalid')
        if test_result:
            self.throw_true(new)
        else:
            self.throw_false(new)

    def receive_item(self, new):
        self.items.append(new)  # % int(self.test[-1]))

    def throw_true(self, new):
        _throw, _to, _monkey, id = self.iftrue
        self.throw(new, id)

    def throw_false(self, new):
        _throw, _to, _monkey, id = self.iffalse
        self.throw(new, id)

    def throw(self, new, id):
        m = monkeys[id]
        m.receive_item(new)


monkeys: dict[str, Monkey] = {}

for chunk in monkey_info_text:
    monkeyid, items, op, test, iftrue, iffalse = chunk.replace(':', '').splitlines()
    _monkey, id = monkeyid.split()
    monkeys[id] = Monkey(
        id=id,
        starting_items=[],
        operation=op,
        test=test,
        iftrue=iftrue,
        iffalse=iffalse
    )

for chunk in monkey_info_text:
    monkeyid, items, op, test, iftrue, iffalse = chunk.replace(':', '').splitlines()
    _monkey, id = monkeyid.split()
    monkeys[id].items = list(map(lambda x: Worry.from_int(int(x.strip(','))), items.split()[2:]))

k = 0
for i in range(10_000):
    for id, monkey in monkeys.items():
        while monkey.items:
            k += 1
            # print(f'monkey {id} inspecting item on round {i}, {k}')
            monkey.inspect_item()

print('\n'.join([
    f'Monkey {id}: {monkey.inspections} inspections. items: {", ".join(map(str, monkey.items))}'
    for id, monkey in monkeys.items()
]))
secondmost, most = sorted(monkey.inspections for monkey in monkeys.values())[-2:]
print(f'two most active: {secondmost}, {most}')
print(f'product: {secondmost * most}')
