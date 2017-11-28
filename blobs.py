#!/usr/bin/env python3

from renderers import marching_square



def dfield_balls(hres, vres):
    balls = [(23, 10), (10, 5), (60, 18), (16, 10)]

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

    df = dfield_balls(75, 40)

    marching_square.render(df, marching_square.shade_box_dots)



