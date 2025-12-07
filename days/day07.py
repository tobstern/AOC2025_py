import time
import os
from collections import defaultdict as dd


def movable(diag, pos):
    retval = diag.get(pos, "")
    if retval == "" or retval == "^":
        return False
    else:
        return True


def part1(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 1:")

    splitters = []
    start = (0, 0)
    diagram = dict()
    # read in the diagram
    for i, line in enumerate(input_str.strip().splitlines()):
        # print(list(line))
        for j, elem in enumerate(line):
            diagram[(i, j)] = elem

            if elem == "S":
                start = (i, j)
            elif elem == "^":
                splitters.append((i, j))
    tachyons = {start}

    # move the beam(s)
    splitcount = 0
    last_tachyons = set()
    used_beamsplitters = set()
    while True:
        if all(beam in last_tachyons for beam in tachyons):
            # there is no change anymore -> so stop
            break
        # now move all tachyons to next downward (where possible)
        last_tachyons = tachyons.copy()  # okay, but not altered in place
        # print(f"current tachyons: {tachyons}")

        for i, j in last_tachyons:
            nextpos = (i + 1, j)

            if diagram.get(nextpos, "") == "^":
                # splitcount += 1
                used_beamsplitters.add(nextpos)

                # split at nextpos to left and right and save them to tachyons
                if movable(diagram, (i + 1, j + 1)):
                    tachyons.add((i + 1, j + 1))
                if movable(diagram, (i + 1, j - 1)):
                    tachyons.add((i + 1, j - 1))

            elif diagram.get(nextpos, "") == ".":
                # just move downward if not oob:
                if movable(diagram, nextpos):
                    tachyons.add(nextpos)

    result = len(used_beamsplitters)
    # result = splitcount
    print(f"Part 1 result is: {result}")

    end_time = time.time()
    print(f"Part 1 execution time: {end_time - start_time} seconds")


def part2(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 2:")

    splitters = []
    start = (0, 0)
    diagram = dict()
    # read in the diagram
    maxrows = 0
    for i, line in enumerate(input_str.strip().splitlines()):
        # print(list(line))
        for j, elem in enumerate(line):
            diagram[(i, j)] = elem

            if elem == "S":
                start = (i, j)
            elif elem == "^":
                splitters.append((i, j))
    else:
        maxrows = i

    # move the beam(s)
    timeline_counts = dd(int)
    timeline_counts[start] = 1

    # now move all tachyons to next downward (where possible)

    for rc in range(0, maxrows + 1):
        print(f"timeline counts: {sum(timeline_counts.values())}")
        next_timeline_counts = dd(int)

        for (i, j), count in timeline_counts.items():
            if i != rc:
                continue

            nextpos = (i + 1, j)
            elem = diagram.get(nextpos, "")

            # If we're at the last row, keep these beams
            if i == maxrows:
                next_timeline_counts[(i, j)] += count
                continue

            if elem == "^":
                # Each beam splits into 2 beams
                left = (i + 1, j - 1)
                right = (i + 1, j + 1)

                # split at nextpos to left and right - each gets the full count
                if movable(diagram, left):
                    next_timeline_counts[left] += count
                if movable(diagram, right):
                    next_timeline_counts[right] += count

            elif elem == ".":
                # just move downward if not oob:
                if movable(diagram, nextpos):
                    next_timeline_counts[nextpos] += count

        timeline_counts = next_timeline_counts

    result = sum(timeline_counts.values())
    print(f"Part 2 result is: {result}")

    end_time = time.time()
    print(f"Part 2 execution time: {end_time - start_time} seconds")


# Brute-Force approach -> exponential growth -> memory/processing issue (32_451_134_474_991 -> ~32e12 timelines!!!)
# def part2(input_str):
#     start_time = time.time()
#     filename = os.path.basename(__file__)
#     day_num = filename.replace("day", "").replace(".py", "").strip()
#     print(f"Day {day_num}, Part 2:")
#
#     splitters = []
#     start = (0, 0)
#     diagram = dict()
#     # read in the diagram
#     maxrows = 0
#     for i, line in enumerate(input_str.strip().splitlines()):
#         # print(list(line))
#         for j, elem in enumerate(line):
#             diagram[(i, j)] = elem
#
#             if elem == "S":
#                 start = (i, j)
#             elif elem == "^":
#                 splitters.append((i, j))
#     else:
#         maxrows = i
#
#     tachyons = {start}
#
#     # move the beam(s)
#     timelines = 0
#
#     last_tachyons = set()
#     used_beamsplitters = set()
#     all_poss_beams = [[start]]
#     last_all_poss_beams = []
#     while True:
#         if all(beam_path[-1][0] == maxrows or beam_path[-1][1] == maxrows for beam_path in all_poss_beams):
#             break
#         # now move all tachyons to next downward (where possible)
#         last_all_poss_beams = all_poss_beams.copy()  # okay, but not altered in place
#         # print(f"current tachyons: {tachyons}")
#
#         for bidx, beam in enumerate(last_all_poss_beams):
#             lastpos = beam[-1]
#             nextpos = (lastpos[0] + 1, lastpos[1])
#
#             if diagram.get(nextpos, "") == "^":
#
#                 # split at nextpos to left and right and save them to tachyons
#                 right = (nextpos[0], nextpos[1] + 1)
#                 left = (nextpos[0], nextpos[1] - 1)
#                 if movable(diagram, right):
#                     all_poss_beams.append(beam + [right])
#
#                 if movable(diagram, left):
#                     all_poss_beams[bidx].append(left)
#
#             elif diagram.get(nextpos, "") == ".":
#                 # just move downward if not oob:
#                 if movable(diagram, nextpos):
#                     all_poss_beams[bidx].append(nextpos)
#
#     result = len(all_poss_beams)
#     print(f"Part 2 result is: {result}")
#
#     end_time = time.time()
#     print(f"Part 2 execution time: {end_time - start_time} seconds")
