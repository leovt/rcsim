from math import sqrt, asinh
import bisect
from vmath import vec2

SQRT_HALF = sqrt(0.5)

class Flat:
    @staticmethod
    def x(s):
        return vec2(s, 0)

    @staticmethod
    def x1(s):
        return vec2(1, 0)

    @staticmethod
    def x2(s):
        return vec2(0, 0)

    T = x1

    @staticmethod
    def N(s):
        return vec2(0, 1)

    length = 1
    endpoint = vec2(1, 0)


class StartHillUp:
    @staticmethod
    def x(s):
        u = s*0.9
        for _ in range(3):
            # Newton iteration to find the x-value for a given arc length s
            dl = sqrt(u*u+1)
            arclength = 0.5*(u*dl+asinh(u))
            u -= (arclength-s) / dl
        return vec2(u, 0.5*u*u)

    @staticmethod
    def x1(s):
        u = StartHillUp.x(s).x
        f = 1.0 / sqrt(u*u+1)
        return vec2(f, f*u)

    @staticmethod
    def x2(s):
        u = StartHillUp.x(s).x
        f = 1.0 / (u*u+1)**2
        return vec2(-u*f, f)

    T = x1

    @staticmethod
    def N(s):
        u = StartHillUp.x(s).x
        f = 1.0 / sqrt(u*u+1)
        return vec2(-f*u, f)

    length = 0.5*(sqrt(2)+asinh(1))
    endpoint = vec2(1, 0.5)

class HillUp:
    @staticmethod
    def x(s):
        return vec2(s * SQRT_HALF, s * SQRT_HALF)

    @staticmethod
    def x1(s):
        return vec2(SQRT_HALF, SQRT_HALF)

    @staticmethod
    def x2(s):
        return vec2(0, 0)

    T = x1

    @staticmethod
    def N(s):
        return vec2(-SQRT_HALF, SQRT_HALF)

    length = sqrt(2)
    endpoint = vec2(1, 1)


class Track:
    def __init__(self):
        self.elements = []
        self.lengths = []
        self.pos = vec2()
        self.length = 0.0

    def append(self, el):
        self.elements.append((el, self.pos, self.length))
        self.length += el.length
        self.lengths.append(self.length)
        self.pos += el.endpoint

    def x(self, s):
        i = bisect.bisect_left(self.lengths, s)
        el, pos, ds = self.elements[i]
        elx = el.x(s-ds)
        return pos + elx

    def x1(self, s):
        i = bisect.bisect_left(self.lengths, s)
        el, pos, ds = self.elements[i]
        return el.x1(s-ds)

    def x2(self, s):
        i = bisect.bisect_left(self.lengths, s)
        el, pos, ds = self.elements[i]
        return el.x2(s-ds)

    def T(self, s):
        i = bisect.bisect_left(self.lengths, s)
        el, pos, ds = self.elements[i]
        return el.T(s-ds)

    def N(self, s):
        i = bisect.bisect_left(self.lengths, s)
        el, pos, ds = self.elements[i]
        return el.N(s-ds)

def test():
    track = Track()
    track.append(Flat)
    track.append(Flat)
    track.append(Flat)
    track.append(StartHillUp)
    track.append(HillUp)
    track.append(HillUp)
    track.append(HillUp)

    s = 0.0
    print(', '.join(['s', 'x1', 'x2', 'x\'1', 'x\'2', 'x"1', 'x"2', 'T1', 'T2', 'N1', 'N2']))
    while s < track.length:
        print(s, track.x(s).x, track.x(s).y,
                 track.x1(s).x, track.x1(s).y,
                 track.x2(s).x, track.x2(s).y,
                 track.T(s).x, track.T(s).y,
                 track.N(s).x, track.N(s).y,
              sep = ', ')
        s += 0.1

if __name__ == '__main__':
    test()
