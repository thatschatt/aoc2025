import time
import numpy as np


def go(filename: str) -> int:
    # Looks like a straightforward numpy brute force is on the cards here.
    # Each battery bank is 100 entries long, and there's 200 of them, so
    # 100*100*200 = 2M ops worst case.

    def get_max_jolts(bank: np.typing.NDArray[np.int64]) -> tuple[int, int, int]:
        max_jolt = 0
        for n in range(99, 0, -1):
            n_1_ind = np.where(bank == n // 10)[0]
            if len(n_1_ind) == 0:
                continue
            n_1 = n_1_ind[0]
            n_2_ind = np.where(bank[n_1 + 1 :] == n % 10)[0]
            if len(n_2_ind) == 0:
                continue
            max_jolt = n
            n_2 = n_2_ind[0]
            return (max_jolt, n_1, n_2 + n_1)
        raise ValueError(f"Never found a max jolt for {bank}!")

    with open(filename, "r") as f:
        jolt_sum = 0
        for l in f.readlines():
            bank = np.array([int(n) for n in l.strip()])
            (jolts, n_1, n_2) = get_max_jolts(bank)
            jolt_sum += jolts
            print(
                f"In {bank}, you can make the largest joltage possible, {jolts}, by turning on batteries [{n_1}] and [{n_2}]."
            )
    print(f"***Total output is for {filename} is {jolt_sum}")
    return jolt_sum


# Part 2 is going to take some thinking - brute force is completely out the cards here.
# Feels a lot like it's going to be a recursive depth first search function. Let's try that.
def go_2(filename: str):
    def array2num(array: list | np.typing.NDArray) -> int:
        num = 0
        for ex, n in enumerate(array[::-1]):
            num += int(10**ex) * n
        return num

    def get_max_jolts(
        bank: list[int],
        battery: list[int] = [],
        ind: int = 0,
        best_battery: list[int] = [0] * 12,
    ) -> list[int]:
        # need to do do a wee search in here
        # We need to pass:
        #   the overall bank
        #   the battery we've assembled so far
        #   the index of the last battery
        #   the largest jolts we've seen so far

        # OK so this works, but it's miserably slow. Need to come up with a way to sample
        # much less of the tree

        # when we hit the bottom, return this bank
        level = len(battery)
        if level == 12:  # zero indexed!
            return battery
        if level == 4:
            print(".", end="", flush=True)

        # at each level, we only continue if the number we are looking at right now beats the
        # best that we've ever seen

        # do this with explicit indicies, because I feel we'll need it...
        for i in range(ind, len(bank) - (11 - level)):
            trial = battery + [bank[i]]
            if array2num(trial) > array2num(best_battery[: level + 1]):
                best_battery = get_max_jolts(bank, trial, i + 1, best_battery)
        return best_battery

    # Hold on. In all cases, biggest number in the first 88 numbers is the best 1st digit.
    # SO a much smarter move is to find the biggest number in this range, and set it as the 1st digit, and then
    # take the first instance of it as out index for it
    def get_max_jolts_not_dumb(bank: np.typing.NDArray[np.int64]):
        battery = np.zeros(12, dtype=np.int64)
        last_d = -1
        for digit in range(12):
            i = np.argmax(bank[last_d + 1 : len(bank) - 11 + digit]) + last_d + 1
            battery[digit] = bank[i]
            last_d = i
        return battery

    with open(filename, "r") as f:
        jolt_sum = 0
        for l in f.readlines():
            bank = np.array([int(n) for n in l.strip()])
            battery = get_max_jolts_not_dumb(bank)
            jolt_sum += array2num(battery)
            print(
                f"In {bank}, you can make the largest joltage possible, {array2num(battery)}"
            )
    print(f"***Total output is for {filename} is {jolt_sum}")
    return jolt_sum


if go("day03/test03.txt") == 357:
    t0 = time.perf_counter()
    go("day03/input03.txt")
    print(f"took {time.perf_counter() - t0} s")

print("\n*******\n")
if go_2("day03/test03.txt") == 3121910778619:
    t0 = time.perf_counter()
    go_2("day03/input03.txt")
    print(f"took {time.perf_counter() - t0} s")
