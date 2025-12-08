import time
import os
from collections import defaultdict as dd


def prod(li):
    res = 1
    for num in li:
        res *= num
    return res


def part1(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 1:")

    loop_lim = 0
    test_input = 0
    if test_input:
        loop_lim = 10
        print(f"Test input, thus: loop till {loop_lim}")
    else:
        loop_lim = 1000
        print(f"Real input, thus: loop till {loop_lim}")

    juncboxes = []
    for line in input_str.strip().splitlines():
        juncboxes.append(tuple(map(int, line.split(","))))
    # print(juncboxes)

    # Calculate all pair distances once
    all_pairs = []
    for i, box1 in enumerate(juncboxes):
        for j, box2 in enumerate(juncboxes):
            if i < j:  # Only calculate each pair once
                dist = ((box1[0] - box2[0]) ** 2 + (box1[1] - box2[1]) ** 2 + (box1[2] - box2[2]) ** 2) ** 0.5
                all_pairs.append((dist, box1, box2))
    all_pairs.sort()  # Sort by distance

    linked_dists = set()

    # print(linked_dists)

    circuits = []
    last_min_dist = 0

    actual_conns = 0
    pair_idx = 0
    successfull = False
    while actual_conns < loop_lim and pair_idx < len(all_pairs):
        curr_min_dist, starting_minbox, aiming_minbox = all_pairs[pair_idx]
        pair_idx += 1

        actual_conns += 1
        # connect junction boxes with shortest distance
        # check if already in same circuit:
        same_circ = False
        for set_collec in circuits:
            if starting_minbox in set_collec and aiming_minbox in set_collec:
                same_circ = True
                break
        if same_circ:
            # skip this pair
            continue

        # print()
        # print(f"junction pair: {starting_minbox} and {aiming_minbox} with mindist: {curr_min_dist}")

        # temp_circuits = circuits.copy()
        circuits_with_starting = [i for i, circ in enumerate(circuits) if starting_minbox in circ]
        circuits_with_aiming = [i for i, circ in enumerate(circuits) if aiming_minbox in circ]

        if not circuits_with_starting and not circuits_with_aiming:
            # both empty -> create new circuit
            circuits.append({starting_minbox, aiming_minbox})
            # actual_conns += 1

        elif circuits_with_starting and circuits_with_aiming:
            # sth is there:
            if circuits_with_starting[0] != circuits_with_aiming[0]:
                # not same circuit indice
                # merge both circs:
                circuits[circuits_with_starting[0]].update(circuits[circuits_with_aiming[0]])
                circuits.pop(circuits_with_aiming[0])
                # actual_conns += 1

        elif circuits_with_starting:
            # only starting exists - add aiming
            circuits[circuits_with_starting[0]].add(aiming_minbox)
            # actual_conns += 1

        else:
            # only aiming exists - add starting
            circuits[circuits_with_aiming[0]].add(starting_minbox)
            # actual_conns += 1

        # print(f"circuits: {circuits}")

    circ_lens = sorted([len(circ) for circ in circuits], reverse=True)
    result = prod(circ_lens[:3])
    print(f"Part 1 result is: {result}")

    end_time = time.time()
    print(f"Part 1 execution time: {end_time - start_time} seconds")


def part2(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 2:")

    juncboxes = []
    for line in input_str.strip().splitlines():
        juncboxes.append(tuple(map(int, line.split(","))))
    # print(juncboxes)

    # Calculate all pair distances once
    all_pairs = []
    for i, box1 in enumerate(juncboxes):
        for j, box2 in enumerate(juncboxes):
            if i < j:  # Only calculate each pair once
                dist = ((box1[0] - box2[0]) ** 2 + (box1[1] - box2[1]) ** 2 + (box1[2] - box2[2]) ** 2) ** 0.5
                all_pairs.append((dist, box1, box2))
    all_pairs.sort()  # Sort by distance

    linked_dists = set()

    # print(linked_dists)

    circuits = []
    last_min_dist = 0

    actual_conns = 0
    pair_idx = 0
    successfull = False
    last_pair = []

    mult_junc_boxes_res = 0
    while True:
        found = False

        for circ in circuits:
            bool_collec = []
            for box in juncboxes:
                bool_collec.append(box in circ)
            if all(bool_collec):
                found = True
                last_pair.append([starting_minbox, aiming_minbox])
                print(last_pair)
                mult_junc_boxes_res = starting_minbox[0] * aiming_minbox[0]
                break

        if found:
            break

        curr_min_dist, starting_minbox, aiming_minbox = all_pairs[pair_idx]
        pair_idx += 1

        actual_conns += 1
        # connect junction boxes with shortest distance
        # check if already in same circuit:
        same_circ = False
        for set_collec in circuits:
            if starting_minbox in set_collec and aiming_minbox in set_collec:
                same_circ = True
                break
        if same_circ:
            # skip this pair
            continue

        # print()
        # print(f"junction pair: {starting_minbox} and {aiming_minbox} with mindist: {curr_min_dist}")

        # temp_circuits = circuits.copy()
        circuits_with_starting = [i for i, circ in enumerate(circuits) if starting_minbox in circ]
        circuits_with_aiming = [i for i, circ in enumerate(circuits) if aiming_minbox in circ]

        if not circuits_with_starting and not circuits_with_aiming:
            # both empty -> create new circuit
            circuits.append({starting_minbox, aiming_minbox})
            # actual_conns += 1

        elif circuits_with_starting and circuits_with_aiming:
            # sth is there:
            if circuits_with_starting[0] != circuits_with_aiming[0]:
                # not same circuit indice
                # merge both circs:
                circuits[circuits_with_starting[0]].update(circuits[circuits_with_aiming[0]])
                circuits.pop(circuits_with_aiming[0])
                # actual_conns += 1

        elif circuits_with_starting:
            # only starting exists - add aiming
            circuits[circuits_with_starting[0]].add(aiming_minbox)
            # actual_conns += 1

        else:
            # only aiming exists - add starting
            circuits[circuits_with_aiming[0]].add(starting_minbox)
            # actual_conns += 1

        # print(f"circuits: {circuits}")

    # circ_lens = sorted([len(circ) for circ in circuits], reverse=True)
    # result = prod(circ_lens[:3])
    result = mult_junc_boxes_res
    print(f"Part 2 result is: {result}")

    end_time = time.time()
    print(f"Part 2 execution time: {end_time - start_time} seconds")
