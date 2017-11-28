#!/usr/bin/env python3

import math
import time

from renderers import marching_square
from renderers import utils


def dfield_balls(hres, vres, t):
    balls = [(23 + 15 * math.cos(t),
              10 + 10 * math.sin(t*0.75) ),
             (40 + 8 * math.cos(t + 15),
              5 + 6 * math.sin(t)),
              (60 + 15 * math.sin(t),
               18 + 5 * math.cos(t)),
              (16 + 30 * math.cos(t),
               10 + 8 * math.sin(t))]

    dfield = [[0.0 for _ in range(hres)] for _ in range(vres)]
    for y in range(vres):
        for x in range(hres):
            for b in balls:
                if b[0] == x and b[1] == y:
                    dfield[y][x] = 1.0
                else:
                    dfield[y][x] += 1.0 / ((x - b[0])**2 + (y - b[1])**2)

                if dfield[y][x] > 1.0:
                    dfield[y][x] = 1.0

    return dfield



if __name__ == "__main__":


    t0 = time.time()

    while 42:
        t = time.time() - t0
        utils.clear()
        df = dfield_balls(80, 30, t)
        if (t % 10) < 5:
            marching_square.render(df, marching_square.shade_box_lines)
        else:
            marching_square.render(df, marching_square.shade_box_dots)
        time.sleep(1.0 / 25.0)



