import sys, getopt
import time

# By default I want the real input, and *not* to debug.
ARG_data = 'input.txt'
ARG_debugLogging = False

# Get the args off the command-line
opts, args = getopt.getopt(sys.argv[1:],"td",["test","debug"])
for opt, arg in opts:
    if opt in ("-t", "--test"):
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
data = open(ARG_data).read().split('\n')

x_limit = [0,len(data[0]) - 1]
y_limit = [0,len(data) - 1]

def in_bounds(p, offset):
    #debug(f' in_bounds: ({x_limit[0] <= p[0] + offset[0] <= x_limit[1]}),({y_limit[0] <= p[1] + offset[1] <= y_limit[1]})')
    #debug(f'            ({p[0] + offset[0]}),({p[1] + offset[1]})')
    if (x_limit[0] <= p[0] + offset[0] <= x_limit[1]) and (y_limit[0] <= p[1] + offset[1] <= y_limit[1]):
        return True
    return False

grid = []
start = []

#                        N                        E                        S                        W 
connection_directions = [[0,-1, ("|", "F", "7")], [1, 0, ("-", "J", "7")], [0, 1, ("|", "J", "L")], [-1,0, ("-", "L", "F")]]


# | ║
# - ═
# L ╚
# J ╝
# 7 ╗
# F ╔


start = []
current = []
# loop through data
for y,line in enumerate(data):
    grid.append(line)
    if line.count('S'):
        start = [line.index('S'), y]
        

       


debug(grid)
debug(f'start({start})')

for d in connection_directions:
    if in_bounds(start, d) and grid[start[0] + d[0]][start[1] + d[1]] in d[2]:
        current = [start[0] + d[0], start[1] + d[1]]

        break

path = [current]
while current != start:
    for d in connection_directions:
        n = [current[0] + d[0], current[1] + d[1]]
        debug(f' current = {current}; looking for {d[2]} in {grid[n[0]][n[1]]}, at {n}')

        if in_bounds(start, d):
            if grid[n[0]][n[1]] in d[2]:
                if n not in path:
                    debug(f' found {grid[n[0]][n[1]]} at ({n})')
                    current = n
                    path.append(n)
                    break
    time.sleep(1)

        


# Print out the answers
print(f"\33[32m__P1__ : \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__ : \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print("\33[35mTook \33[1;35m{}\33[0m\33[35m seconds to run\33[0m".format(time.process_time_ns() / 1000000000))