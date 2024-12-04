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

# read input data and split into list of lines
grid = open(ARG_data).read().split('\n')

directions = {
    "N": [(-1,0),(-2,0),(-3,0)],
    "S": [(1,0),(2,0),(3,0)],
    "W": [(0,-1),(0,-2),(0,-3)],
    "E": [(0,1),(0,2),(0,3)], 
    "NW": [(-1,-1),(-2,-2),(-3,-3)],
    "NE": [(-1,1),(-2,2),(-3,3)],
    "SE": [(1,1),(2,2),(3,3)],
    "SW": [(1,-1),(2,-2),(3,-3)],
}

line_max = len(grid[0]) - 1
row_max = len(grid) - 1

for ri, row in enumerate(grid):
    for ci,letter in enumerate(row):
        #Part 1
        if grid[ri][ci] == "X":
            debug(f"Found X at ({ri:3},{ci:3})")
            for cardinal, dir in directions.items():
                # check if we're in-bounds
                if (
                    (0 <= (ri + dir[0][0]) <= row_max and 0 <= (ri + dir[1][0]) <= row_max and 0 <= (ri + dir[2][0]) <= row_max) and
                    (0 <= (ci + dir[0][1]) <= line_max and 0 <= (ci + dir[1][1]) <= line_max and 0 <= (ci + dir[2][1]) <= line_max)
                ):
                    # Have we found MAS?
                    if (grid[ri + dir[0][0]][ci + dir[0][1]] == "M" and 
                        grid[ri + dir[1][0]][ci + dir[1][1]] == "A" and 
                        grid[ri + dir[2][0]][ci + dir[2][1]] == "S"):
                        debug(f"  XMAS going {cardinal}")
                        answer_p1 += 1

for ri, row in enumerate(grid[1:]):
    for ci,letter in enumerate(row[1:]):
        # Part 2
        if grid[ri][ci] == "A":
            debug(f"Found A at ({ri:3},{ci:3})")
            # See if the letters in the opposite corners make an X-MAS
            if (grid[ri + -1][ci + -1] + grid[ri + 1][ci + 1] in ["MS", "SM"] and 
                grid[ri + -1][ci + 1] + grid[ri + 1][ci + -1] in ["MS", "SM"]):
                debug(f"  X-MAS!")
                answer_p2 += 1


# Print out the answers
print(f"\33[32m__P1__ : \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__ : \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print("\33[35mTook \33[1;35m{}\33[0m\33[35m seconds to run\33[0m".format(time.process_time_ns() / 1000000000))