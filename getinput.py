session_id = ''
import requests, io

with open('session_id', 'r') as f:
    session_id = f.read()


def fetch_input(year, day):
    url = f'https://adventofcode.com/{year}/day/{day}/input'
    headers = {'Cookie': f'session={session_id}'}
    response = requests.get(url, headers=headers)
    return response.text.strip()


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        x, y = other
        return Point(self.x + x, self.y + y)

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        x, y = other
        return Point(self.x - x, self.y - y)

    def __eq__(self, other):
        if isinstance(other, Point):
            return (self.x, self.y) == (other.x, other.y)
        return (self.x, self.y) == other

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __iter__(self):
        return iter((self.x, self.y))

    @property
    def yx(self):
        return Point(self.y, self.x)

    def manhattan(self):
        return abs(self.x) + abs(self.y)
