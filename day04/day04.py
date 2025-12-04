import time
import numpy as np
from scipy.signal import convolve2d

def get_map(filename: str) -> np.ndarray:
    with open(filename, "r") as f:
        paper_map = np.array(bytearray(f.readline().strip().encode()))
        for l in f.readlines():
            paper_map = np.vstack((paper_map, np.array(bytearray(l.strip().encode()))))
        paper_map[paper_map == 46] = 0
        paper_map[paper_map == 64] = 1
    return paper_map

def get_accessible_sites(paper_map: np.ndarray) -> np.ndarray:
    kernel = np.array([[1, 1, 1], [1, 10, 1], [1, 1, 1]])
    conv = convolve2d(paper_map, kernel, mode='same')
    accessible = ((conv >= 10) & (conv <= 13))
    return accessible

def go(filename: str) -> int:
    # This feels a convolution to me. Should be simple.
    # first need to convert the string into a numpy matrix
    paper_map = get_map(filename)
    ok_sum = np.sum(get_accessible_sites(paper_map))
    print(f"there are {ok_sum} rolls of paper that can be accessed by a forklift in {filename}")
    return ok_sum

# so part 2 wants us to find the optimal order to remove rolls in
# for the first step there are 1625 rolls accessible, which means
# this tree could be a little gnarly.
# Sounds like recursion then.

def go_2(filename: str) -> int:
    # my naive method will do a shitload of allocating, and run a jillion convolutions
    # Let's hope that's OK!

    # so apparently python has a maximum recusion depth of 1000 by default.
    # Let's just set it to be big
    import sys
    sys.setrecursionlimit(10_000)

    def remove_roll(paper_map: np.ndarray, level: int=0) -> int:
        # for a given map, find all the available rolls, and queue them up for recursive investigation
        # if we are at the limit, return the number of removals and pass it back up

        # wait no - we only need to do the first available, since order doesn't matter!

        # if the conv is too slow, we may have to write a function that quickly locatse first
        # accessible spot.
        accessible_inds = np.where(get_accessible_sites(paper_map))
        max_remove = 0
        print(f"level = {level}, accessibles = {len(accessible_inds[0])}")
        if len(accessible_inds[0]) == 0:
            return level
        map_copy = np.copy(paper_map) # ouch.
        map_copy[accessible_inds[0][0], accessible_inds[1][0]] = 0
        m = remove_roll(map_copy, level+1)
        if m > max_remove:
            max_remove = m
        return max_remove
    
    paper_map = get_map(filename)
    max_remove = remove_roll(paper_map)
    print(f"there are {max_remove} rolls of paper that can be removed in {filename}")
    return max_remove


if go("day04/test04.txt") == 13:
    t0 = time.perf_counter()
    go("day04/input04.txt")
    print(f"took {time.perf_counter() - t0} s")

print("\n*******\n")
if go_2("day04/test04.txt") == 43:
    t0 = time.perf_counter()
    go_2("day04/input04.txt")
    print(f"took {time.perf_counter() - t0} s")
