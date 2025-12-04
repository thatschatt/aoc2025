import time
import numpy as np
from scipy.signal import convolve2d

def get_map(filename: str) -> np.ndarray[tuple[int, int], np.dtype[np.int64]]:
    with open(filename, "r") as f:
        paper_map = np.array(bytearray(f.readline().strip().encode()))
        for l in f.readlines():
            paper_map = np.vstack((paper_map, np.array(bytearray(l.strip().encode()))))
        paper_map[paper_map == 46] = 0
        paper_map[paper_map == 64] = 1
    return paper_map

def go(filename: str) -> int:
    # This feels a convolution to me. Should be simple.
    # first need to convert the string into a numpy matrix
    paper_map = get_map(filename)
    kernel = np.array([[1, 1, 1], [1, 10, 1], [1, 1, 1]])
    conv = convolve2d(paper_map, kernel, mode='same')
    ok_sum = np.sum((conv >= 10) & (conv <= 13))
    print(f"there are {ok_sum} rolls of paper that can be accessed by a forklift")
    return ok_sum

# so part 2 wants us to find the optimal order to remove rolls in
# for the first step there are 1625 rolls accessible, which means
# this tree could be a little gnarly.
# Depth or breadth first?
#    I guess it doesn't matter since we need to be exhaustive
#    I'll want to memoize this though, since we'll hit the same branch
#    very often.
# Sounds like recursion then. 

if go("day04/test04.txt") == 13:
    t0 = time.perf_counter()
    go("day04/input04.txt")
    print(f"took {time.perf_counter() - t0} s")

# print("\n*******\n")
# if go_2("day03/test03.txt") == 3121910778619:
#     t0 = time.perf_counter()
#     go_2("day03/input03.txt")
#     print(f"took {time.perf_counter() - t0} s")
