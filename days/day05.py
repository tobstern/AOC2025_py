import time
import os


def part1(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 1:")

    id_ranges_str, idlist_str = input_str.strip().split("\n\n")

    id_ranges = [
        (int(line.strip().split("-")[0]), int(line.strip().split("-")[1]))
        for line in id_ranges_str.strip().splitlines()
    ]
    # print(id_ranges)
    # print(idlist)

    # check if in bounds:
    freshcount = 0
    for idstr in idlist_str.strip().splitlines():
        # print(idstr)
        idnum = int(idstr)
        inanyrange = False

        for lb, rb in id_ranges:
            if idnum >= lb and idnum <= rb:
                # id is in this range
                inanyrange = True
                break
        if inanyrange:
            freshcount += 1

    result = freshcount
    print(f"Part 1 result is: {result}")

    end_time = time.time()
    print(f"Part 1 execution time: {end_time - start_time} seconds")


# def merge_ranges(i, currb, nextb, allranges):
#     (clb, crb) = currb
#     (nlb, nrb) = nextb
#
#     # print(f"currb={currb}, nextb={nextb}")
#     if crb < nlb:
#         # next range is separate, give nlb,nrb as next curr range
#         return i, (nlb, nrb), allranges
#     if i + 2 >= len(allranges):
#         print(f"currb={currb}, nextb={nextb}")
#
#         if crb >= nlb:
#             # do this now only for the last range again and save to merged:
#             clb, crb = clb, nrb
#         return i, (clb, crb), allranges
#     if crb >= nlb:
#         # merge:
#         return merge_ranges(i + 2, (clb, nrb), allranges[i + 2], allranges)


def merge_ranges(i, currb, allranges, merged):
    if i + 1 >= len(allranges):
        return i + 1, allranges, merged + [currb]

    (clb, crb) = currb
    (nlb, nrb) = allranges[i + 1]
    i += 1
    if crb < nlb:
        # next range is separate, give nlb,nrb as next curr range
        merged.append((clb, crb))
        return i, allranges, merged
    if crb >= nlb and crb <= nrb:
        # range needs to be continued/merged -> until else
        return merge_ranges(i, (clb, nrb), allranges, merged)
    elif crb >= nlb and crb > nrb:
        # next right bound is smaller than current one -> skip
        return merge_ranges(i, (clb, crb), allranges, merged)


def part2(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 2:")

    id_ranges_str, idlist_str = input_str.strip().split("\n\n")

    id_ranges = [
        (int(line.strip().split("-")[0]), int(line.strip().split("-")[1]))
        for line in id_ranges_str.strip().splitlines()
    ]

    # sort them and then check for separated or overlapping
    id_ranges_sorted = sorted(id_ranges)
    merged_id_ranges = []
    # print(id_ranges_sorted)

    # for i,(clb,crb) in enumerate(id_ranges_sorted):
    #     nlb,nrb = id_ranges_sorted[i+1]
    #     if crb >= nlb:
    #         # call recursively to merge until crb < nlb
    #         merged_id_ranges += merge_ranges(id_ranges_sorted)

    i = 0
    while i < len(id_ranges_sorted):
        currb = id_ranges_sorted[i]
        # def merge_ranges(i, currb, allranges, merged):
        # print(f"i={i}: currb={currb}")
        i, id_ranges_sorted, merged_id_ranges = merge_ranges(i, currb, id_ranges_sorted, merged_id_ranges)

    # merged_id_ranges.append(currb)

    # print(id_ranges_sorted)
    # print()
    # print(f"merged results: {merged_id_ranges}")
    # print(f"count of merged ranges: {len(merged_id_ranges)}")
    freshcount = 0
    for lb, rb in merged_id_ranges:
        freshcount += rb - lb + 1

    result = freshcount
    print(f"Part 2 result is: {result}")

    end_time = time.time()
    print(f"Part 2 execution time: {end_time - start_time} seconds")
