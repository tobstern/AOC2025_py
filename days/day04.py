import time
import os


def part1(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 1:")

    paper_rolls = dict()
    for r, row in enumerate(input_str.splitlines()):
        for c, ele in enumerate(row):
            paper_rolls[(r, c)] = ele

    # print(paper_rolls)
    reachable_rolls_posis = set()
    for r, row in enumerate(input_str.splitlines()):
        for c, ele in enumerate(row):
            rollcount = 0
            # print((r, c), ele)
            # check for every ele if rollcount<4
            for nr, nc in [
                (r + 1, c),
                (r - 1, c),
                (r, c + 1),
                (r, c - 1),
                (r + 1, c - 1),
                (r + 1, c + 1),
                (r - 1, c - 1),
                (r - 1, c + 1),
            ]:
                # skip if oob:
                if nr < 0 or nc < 0 or nr >= len(row) or nc >= len(row):
                    continue
                # else check if roll
                if paper_rolls[(nr, nc)] == "@":
                    rollcount += 1
            if rollcount < 4 and paper_rolls[(r, c)] == "@":
                # can be reached
                reachable_rolls_posis.add((r, c))

    # # Print grid with reachable positions marked by "x"
    # for r, row in enumerate(input_str.splitlines()):
    #     line = ""
    #     for c, ele in enumerate(row):
    #         if (r, c) in reachable_rolls_posis:
    #             line += "x"
    #         else:
    #             line += ele
    #     print(line)

    # print(reachable_rolls_posis)
    result = len(reachable_rolls_posis)
    print(f"Part 1 result is: {result}")

    end_time = time.time()
    print(f"Part 1 execution time: {end_time - start_time} seconds")


def part2(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 2:")

    maxrow = 0
    maxcol = 0
    paper_rolls = dict()
    for r, row in enumerate(input_str.splitlines()):
        for c, ele in enumerate(row):
            paper_rolls[(r, c)] = ele
        else:
            maxcol = c
    else:
        maxrow = r

    # print(paper_rolls)
    reachable_rolls_posis = set()
    for r, row in enumerate(input_str.splitlines()):
        for c, ele in enumerate(row):
            rollcount = 0
            # print((r, c), ele)
            # check for every ele if rollcount<4
            for nr, nc in [
                (r + 1, c),
                (r - 1, c),
                (r, c + 1),
                (r, c - 1),
                (r + 1, c - 1),
                (r + 1, c + 1),
                (r - 1, c - 1),
                (r - 1, c + 1),
            ]:
                # skip if oob:
                if nr < 0 or nc < 0 or nr >= len(row) or nc >= len(row):
                    continue
                # else check if roll
                if paper_rolls[(nr, nc)] == "@":
                    rollcount += 1
            if rollcount < 4 and paper_rolls[(r, c)] == "@":
                # can be reached
                reachable_rolls_posis.add((r, c))

    removed_rolls_count = len(reachable_rolls_posis)
    last_paper_rolls = dict()
    while True:
        if paper_rolls == last_paper_rolls:
            # nothing movable anymore
            break

        last_paper_rolls = paper_rolls.copy()
        for r, c in reachable_rolls_posis:
            # print((r, c), ele)
            # delete reachable and check again for reachable
            del paper_rolls[(r, c)]

        next_map_list = [["."] * (maxcol + 1)] * (maxrow + 1)
        # print(next_map_list, maxcol, maxrow)

        for (r, c), ele in paper_rolls.items():
            next_map_list[r][c] = ele

        # print(next_map_list)

        # while loop until nothing movable anymore: nothing reachable
        # print(len(next_paper_rolls), len(paper_rolls))

        reachable_rolls_posis = set()
        for r, row in enumerate(next_map_list):
            for c, ele in enumerate(row):
                rollcount = 0
                # print((r, c), ele)
                # check for every ele if rollcount<4
                for nr, nc in [
                    (r + 1, c),
                    (r - 1, c),
                    (r, c + 1),
                    (r, c - 1),
                    (r + 1, c - 1),
                    (r + 1, c + 1),
                    (r - 1, c - 1),
                    (r - 1, c + 1),
                ]:
                    # skip if oob:
                    if nr < 0 or nc < 0 or nr >= len(row) or nc >= len(row):
                        continue
                    # else check if roll
                    if paper_rolls.get((nr, nc), ".") == "@":
                        rollcount += 1
                if rollcount < 4 and paper_rolls.get((r, c), "") == "@":
                    # can be reached
                    reachable_rolls_posis.add((r, c))

        removed_rolls_count += len(reachable_rolls_posis)

    result = removed_rolls_count
    print(f"Part 2 result is: {result}")

    end_time = time.time()
    print(f"Part 2 execution time: {end_time - start_time} seconds")
