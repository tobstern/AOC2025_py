import time
import os
from collections import deque
import heapq

# Import ILP solver for optimization
try:
    from pulp import LpMinimize, LpProblem, LpVariable, lpSum, LpInteger, value
except ImportError:
    print("Installing pulp...")
    import subprocess

    subprocess.check_call(["pip", "install", "pulp"])
    from pulp import LpMinimize, LpProblem, LpVariable, lpSum, LpInteger, value


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
        joltage_state = initial_lights[mc]
        curr_buttons = button_wirings[mc]

        # do BFS:
        button_press_count = 0
        ini_state = joltage_state
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
    for b in button:
        state_li[b] += 1
    # print(state_li)
    return tuple(state_li)


def part2(input_str):
    start_time = time.time()
    filename = os.path.basename(__file__)
    day_num = filename.replace("day", "").replace(".py", "").strip()
    print(f"Day {day_num}, Part 2:")

    result = 0

    lights = []
    initial_lights = []
    button_wirings = []
    joltage_reqs = []
    initial_joltages = []
    for line in input_str.strip().splitlines():
        line_elems = line.split()
        lights.append(tuple(line_elems[0][1:-1]))
        initial_lights.append(tuple("." for _ in range(len(lights[-1]))))
        button_wirings.append(list(tuple(map(int, (s[1:-1].split(",")))) for s in line_elems[1:-1]))
        joltage_reqs.append(tuple(map(int, line_elems[-1][1:-1].split(","))))
        initial_joltages.append(tuple(0 for _ in range(len(lights[-1]))))

    print(lights)
    print(initial_lights)
    print(button_wirings)
    print(joltage_reqs)
    print(initial_joltages)

    ########## - Solution with help from Claude Sonnet... - ###################
    # BFS of course did not work here for the real input (joltages of ~ 200 etc.)
    # Solve using Integer Linear Programming (ILP)
    # For each machine, we need to find the minimum number of button presses
    # such that each position reaches its target joltage
    button_presses_tot = 0
    for mc, joltage_aim in enumerate(joltage_reqs):
        print(f"Solving machine {mc + 1}/{len(joltage_reqs)}...")

        curr_buttons = button_wirings[mc]
        num_positions = len(joltage_aim)
        num_buttons = len(curr_buttons)

        # Create the LP problem: minimize total button presses
        prob = LpProblem(f"Machine_{mc}", LpMinimize)

        # Decision variables: how many times to press each button (non-negative integers)
        button_presses = [LpVariable(f"button_{i}", lowBound=0, cat=LpInteger) for i in range(num_buttons)]

        # Objective: minimize total button presses
        prob += lpSum(button_presses), "Total_Button_Presses"

        # Constraints: each position must reach exactly its target joltage
        # For each position, sum up contributions from all buttons that affect it
        for pos in range(num_positions):
            # Find which buttons affect this position
            contribution = []
            for btn_idx, button in enumerate(curr_buttons):
                if pos in button:
                    # This button adds 1 to this position when pressed
                    contribution.append(button_presses[btn_idx])

            # The sum of contributions must equal the target joltage for this position
            prob += lpSum(contribution) == joltage_aim[pos], f"Position_{pos}_Target"

        # Solve the problem
        prob.solve()

        # Check if solution was found
        if prob.status == 1:  # Optimal solution found
            total_presses = int(value(prob.objective))
            result += total_presses
            print(f"  Solution: {total_presses} presses")
        else:
            print(f"  No solution found! Status: {prob.status}")

    print(f"Part 2 result is: {result}")

    end_time = time.time()
    print(f"Part 2 execution time: {end_time - start_time} seconds")
