import time
import os
from bisect import bisect_left


def _build_vertical_edges(corners):
    edges = []
    for (x1, y1), (x2, y2) in zip(corners, corners[1:]):
        if x1 == x2 and y1 != y2:
            y_low, y_high = sorted((y1, y2))
            edges.append((x1, y_low, y_high))
    return edges


def _scanline_mask(xs, ys, vertical_edges):
    num_rows = len(ys) - 1
    num_cols = len(xs) - 1
    inside = [[False] * num_cols for _ in range(num_rows)]
    for row_idx in range(num_rows):
        y_mid = (ys[row_idx] + ys[row_idx + 1]) / 2
        hits = [x for x, y_low, y_high in vertical_edges if y_low <= y_mid < y_high]
        if not hits:
            continue
        hits.sort()
        if len(hits) % 2 != 0:
            raise ValueError("Scanline intersection count is odd; polygon may be invalid.")
        for i in range(0, len(hits), 2):
            x_left = hits[i]
            x_right = hits[i + 1]
            start_col = bisect_left(xs, x_left)
            end_col = bisect_left(xs, x_right)
            for col in range(start_col, end_col):
                inside[row_idx][col] = True
    return inside


def _build_prefix(mask):
    rows = len(mask)
    cols = len(mask[0]) if rows else 0
    prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r in range(rows):
        row_total = 0
        for c in range(cols):
            if mask[r][c]:
                row_total += 1
            prefix[r + 1][c + 1] = prefix[r][c + 1] + row_total
    return prefix


def _build_tile_map(corners):
    if not corners:
        return None

    polygon = corners[:]
    if polygon[0] != polygon[-1]:
        polygon.append(polygon[0])

    xs = sorted(set(x for x, _ in polygon))
    ys = sorted(set(y for _, y in polygon))
    if len(xs) < 2 or len(ys) < 2:
        return None

    vertical_edges = _build_vertical_edges(polygon)
    if not vertical_edges:
        return None

    inside_mask = _scanline_mask(xs, ys, vertical_edges)
    if not inside_mask:
        return None

    prefix = _build_prefix(inside_mask)
    return {
        "xs": xs,
        "ys": ys,
        "x_to_idx": {value: idx for idx, value in enumerate(xs)},
        "y_to_idx": {value: idx for idx, value in enumerate(ys)},
        "mask": inside_mask,
        "prefix": prefix,
    }


def _tile_exists(tile_map, x, y):
    if tile_map is None:
        return False
    x_idx = tile_map["x_to_idx"].get(x)
    y_idx = tile_map["y_to_idx"].get(y)
    if x_idx is None or y_idx is None:
        return False

    rows = len(tile_map["ys"]) - 1
    cols = len(tile_map["xs"]) - 1
    mask = tile_map["mask"]

    # A tile (x, y) is considered valid if any adjacent cell is filled.
    adjacent = False
    if y_idx > 0 and x_idx > 0:
        adjacent |= mask[y_idx - 1][x_idx - 1]
    if y_idx > 0 and x_idx < cols:
        adjacent |= mask[y_idx - 1][x_idx]
    if y_idx < rows and x_idx > 0:
        adjacent |= mask[y_idx][x_idx - 1]
    if y_idx < rows and x_idx < cols:
        adjacent |= mask[y_idx][x_idx]
    return adjacent


def _area_is_filled(tile_map, x1, y1, x2, y2):
    if tile_map is None:
        return False
    x_to_idx = tile_map["x_to_idx"]
    y_to_idx = tile_map["y_to_idx"]
    x_low_idx = x_to_idx.get(min(x1, x2))
    x_high_idx = x_to_idx.get(max(x1, x2))
    y_low_idx = y_to_idx.get(min(y1, y2))
    y_high_idx = y_to_idx.get(max(y1, y2))
    if None in (x_low_idx, x_high_idx, y_low_idx, y_high_idx):
        return False
    if x_low_idx == x_high_idx or y_low_idx == y_high_idx:
        return False

    prefix = tile_map["prefix"]
    filled = (
        prefix[y_high_idx][x_high_idx]
        - prefix[y_low_idx][x_high_idx]
        - prefix[y_high_idx][x_low_idx]
        + prefix[y_low_idx][x_low_idx]
    )
    width_cells = x_high_idx - x_low_idx
    height_cells = y_high_idx - y_low_idx
    return filled == width_cells * height_cells


def _largest_axis_aligned_rectangle(corners):
    tile_map = _build_tile_map(corners)
    if tile_map is None:
        return 0

    best_area = 0
    total_corners = len(corners)
    for idx in range(total_corners):
        x1, y1 = corners[idx]
        for jdx in range(idx + 1, total_corners):
            x2, y2 = corners[jdx]
            if x1 == x2 or y1 == y2:
                continue
            if not (
                _tile_exists(tile_map, x1, y1)
                and _tile_exists(tile_map, x2, y2)
                and _tile_exists(tile_map, x1, y2)
                and _tile_exists(tile_map, x2, y1)
            ):
                continue
            if _area_is_filled(tile_map, x1, y1, x2, y2):
                area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
                if area > best_area:
                    best_area = area

    return best_area


def part1(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 1:")
    # Implement the logic here

    corners = []
    for line in input_str.splitlines():
        corners.append(list(map(int, line.split(","))))

    # print(corners)

    # get max area of largest rect
    all_areas = set()
    for idx, (i, j) in enumerate(corners):
        for x, y in corners[idx:]:
            # print(f"i,j={i,j} and x,y={x,y}")
            all_areas.add((abs(x - i) + 1) * (abs(y - j) + 1))
    # print(all_areas)

    result = max(all_areas)
    print(f"Part 1 result is: {result}")

    end_time = time.time()
    print(f"Part 1 execution time: {end_time - start_time} seconds")


def part2(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 2:")

    corners = []
    for line in input_str.splitlines():
        corners.append(tuple(map(int, line.split(","))))
    result = _largest_axis_aligned_rectangle(corners)
    print(f"Part 2 result is: {result}")

    end_time = time.time()
    print(f"Part 2 execution time: {end_time - start_time} seconds")


# 3107840629 too high
# 4667093750
# 1429596008
