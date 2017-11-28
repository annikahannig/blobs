
import random
import time
import os

def get_screen_size():
    rows, columns = os.popen('stty size', 'r').read().split()

    return (int(columns), int(rows))


def maze_line(w):
    c = ["╲", "╱"]
    for j in range(w):
        print(c[random.randint(0,1)], end="")
    print()


def maze(w, h):
    c = ["╲", "╱"]
    for i in range(h):
        for j in range(w):
            print(c[random.randint(0,1)], end="")
        print()


def scroller(w):
    while 42:
       maze_line(w)
       time.sleep(1/5)


if __name__ == "__main__":
    w, h = get_screen_size()
    maze(w, h - 2)

