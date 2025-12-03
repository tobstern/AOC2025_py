import time
import os
import itertools


def part1(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 1:")

    battres = 0
    for line in input_str.strip().splitlines():
        jolts = [int(s) for s in line]

        m1 = max(jolts)
        idx1 = jolts.index(m1)

        # loop every numcomb and save the largest:
        largest = 0
        for i, num in enumerate(jolts):
            if i == idx1:
                continue
            elif i < idx1:
                m2str = str(num)
                m1str = str(m1)
                combinedstr = m2str + m1str
            elif i > idx1:
                m2str = str(num)
                m1str = str(m1)
                combinedstr = m1str + m2str

            nc = int(combinedstr)
            if nc > largest:
                largest = nc

        # print(largest)

        battres += largest

    result = battres
    print(f"Part 1 result is: {result}")

    end_time = time.time()
    # too high: 17589
    print(f"Part 1 execution time: {end_time - start_time} seconds")


def part2(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 2:")

    battres = 0
    for line in input_str.strip().splitlines():
        jolts = [int(s) for s in line]
        n = len(jolts)
        to_remove = n - 12

        # Greedily remove digits to maximize the remaining number
        digits = jolts.copy()
        removed = 0

        while removed < to_remove:
            # Find the first digit where removing it increases the value
            # (i.e., the next digit is larger, or we need to remove from the end)
            idx_to_remove = -1

            for i in range(len(digits) - 1):
                if digits[i] < digits[i + 1]:
                    idx_to_remove = i
                    break

            # If no such position found, remove from the end
            if idx_to_remove == -1:
                idx_to_remove = len(digits) - 1

            digits.pop(idx_to_remove)
            removed += 1

        result_num = int("".join(map(str, digits)))
        print(result_num)
        battres += result_num

    result = battres
    print(f"Part 2 result is: {result}")

    end_time = time.time()
    print(f"Part 2 execution time: {end_time - start_time} seconds")


# too high: 172428152372374
#           171741365473332

# battres = 0
# for line in input_str.strip().splitlines():
#     jolts = [int(s) for s in line]

#     m1 = max(jolts)
#     idx1 = jolts.index(m1)

#     combs12of15 = list(itertools.combinations(jolts, 12))
#     # print(combs12of15)
#     # loop every numcomb and save the largest:
#     largest = 0
#     for tup in combs12of15:
#         # print("".join([str(ele) for ele in tup]))
#         num = int("".join([str(ele) for ele in tup]))
#         if num > largest:
#             largest = num

#     # for i, num in enumerate(jolts):

#     # print(largest)

#     battres += largest

# result = battres
