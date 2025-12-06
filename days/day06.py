import time
import os


def part1(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 1:")

    nums_list = []
    for i, line in enumerate(input_str.strip().splitlines()):
        row_nums = [int(s) if s.isnumeric() else s for s in line.split()]
        # print(row_nums)
        nums_list.append(row_nums)

    # print(nums_list)
    tpose_nums = list(map(list, zip(*nums_list)))
    # print(tpose_nums)

    # operate on lists
    sumres = 0

    for curr_nums_list in tpose_nums:
        curr_op = curr_nums_list[-1]

        if curr_op == "*":
            op_res = 1
            for num in curr_nums_list[:-1]:
                op_res *= num
            sumres += op_res
        if curr_op == "+":
            op_res = 0
            for num in curr_nums_list[:-1]:
                op_res += num
            sumres += op_res

    result = sumres
    print(f"Part 1 result is: {result}")

    end_time = time.time()
    print(f"Part 1 execution time: {end_time - start_time} seconds")


def part2(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 2:")

    str_lines = [list(s) for s in input_str.splitlines()]
    # row_nums = [list(s) for s in line.split()]
    # print(row_nums)
    # nums_list.append(row_nums)

    # print(str_lines)
    # exit(0)

    str_elems_tpose = list(map(list, zip(*str_lines)))
    # print(str_elems_tpose)

    full_tpose_str = ""
    for line in str_elems_tpose:
        if all(ele == " " for ele in line):
            full_tpose_str += "\n"
            continue

        for elem in line:
            full_tpose_str += elem
        full_tpose_str += "\n"
    # print(full_tpose_str)

    # print(full_tpose_str.split("\n\n"))
    # exit()

    sumres = 0
    for block in full_tpose_str.split("\n\n"):
        # print("block:", block)
        li = block.split()
        # print("curr list:", li)
        if "*" in li[0] or "+" in li[0]:
            # separate the number from the op
            curr_op = li[0][-1]
            op_res = int(li[0][:-1])
            start = 1
        else:
            curr_op = li[1]
            op_res = int(li[0])
            start = 2

        for num in li[start:]:
            if curr_op == "*":
                op_res *= int(num)
            if curr_op == "+":
                op_res += int(num)
        sumres += op_res

    result = sumres
    print(f"Part 2 result is: {result}")

    end_time = time.time()
    print(f"Part 2 execution time: {end_time - start_time} seconds")
