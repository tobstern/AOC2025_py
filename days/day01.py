import time
import os


def part1(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 1:")
    # Implement the logic here
    password = 0
    count = 50
    for line in input_str.splitlines():
        # print(line)
        if line[0] == "R":
            count += int(line[1:].strip())
        elif line[0] == "L":
            count -= int(line[1:].strip())
        else:
            ValueError("Not defined: must be either L or R!")

        count %= 100

        if count == 0:
            password += 1

    result = password
    print(f"Part 1 result is: {result}")

    end_time = time.time()
    print(f"Part 1 execution time: {end_time - start_time} seconds")


def part2(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 2:")
    password = 0
    count = 50
    for line in input_str.splitlines():
        oldcount = count

        stepnum = int(line[1:].strip())
        password += stepnum // 100
        stepnum %= 100

        # check the zero crossing under step_hundreds movement:
        if line[0] == "L":
            count -= stepnum
        else:
            # R:
            count += stepnum

        if count * oldcount < 0 or count > 99 or count % 100 == 0:
            password += 1

        count %= 100

    result = password
    print(f"Part 2 result is: {result}")

    end_time = time.time()
    print(f"Part 2 execution time: {end_time - start_time} seconds")
