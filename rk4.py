def rk4(f, t0, y0, h):
    ''' approximate y(t0+h)
        where y'(t) = f(t, y(t)) and y(t0) = y0
    '''
    k1 = f(t0, y0)
    k2 = f(t0 + 0.5*h, y0 + 0.5*h*k1)
    k3 = f(t0 + 0.5*h, y0 + 0.5*h*k2)
    k4 = f(t0 + h, y0 + h*k3)
    return y0 + h * (0.5*k1 + k2 + k3 + 0.5*k4) * (1.0 / 3.0)
