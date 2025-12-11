import time
import os


def dfs(conns_lib, node, count):
    if node == "out":
        # print(f"node:{node} and count:{count}")
        return count + 1

    # do something with node etc...
    # print(f"node:{node} and count:{count}")
    for child in conns_lib[node]:
        count = dfs(conns_lib, child, count)

    return count


def part1(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 1:")
    # Implement the logic here

    conns_lib = dict()
    for line in input_str.strip().splitlines():
        left, right = line.split(": ")
        conns_lib[left] = right.strip().split()
    # print(conns_lib)

    path_count = 0

    # DFS depth first search
    start = "you"
    aim = "out"
    # result = 0

    result = dfs(conns_lib, start, path_count)

    # result = path_count
    print(f"Part 1 result is: {result}")

    end_time = time.time()
    print(f"Part 1 execution time: {end_time - start_time} seconds")


def dfs_dacfft(conns_lib, node, count, seen_thetwo, vis, cache):
    # Detect cycles per-path; do not traverse already-on-path nodes
    if node in vis:
        return count

    seen_dac, seen_fft = seen_thetwo
    if node == "out":
        return 1 if (seen_dac and seen_fft) else 0
    # Mark current node in the path
    vis.add(node)

    # do something with node etc...
    # print(f"node:{node} and count:{count}")
    if node == "dac":
        seen_dac = True
    if node == "fft":
        seen_fft = True
    # print(f"{seen_dac and seen_fft} . dac:{seen_dac} . fft:{seen_fft}")

    # Memoization on (node, seen_dac, seen_fft)
    key = (node, seen_dac, seen_fft)
    if key in cache:
        cached = cache[key]
        vis.remove(node)
        return cached

    total = 0
    for child in conns_lib[node]:
        total += dfs_dacfft(conns_lib, child, 0, (seen_dac, seen_fft), vis, cache)

    # Backtrack: remove current node so siblings can traverse it via different paths
    vis.remove(node)

    cache[key] = total
    return total


def part2(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 2:")

    conns_lib = dict()
    for line in input_str.strip().splitlines():
        left, right = line.split(": ")
        conns_lib[left] = right.strip().split()
    # print(conns_lib)

    path_count = 0

    # DFS depth first search
    start = "svr"  # server rack
    aim = "out"
    # result = 0
    visited = set()
    cache = {}

    # required nodes seen
    seen_dac_fft = (False, False)

    result = dfs_dacfft(conns_lib, start, path_count, seen_dac_fft, visited, cache)
    print(f"Part 2 result is: {result}")

    end_time = time.time()
    print(f"Part 2 execution time: {end_time - start_time} seconds")
