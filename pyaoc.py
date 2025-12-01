import sys
import os
import requests
import importlib


def read_txt(day):
    if int(day.split("_")[0]) < 10:
        filename = f"./puzzle_inputs/day0{day}.txt"
    else:
        filename = f"./puzzle_inputs/day{day}.txt"

    if os.path.exists(filename):
        try:
            return open(filename, "r").read()
        except Exception as e:
            exit(f"Stopped - Could not read the file: {e}")
    else:
        print(f"File {filename} not found.")
        # Try to download the puzzle input
        url = f"https://adventofcode.com/2025/day/{day}/input"  # attention!!! -> adapt the year accordingly!!!
        session_cookie = open("session_cookie.txt", "r").read().strip()
        headers = {"Cookie": f"session={session_cookie}"}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                with open(filename, "w") as file:
                    file.write(response.text)
                print("File downloaded")
            else:
                print(f"Failed to download file, HTTP response code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Failed to download file, error: {e}")

        return open(filename, "r").read().strip() if os.path.exists(filename) else ""


# Define other day and part functions similarly...


def main():
    if len(sys.argv) < 3:
        print("Please provide the day and part as command line arguments. Example: python pyaoc.py 1 1")
        return

    day = sys.argv[1]
    part = sys.argv[2]

    input_str = read_txt(day)

    if "test" in day:
        day = day.split("_test")[0]

    try:
        day_module = importlib.import_module(f"days.day{day.zfill(2)}")
    except ModuleNotFoundError:
        print(f"No module found for day {day}")
        return

    func = getattr(day_module, f"part{part}", None)
    if func:
        func(input_str)
    else:
        print(f"No function found for day {day}, part {part}")


if __name__ == "__main__":
    main()
