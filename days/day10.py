import time
import os
from collections import deque
import heapq
from functools import cache
from itertools import combinations, product
import pprint

pp = pprint.PrettyPrinter(width=120)


#
def match_light(state, aim):
    return all([state[i] == aim[i] for i in range(len(aim))])


def apply_button(state, button):
    state_li = list(state)
    for b in button:
        onoroff = state[b]
        if onoroff == "#":
            # toggle to off
            state_li[b] = "."
        elif onoroff == ".":
            # toggle to on
            state_li[b] = "#"
    return tuple(state_li)


def part1(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 1:")
    # Implement the logic here
    result = 0

    lights = []
    initial_lights = []
    button_wirings = []
    joltage_reqs = []
    for line in input_str.strip().splitlines():
        line_elems = line.split()
        lights.append(tuple(line_elems[0][1:-1]))
        initial_lights.append(tuple("." for _ in range(len(lights[-1]))))
        button_wirings.append(list(tuple(map(int, (s[1:-1].split(",")))) for s in line_elems[1:-1]))
        joltage_reqs.append(tuple(map(int, line_elems[-1][1:-1].split(","))))
    # print(lights)
    # print(initial_lights)
    # print(button_wirings)
    # print(joltage_reqs)

    # find the shortest count of button presses to arrive at the lights state: "#"=on, "."=off
    button_presses_tot = 0
    for mc, light_aim in enumerate(lights):

        working_comb = []
        curr_min_count = None
        light_state = initial_lights[mc]
        curr_buttons = button_wirings[mc]

        # do BFS:
        button_press_count = 0
        ini_state = light_state
        queue = deque([(ini_state, button_press_count)])

        seen_states = {ini_state}
        # print(seen_states)

        while queue:
            # print(queue)
            # print(queue.popleft())

            cs, bt_pr_ct = queue.popleft()

            if cs == light_aim:
                # print(bt_pr_ct)
                result += bt_pr_ct
                break

            # check if already seen the combination:

            for button in curr_buttons:
                ns = apply_button(cs, button)

                if ns not in seen_states:
                    seen_states.add(ns)
                    queue.append((ns, bt_pr_ct + 1))

    print(f"Part 1 result is: {result}")

    end_time = time.time()
    print(f"Part 1 execution time: {end_time - start_time} seconds")


def apply_button_joltage(state, button):
    state_li = list(state)
    # print(state, type(state))
    for b in button:
        state_li[b] += 1
    # print(state_li)
    return tuple(state_li)


def apply_button_toggle(state, button):
    state_li = list(state)
    # print(state, type(state))
    for b in button:
        state_li[b] += 1
        state_li[b] %= 2
    # print(state_li)
    return tuple(state_li)


def combs(all_buttons):
    # Return unique button combinations as frozensets
    if not all_buttons:
        return {frozenset()}

    combos = {frozenset()}
    for button in all_buttons:
        new_combos = {combo | {button} for combo in combos}
        combos |= new_combos
    return combos


def patterns(coeffs):
    # coeffs: list of 0/1 tuples (button -> counters mask)
    num_buttons = len(coeffs)
    num_variables = len(coeffs[0]) if coeffs else 0
    out = {parity_pattern: {} for parity_pattern in product(range(2), repeat=num_variables)}
    # enumerate all subsets of buttons
    for num_pressed_buttons in range(num_buttons + 1):
        for buttons in combinations(range(num_buttons), num_pressed_buttons):
            # compute numeric pattern = sum of selected button vectors (elementwise)
            pattern = tuple(map(sum, zip((0,) * num_variables, *(coeffs[i] for i in buttons))))
            parity_pattern = tuple(i % 2 for i in pattern)
            # keep minimal number of buttons that produce this numeric pattern
            if pattern not in out[parity_pattern]:
                out[parity_pattern][pattern] = num_pressed_buttons
    return out


def solve_single(coeffs, goal):
    # precompute pattern -> minimal cost grouped by parity
    pattern_costs = patterns(coeffs)

    @cache
    def solve_single_aux(goal_tup):
        # goal_tup: tuple of nonnegative integers
        if all(i == 0 for i in goal_tup):
            return 0
        answer = 10**12
        parity = tuple(i % 2 for i in goal_tup)
        # iterate all numeric patterns matching this parity
        for pattern, pattern_cost in pattern_costs[parity].items():
            # must not subtract more than goal
            if all(pi <= gi for pi, gi in zip(pattern, goal_tup)):
                new_goal = tuple((gi - pi) // 2 for pi, gi in zip(pattern, goal_tup))
                candidate = pattern_cost + 2 * solve_single_aux(new_goal)
                if candidate < answer:
                    answer = candidate
        return answer

    return solve_single_aux(tuple(goal))


def part2(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 2:")

    result = 0

    # parse each line into coeffs (button vectors) and goal (numeric tuple)
    lights = []
    initial_lights = []
    button_wirings = []
    joltage_reqs = []
    initial_joltages = []
    # ensure the user's snippet variable name is available

    # print(input_str)
    for line in input_str.strip().splitlines():
        line_elems = line.split()
        lights.append(tuple(line_elems[0][1:-1]))
        initial_lights.append(tuple("." for _ in range(len(lights[-1]))))
        button_wirings.append(list(tuple(map(int, (s[1:-1].split(",")))) for s in line_elems[1:-1]))
        joltage_reqs.append(tuple(map(int, line_elems[-1][1:-1].split(","))))
        initial_joltages.append(tuple(0 for _ in range(len(lights[-1]))))

    # Build `parsed` as list of (coeffs, goal) where coeffs are 0/1 tuples for each button
    parsed = []
    for bw, goal in zip(button_wirings, joltage_reqs):
        coeffs = [tuple(1 if i in btn else 0 for i in range(len(goal))) for btn in bw]
        parsed.append((coeffs, goal))

    # print("Parsed", len(parsed), "lines")
    # for i, (c, g) in enumerate(parsed, 1):
    #     print("Line", i, "goal=", g, "buttons=", len(c))
    #     if len(c) <= 16:
    #         print(" example buttons (first 6):")
    #         pp.pprint(c[:6])
    #     else:
    #         print("many buttons; first 6 shown:")
    #         pp.pprint(c[:6])

    coeffs0, goal0 = parsed[0]
    # print(f"coeffs: {coeffs0}")
    pat = patterns(coeffs0)
    # print(f"created patterns: {pat}")
    counts = {p: len(dic) for p, dic in pat.items()}
    # show number of numeric patterns for a few parity buckets (non-empty ones)
    nonempty = {p: cnt for p, cnt in counts.items() if cnt}
    # print("non-empty parity buckets:", len(nonempty))
    # show smallest few entries for parity of the goal
    goal_par = tuple(i % 2 for i in goal0)
    # print("goal parity =", goal_par)
    # print("number of numeric patterns for this parity:", len(pat[goal_par]))
    # show up to 12 pattern->cost items
    for i, (pattern, cost) in enumerate(sorted(pat[goal_par].items())[:12]):
        print(i + 1, pattern, "cost=", cost)

    total = 0
    for i, (coeffs, goal) in enumerate(parsed, 1):
        # print("\nSolving line", i, "goal=", goal)
        ans = solve_single(coeffs, goal)
        # print(" -> minimal presses =", ans)
        total += ans
    print("\nTotal =", total)

    # exit()

    # print(f"Part 2 result is: {result}")

    end_time = time.time()
    print(f"Part 2 execution time: {end_time - start_time} seconds")
