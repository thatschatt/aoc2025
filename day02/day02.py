import time


def go(filename: str):
    # OK, so we can for sure brute force section 1 here, since all the ranges seem to
    # be < 1 million
    # I'll save the celver trick for whtever it is that part 2 requires
    with open(filename, "r") as f:
        ranges = f.readline().strip().split(",")
        invalids = 0
        inv_sum = 0
        for r in ranges:
            invalid_r = 0
            (lower, upper) = (int(i) for i in r.split("-"))
            for n in range(lower, upper + 1):
                n_str = f"{n}"
                if len(n_str) % 2 != 0:
                    continue
                if n_str[0 : len(n_str) // 2] == n_str[len(n_str) // 2 :]:
                    invalid_r += 1
                    inv_sum += n
            print(f"{lower}-{upper} has {invalid_r} invalid IDs.")
            invalids += invalid_r
    print(f"Adding up all the invalid IDs in this example produces {inv_sum}.")
    return inv_sum


# so for part 2, the easy option seems to be just include a nested loop.
# Part 1 ran in 0.3 s, so in the worst case we go maybe 5x longer, which is still fine.


def check_str(n_str: str, digits: int):
    """For a given number (in string form), check if it repeats with groups
    of `digits`."""
    if len(n_str) % digits != 0:
        return False  # easy return if it can't fit
    first_group = n_str[:digits]
    for n in range(1, len(n_str) // digits):
        if n_str[n * digits : (n + 1) * digits] != first_group:
            return False
    return True


def go2(filename: str):
    with open(filename, "r") as f:
        ranges = f.readline().strip().split(",")
        invalids = 0
        inv_sum = 0
        for r in ranges:
            invalid_r = 0
            (lower, upper) = (int(i) for i in r.split("-"))
            for n in range(lower, upper + 1):
                n_str = f"{n}"
                for d in range(1, len(n_str) // 2 + 1):
                    if check_str(n_str, d):
                        invalid_r += 1
                        inv_sum += n
                        break  # prevent double counting
            print(f"{lower}-{upper} has {invalid_r} invalid IDs.")
            invalids += invalid_r
    print(f"Adding up all the invalid IDs in this example produces {inv_sum}.")
    return inv_sum


if go("day02/test02.txt") == 1227775554:
    t0 = time.perf_counter()
    go("day02/input02.txt")
    print(f"took {time.perf_counter() - t0} s")

print("\n*******\n")

if go2("day02/test02.txt") == 4174379265:
    print("\n*******\n")
    t0 = time.perf_counter()
    go2("day02/input02.txt")
    print(f"took {time.perf_counter() - t0} s")
