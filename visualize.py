import tkinter
import time

from track import *
from rk4 import rk4
from vmath import vec2

track = Track()
track.append(Flat)
track.append(Flat)
track.append(Flat)
track.append(StartHillUp)
track.append(HillUp)
track.append(HillUp)
track.append(HillUp)

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

class Simulator:
    def __init__(self):
        self.t = 0.0
        self.y = vec2(0.0, 5.5) # at position 0 with a speed of 10m/s
        self.t_old = self.t-1
        self.y_old = self.y

    def state_at(self, t):
        if self.t_old > t:
            raise ValueError

        h = 0.1

        while self.t < t:
            self.t_old = self.t
            self.y_old = self.y
            self.y = rk4(f, self.t, self.y, h)
            self.t += h

        y = 1.0 / (self.t - self.t_old)*(self.y_old * (self.t - t) + self.y * (t - self.t_old))
        return track.x(y.x), y.x, y.y, f(t,y).y, track.T(y.x), track.N(y.x)





def main():
    tk = tkinter.Tk()
    canvas = tkinter.Canvas(tk, width=400, height=300)
    canvas.pack()

    for i in range(10):
        canvas.create_line((0, 40*i+20, 400, 40*i+20), fill='grey')
        canvas.create_line((40*i, 0, 40*i, 300), fill='grey')



    s = 0.0
    coords = [40, 400]
    while s < track.length:
        p = track.x(s)
        coords.append(p.x*40 + 40)
        coords.append(260 - p.y*40)
        s += 0.1
    p = track.pos
    coords.append(p.x*40 + 40)
    coords.append(260 - p.y*40)
    coords.append(p.x*40 + 40)
    coords.append(400)



    canvas.create_polygon(coords, fill='', outline='black')
    canvas.create_polygon((0,0,0,0), fill='red', outline='black', tag='car')

    after_ids = []

    def stop():
        while after_ids:
            tk.after_cancel(after_ids.pop())

    pos = tkinter.StringVar()
    speed = tkinter.StringVar()
    accel = tkinter.StringVar()

    tkinter.Label(tk, textvariable=pos).pack()
    tkinter.Label(tk, textvariable=speed).pack()
    tkinter.Label(tk, textvariable=accel).pack()

    def start():
        sim = Simulator()
        t0 = time.perf_counter()

        def update():
            t = time.perf_counter() - t0
            p, s, v, a, T, N = sim.state_at(t)
            ra = p - T*0.2 - N*0.1
            rb = p + T*0.2 - N*0.1
            rc = p + T*0.2 + N*0.1
            rd = p - T*0.2 + N*0.1
            canvas.coords('car',
                ra.x*40 + 40, 260-ra.y*40,
                rb.x*40 + 40, 260-rb.y*40,
                rc.x*40 + 40, 260-rc.y*40,
                rd.x*40 + 40, 260-rd.y*40,
                ra.x*40 + 40, 260-ra.y*40,
            )
            pos.set('pos: %0.2f' % s)
            speed.set('speed: %0.2f' % v)
            accel.set('accel: %0.2f' % a)
            stop()
            after_ids.append(tk.after(20, update))

        stop()
        tk.after_idle(update)

    tkinter.Button(tk, text='start', command=start).pack()

    tk.mainloop()

if __name__ == '__main__':
    main()
