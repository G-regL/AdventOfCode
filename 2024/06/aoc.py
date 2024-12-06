import sys, getopt
import time

# By default I want the real input, and *not* to debug.
ARG_data = 'input.txt'
ARG_debugLogging = False
ARG_printgrid = 0

# Get the args off the command-line
opts, args = getopt.getopt(sys.argv[1:],"tdgG",["test","debug","grid","gridall"])
for opt, arg in opts:
    if opt in ("-t", "--test"):
        print(f"\33[31mUSING TEST DATA\33[0m")
        ARG_data = 'test.txt'
    elif opt in ("-d", "--debug"):
        ARG_debugLogging = True
    elif opt in ("-g", "--grid"):
        ARG_printgrid = 1
    elif opt in ("-G", "--gridall"):
        ARG_printgrid = 2

# Useful during testing to see what the hell is going on
def debug(thing):
    if ARG_debugLogging:
        print(f"\33[39mDEBUG:\33[0m {thing}")

answer_p1 = 0
answer_p2 = 0

grid = open(ARG_data).read().split('\n')

visited_grid = []

x_limit = len(grid[0])
y_limit = len(grid)

directions = {"^": (0, -1), ">": (1, 0), "v": (0, 1), "<": (-1,0)}
direction_list = list(directions.keys())
direction = "^"

positions = []
# loop through rows/columns
for y,line in enumerate(grid):
    if line.count('^'):
        positions.append((line.index('^'), y))

    visited_grid.append(list(line))

#new_dir = direction_list[direction_list.index(direction) + 1]
direction_list = direction_list[1:] + [direction_list[0]]

while 0 <= positions[-1][0] + directions[direction][0] < x_limit and 0 <= positions[-1][1] + directions[direction][1] < y_limit:
    new_pos = (positions[-1][0] + directions[direction][0], positions[-1][1] + directions[direction][1])
    debug(f"{new_pos=}")
    if grid[new_pos[1]][new_pos[0]] != "#":
        positions.append(new_pos)
        debug(f"Haven't found # at {new_pos} = {grid[new_pos[1]][new_pos[0]]}")
        visited_grid[positions[-1][1]][positions[-1][0]] = "X"
    else:
        old_dir = direction
        direction = direction_list[0]
        direction_list = direction_list[1:] + [direction_list[0]]
        debug(f"Found # at {new_pos}; turning right ({old_dir},{direction}), next dir={direction_list[0]}")

        if ARG_printgrid == 2:
            for row in visited_grid:
                print("".join(row))

if ARG_printgrid:
    for row in visited_grid:
        print("".join(row))

answer_p1 = len(set(positions))

# Print out the answers
print(f"\33[32m__P1__: \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__: \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print(f"\33[35mTook \33[1;35m{time.process_time_ns() / 1000000000}\33[0m\33[35m seconds to run\33[0m")