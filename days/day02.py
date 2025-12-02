import time
import os


def part1(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 1:")

    result = 0

    for interval in input_str.strip().split(","):
        # print(interval)
        left, right = interval.strip().split("-")
        left = int(left)
        right = int(right)
        # print(left, right)
        for num in range(left, right + 1):
            # check all numbers if their halfs are repeated
            numstr = str(num)
            L = len(numstr)
            leftstr = numstr[: L // 2]
            rightstr = numstr[L // 2 :]
            if leftstr == rightstr:
                # add to res
                # print(f"{numstr} is split into {leftstr}=={rightstr}")
                result += num

    print(f"Part 1 result is: {result}")

    end_time = time.time()
    print(f"Part 1 execution time: {end_time - start_time} seconds")


def part2(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 2:")

    result = 0

    for interval in input_str.strip().split(","):
        # print(interval)
        left, right = interval.strip().split("-")
        left = int(left)
        right = int(right)
        # print(left, right)
        for num in range(left, right + 1):
            numstr = str(num)
            L = len(numstr)
            divis = 0
            invalid = False
            all_subs = []

            while divis <= L:
                divis += 1
                if L % divis != 0:
                    all_subs = []
                    invalid = False
                    continue
                # check all numbers if their halfs,thirds,fourths... are repeated
                # if matchcounter == sublen - 1:

                all_subs = [numstr[j : j + divis] for j in range(0, L, divis)]

                if all([s == all_subs[0] for s in all_subs]) and len(all_subs) > 1:
                    print(all_subs)
                    invalid = True

                    # print(f"Invalid numstr: {numstr}")
                    result += num
                    break

                # print(f"strL:{L}, divisor:{divis}, sublen:{sublen}, matchcounter:{matchcounter}")

    print(f"Part 2 result is: {result}")

    end_time = time.time()
    print(f"Part 2 execution time: {end_time - start_time} seconds")


# 22461391032 not right - too low
# 22471660255
