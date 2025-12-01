#import numpy as np

def go(filename: str):
    zeros = 0
    N = 50
    with open(filename, "r") as f:
        l = f.readline().strip()
        while l:
            if l[0] == 'L':
                N -= int(l[1:])
            elif l[0] == 'R':
                N += int(l[1:])
            else:
                raise ValueError(f"bad line: {l}")
            if (N%100 == 0):
                zeros += 1
            l = f.readline().strip()
    return zeros


def go_2(filename: str):
    zeros = 0
    N = 50
    with open(filename, "r") as f:
        # this gets an off-by-1 if you start or end on a zero I think?
        # only while going left.
        l = f.readline().strip()
        while l:
            inc = -int(l[1:]) if l[0] == 'L' else int(l[1:])
            N_init = N
            N += inc
            z = abs(N // 100)
            zeros += abs(N // 100)
            N = N % 100
            print(
                f"The dial is rotated {l} to point at {N}; during this rotation, it points at zero {z} times."
            )
            # handles some edge case
            # if we go L and started on zero, we overcount
            # if we go L and end on a zero we undercount
            if (inc < 0) and (N == 0):
                zeros += 1
            if (inc < 0) and (N_init == 0):
                zeros -= 1
            l = f.readline().strip()
    return zeros

if go("day01/test01.txt") == 3:
    print(f'part 1: {go("day01/input01.txt")}')

print(go_2("day01/test01.txt"))
if go_2("day01/test01.txt") == 6:
    print(f'part 2: {go_2("day01/input01.txt")}')  # 7159 too high; 6698 too low
