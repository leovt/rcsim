from track import Track, StartHillUp, HillUp, Flat
from vmath import vec2
from rk4 import rk4

track = Track()
#track.append(Flat)
#track.append(Flat)
#track.append(Flat)
#track.append(StartHillUp)
#track.append(HillUp)
#track.append(HillUp)
#track.append(HillUp)
for _ in range(1000):
    track.append(Flat)

# simulate the pair s,s' , i.e. position and speed along the track

# y = (s,s')
# y' = (s', s'') = f(t, y)

gravity = vec2(0, -5.0) # one unit on the track is 2 meters
mu = 0.007
c = 0.0002

def f(t, y):
    s = y.x
    v = y.y

    T = track.T(s)

    # normal acceleration
    n = v*v*(track.x2(s) @ track.N(s)) - gravity @ track.N(s)

    friction = mu * abs(n) + c * v*v

    if v>0:
        sgn = 1
    else:
        sgn = -1

    # ignoring friction
    a = gravity @ T  -  sgn * friction

    return vec2(v, a)

def main():
    t = 0.0
    y = vec2(0.0, 5.0) # at position 0 with a speed of 10m/s
    h = 0.05

    while 0 <= y.x < track.length:
        pos = track.x(y.x)
        print(t, y.x, y.y, pos.x, pos.y, sep=',')
        y = rk4(f, t, y, h)
        t += h

if __name__ == '__main__':
    main()
