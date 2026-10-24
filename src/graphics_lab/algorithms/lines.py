import math

def slope_intercept(last_x: int, last_y: int, nx: int, ny: int) -> list[tuple[int, int]]:
    pixels=[]
    changed = False
    if last_x == nx:
        y = min(ny, last_y)
        for i in range(abs(last_y-ny)+1):
            pixels.append((nx,y+i))
        return pixels

    dx = nx - last_x
    dy = ny-last_y
    m = dy/dx

    if  abs(m)>1:
            last_x, last_y, nx, ny = last_y, last_x, ny, nx
            m = 1/m
            changed = True

    if (nx < last_x):
                    nx, last_x = last_x, nx
                    ny, last_y = last_y, ny

    x = last_x
    y = last_y
    b= last_y-m * last_x
    while (x <= nx):
            if changed: pixels.append((y,x))
            else: pixels.append((x,y))
            x = x+1
            y=round(m*x+b)
    return pixels


def dda(last_x: int, last_y: int, nx: int, ny: int) -> list[tuple[int, int]]:
    pixels=[]
    dx = nx - last_x
    dy = ny - last_y
    m= max(abs(dx),abs(dy))
    if m == 0:
        return [(last_x, last_y)]
    dxp= dx/ m
    dyp= dy/m
    x=last_x+0.5
    y=last_y+0.5
    i=0
    while i<=m:
        pixels.append((math.floor(x), math.floor(y)))
        x=x+dxp
        y=y+dyp
        i=i+1
    return pixels


def bresenham_float(x0: int, y0: int, x1: int, y1: int) -> list[tuple[int, int]]:
    pixels = []

    changed = False

    x = x0
    y = y0
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    s1 = sgn(x1 - x0)
    s2 = sgn(y1 - y0)

    if dy > dx:
        dx, dy = dy, dx
        changed = True

    if dx == 0:
        return [(x0, y0)]

    m = dy/dx
    e = m - 1/2
    i = 0
    while i <= dx:
        pixels.append((x, y))
        while e > 0:
            if not changed:
                y = y + s2
            else:
                x= x + s1
            e = e - 1

        if not changed:
             x = x + s1
        else:
            y = y+s2

        e = e + m
        i = i + 1

    return pixels


def bresenham_int(x0: int, y0: int, x1: int, y1: int) -> list[tuple[int, int]]:
    pixels = []

    changed = False

    x = x0
    y = y0
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    s1 = sgn(x1 - x0)
    s2 = sgn(y1 - y0)

    if dy > dx:
        dx, dy = dy, dx
        changed = True

    ne = 2*dy - dx
    i = 0
    while i <= dx:
        pixels.append((x, y))
        while ne > 0:
            if changed: x = x + s1
            else: y = y + s2
            ne = ne - 2*dx

        if changed: y = y + s2
        else: x = x + s1
        ne = ne + 2*dy
        i = i + 1

    return pixels


def sgn(n: int) -> int:
    if n < 0: return -1
    if n > 0: return 1
    return 0
