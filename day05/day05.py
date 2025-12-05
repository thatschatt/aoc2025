import time
import numpy as np


def go(filename: str) -> int:
    # so we just have to load in some ranges and check if numbers belong
    # Looks like we'll need 64bit ints, but that's about it
    ranges: list[tuple[int, int]] = []
    ingredients: list[int] = []
    with open(filename, "r") as f:
        l = f.readline().strip()
        while l != "":
            (n1, n2) = (int(n) for n in l.split("-"))
            ranges.append((n1, n2))
            l = f.readline().strip()
        l = f.readline().strip()
        while l != "":
            ingredients.append(int(l))
            l = f.readline().strip()

        fresh = 0
        for i in ingredients:
            for r in ranges:
                if (i >= r[0]) and (i <= r[1]):
                    fresh += 1
                    break
    print(f"{fresh} of the available ingredient IDs are fresh in {filename}")
    return fresh


if go("day05/test05.txt") == 3:
    t0 = time.perf_counter()
    go("day05/input05.txt")
    print(f"took {time.perf_counter() - t0} s")

# print("\n*******\n")
# if go_2("day04/test04.txt") == 43:
#     t0 = time.perf_counter()
#     go_2("day04/input04.txt")
#     print(f"took {time.perf_counter() - t0} s")
