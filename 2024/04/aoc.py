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
    #print(f"{ri=}; {row=}")
    for ci,letter in enumerate(row):
        #print(f"{li=}; {letter=}")
        if grid[ri][ci] == "X":
            #print(f"Found X at ({ri}, {li})")
            for dir, cardinal in directions.items():
                l1, l2, l3 = None, None, None
                if (
                    (0 <= (ri + cardinal[0][0]) <= row_max and 0 <= (ri + cardinal[1][0]) <= row_max and 0 <= (ri + cardinal[2][0]) <= row_max) and
                    (0 <= (ci + cardinal[0][1]) <= line_max and 0 <= (ci + cardinal[1][1]) <= line_max and 0 <= (ci + cardinal[2][1]) <= line_max)
                ):
                    l1 = grid[ri + cardinal[0][0]][ci + cardinal[0][1]]
                    l2 = grid[ri + cardinal[1][0]][ci + cardinal[1][1]]
                    l3 = grid[ri + cardinal[2][0]][ci + cardinal[2][1]]

                    if ( l1 == "M" and l2 == "A" and l3 == "S"):
                        debug(f"Found XMAS going {dir} from ({ri},{ci})")
                        l = f"  XMAS = {grid[ri][ci]}({ri},{ci}); {l1}({ri + cardinal[0][0]},{ci + cardinal[0][1]}); "
                        l += f"{l2}({ri + cardinal[1][0]},{ci + cardinal[1][1]}); {l3}({ri + cardinal[2][0]},{ci + cardinal[2][1]})"
                        debug(l)
                        answer_p1 += 1


# Print out the answers
print(f"\33[32m__P1__ : \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__ : \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print("\33[35mTook \33[1;35m{}\33[0m\33[35m seconds to run\33[0m".format(time.process_time_ns() / 1000000000))