import time
import numpy as np


def get_ranges(filename: str) -> set[tuple[int, int]]:
    ranges = set()
    with open(filename, "r") as f:
        l = f.readline().strip()
        while l != "":
            (n1, n2) = (int(n) for n in l.split("-"))
            ranges.add((n1, n2))
            l = f.readline().strip()
    return ranges


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


def go_2(filename: str) -> int:
    # so for part two there is no possible way to brute force it. Instead we have to consider the
    # total overlap between ranges using our wits. Hmm.
    # The trick will be to create new set of ranges by doing OR operations between every range.
    # That'll do it
    #
    # We loop through all the existing ranges, and if they touch we delete the old range and expand
    # the incoming one to incroporate it

    # keep repeating this until it stops changing?
    # - no need if we use sets

    def merge_ranges(old_ranges: set[tuple[int, int]]) -> set[tuple[int, int]]:
        new_ranges: set[tuple[int, int]] = (
            set()
        )  # can't mutate the old list while iterating
        for r in old_ranges:
            merged_range_lo = r[0]
            merged_range_hi = r[1]
            kill_list = set()
            for nr in new_ranges:
                if (
                    ((merged_range_lo >= nr[0]) and (merged_range_lo <= nr[1]))
                    or ((merged_range_hi >= nr[0]) and (merged_range_hi <= nr[1]))
                    or ((merged_range_lo >= nr[0]) and (merged_range_hi <= nr[1]))
                    or ((merged_range_lo <= nr[0]) and (merged_range_hi >= nr[1]))
                ):  # ranges overlap
                    merged_range_lo = min(merged_range_lo, nr[0])
                    merged_range_hi = max(merged_range_hi, nr[1])
                    kill_list.add(nr)
            new_ranges -= kill_list
            new_ranges.add((merged_range_lo, merged_range_hi))
        return new_ranges

    new_ranges = set()
    old_ranges = set(get_ranges(filename))
    mr = merge_ranges(old_ranges)
    print(f"ranges = {mr}")

    range_sum = 0
    for n in mr:
        range_sum += n[1] - n[0] + 1
    print(f"fresh sum = {range_sum}")
    return range_sum


if go("day05/test05.txt") == 3:
    t0 = time.perf_counter()
    go("day05/input05.txt")
    print(f"took {time.perf_counter() - t0} s")

print("\n*******\n")
if go_2("day05/test05.txt") == 14:
    t0 = time.perf_counter()
    go_2("day05/input05.txt")
    print(f"took {time.perf_counter() - t0} s")

# 289362882275704 too low
# 355766168826824 too high
# I forgot about ranges that encompass each other