import getopt
import sys
import time

# By default I want the real input, and *not* to debug.
ARG_data = "input.txt"
ARG_debugLogging = False

# Get the args off the command-line
opts, args = getopt.getopt(sys.argv[1:], "td", ["test", "debug"])
for opt, arg in opts:
    if opt in ("-t", "--test"):
        print(f"\33[31mUSING TEST DATA\33[0m")
        ARG_data = "test.txt"
    elif opt in ("-d", "--debug"):
        ARG_debugLogging = True


# Useful during testing to see what the hell is going on
def debug(thing):
    if ARG_debugLogging:
        print(f"\33[39mDEBUG:\33[0m {thing}")


answer_p1 = 0
answer_p2 = 0

# INPUT
lines = open(ARG_data).read().split("\n")
grid = [list(row) for row in lines]
# grid = {(r, c): char for r, row in enumerate(data) for c, char in enumerate(row)}
start_col = lines[0].find("S")
# grid[(1, start[1])] = "|"
grid[1][start_col] = "|"


# Do things!!
for row in range(2, len(grid)):
    for col, _ in enumerate(grid[row]):
        if grid[row][col] == "^" and grid[row - 1][col] == "|":
            answer_p1 += 1
            grid[row][col - 1] = grid[row][col + 1] = "|"
        elif grid[row - 1][col] == "|":
            grid[row][col] = "|"

# Print out the answers
print(f"\33[32m__P1__: \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__: \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print(
    f"\33[35mTook \33[1;35m{time.process_time_ns() / 1000000000}\33[0m\33[35m seconds to run\33[0m"
)
