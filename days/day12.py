import time
import os


def part1(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 1:")

    shapes = []
    avail_space = []
    shape_counts = []
    S = {}
    for i, block in enumerate(input_str.strip().split("\n\n")):
        temp_list = []
        count = 0
        for line in block.splitlines():
            if i <= 5:
                if ":" in line:
                    S[int(line.split(":")[0])] = 0
                else:
                    count += sum([1 if ele == "#" else 0 for ele in line])
                    temp_list.append(list(line))
            else:
                # print(line)
                avail_space.append(tuple(map(int, line.split(": ")[0].split("x"))))
                shape_counts.append(tuple(map(int, line.split(": ")[1].strip().split())))
        shapes.append(temp_list)
        if i <= 5:
            S[i] += count
    print(shapes)
    print(avail_space)
    print(shape_counts)
    print(S)

    # now find out which space can fit all the specified shapes with its shape counts:
    # tot_psize = []
    result = 0
    for idx, space in enumerate(avail_space):
        tot_empty = space[0] * space[1]
        tot_present = sum([S[i] * shape_counts[idx][i] for i in range(6)])

        # print(f"tot_empty={tot_empty}; tot_present={tot_present}")

        if tot_present // 3 < tot_empty // 3:
            # if there is "plenty of space", problably fitting inside space
            result += 1
        # elif tot_present > tot_empty:
        #     continue
        # else:
        #     print(f"This can be hard to place - probably not fitting...")
        #     print(f"tot_empty={tot_empty}; tot_present={tot_present}")

    print(f"Part 1 result is: {result}")

    end_time = time.time()
    print(f"Part 1 execution time: {end_time - start_time} seconds")


def part2(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 2:")

    result = 0
    print(f"Part 2 result is: {result}")

    end_time = time.time()
    print(f"Part 2 execution time: {end_time - start_time} seconds")
