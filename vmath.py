from math import hypot

class vec2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return vec2(self.x * other, self.y * other)

    __rmul__ = __mul__

    def __matmul__(self, other):
        return self.x * other.x + self.y * other.y

    def __repr__(self):
        return 'vec2(%r, %r)' % (self.x, self.y)

    def __str__(self):
        return '(%s, %s)' % (self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __neq__(self, other):
        return not self == other

    def __abs__(self):
        return hypot(self.x, self.y)
