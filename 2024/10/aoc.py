import sys, getopt
import time

# By default I want the real input, and *not* to debug.
ARG_data = 'input.txt'
ARG_debugLogging = False

# Get the args off the command-line
opts, args = getopt.getopt(sys.argv[1:],"td",["test","debug"])
for opt, arg in opts:
    if opt in ("-t", "--test"):
        print(f"\33[31mUSING TEST DATA\33[0m")
        ARG_data = 'test.txt'
    elif opt in ("-d", "--debug"):
        ARG_debugLogging = True

# Useful during testing to see what the hell is going on
def debug(thing):
    if ARG_debugLogging:
        print(f"\33[39mDEBUG:\33[0m {thing}")

def in_grid(row, col, limits) -> bool:
    return 0 <= row < limits[0] and 0 <= col < limits[1]

answer_p1 = 0
answer_p2 = 0

#----------------------------
from collections import deque

grid = [list(map(int, list(row))) for row in open(ARG_data).read().split('\n')]

limits = (len(grid[0]), len(grid))

#             Up       Down    Left     Right
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
trailheads = {}

for r, row in enumerate(grid):
    for c, char in enumerate(row):
        if char == 0:
            trailheads[(r, c)] = [0,0]


queue = deque([((r,c), 0, (r,c), set([(r,c)])) for (r,c) in trailheads.keys()])
queue.extend([((r,c), 0, (r,c), False) for (r,c) in trailheads.keys()])

while queue:
    (row, column), height, trailhead, path = queue.popleft()
    debug(f"{row=}, {column=}, {path=}, {isinstance(path, set)=}")
    #new_path = set()
    #new_path.add

    if height == 9:
        if isinstance(path, set):
            trailheads[trailhead][0] += 1
        else:
            trailheads[trailhead][1] += 1
        # if trailhead == (6,6):
        #     print(f"Found 9!! {trailhead}, ({row},{column}), {path}")
        continue

    for (dr, dc) in directions:
        #height = grid[row][column]
        row_new, column_new = row + dr, column + dc
        #if 0 > row_new or row_new >= limits[0] or 0 > column_new or column_new >= limits[1]:
        if not in_grid(row_new, column_new, limits):
            continue

        if (
            grid[row_new][column_new] == grid[row][column] + 1 and 
            ((isinstance(path, set) and (row_new, column_new) not in path) or not path)
        ):
            if isinstance(path, set):
                path.add((row_new, column_new))

            queue.append(((row_new, column_new), grid[row_new][column_new], trailhead, path))

answer_p1 = sum(i[0] for i in trailheads.values())
answer_p2 = sum(i[1] for i in trailheads.values())
#----------------------------
# # Print out the answers
print(f"\33[32m__P1__: \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__: \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print(f"\33[35mTook \33[1;35m{time.process_time_ns() / 1000000000}\33[0m\33[35m seconds to run\33[0m")