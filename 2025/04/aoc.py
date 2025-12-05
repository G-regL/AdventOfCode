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

answer_p1 = 0
answer_p2 = 0

#INPUT
data = open('input.txt').read().split('\n')
grid = {(r,c): char for r, row in enumerate(data) for c, char in enumerate(row)}

#             W        NW       N        NE      E        SE       S        SW
directions = [(0, -1), (-1,-1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]

# Do things!!
for (row, col), cell in grid.items():
    if cell == ".":
        continue

    rolls_seen = 0
    for dc, dr in directions:
        if rolls_seen > 4:
            break;
        
        look = (row + dr, col + dc)
        if look in grid and grid[look] == "@":
            rolls_seen += 1

    if rolls_seen < 4:
        answer_p1 += 1

# Print out the answers
print(f"\33[32m__P1__: \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__: \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print(f"\33[35mTook \33[1;35m{time.process_time_ns() / 1000000000}\33[0m\33[35m seconds to run\33[0m")