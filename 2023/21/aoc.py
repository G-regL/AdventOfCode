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
grid = open(ARG_data).read().split('\n')

x_limit = (0, len(grid[0]) - 1)
y_limit = (0, len(grid) - 1)

start = ()
# loop through rows/columns
for y,line in enumerate(grid):
    if line.count('S'):
        start = (line.index('S'), y)
        
positions = set([start])

#              Up       Down    Left     Right
directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

# Do 64 full steps
for _ in range(64):
    # initialize the new position set for this step
    new_positions = set()
    # for each position we *could* be at..
    for pos in positions:
        # Check
        for dir_x, dir_y in directions:
            look_x, look_y = pos[0] + dir_x, pos[1] + dir_y
            inbounds = (x_limit[0] <= look_x <= x_limit[1]) and (y_limit[0] <= look_y <= y_limit[1])
            if inbounds and grid[look_x][look_y] == ".":
                new_positions.add((look_x, look_y))
                
    positions = new_positions

positions.add(start)

def part2_from_reddit(data): # https://www.reddit.com/r/adventofcode/comments/18nevo3/comment/keavm0j
    n = len(data)
    sparse = {(i,j) for i in range(n) for j in range(n) if data[i][j] in '.S'}
    S = next((i,j) for i in range(n) for j in range(n) if data[i][j] == 'S')
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]

    def tadd(a,b): return ((a[0]+b[0]),(a[1]+b[1]))
    def modp(a): return(a[0]%n, a[1]%n)

    visited, new, cache = {S}, {S}, {0:1}
    k, r  = 26501365//n, 26501365%n

    for c in range(1,r+2*n+1):
        visited, new = new, { np for p in new for di in dirs for np in [tadd(p,di)] if np not in visited and modp(np) in sparse}
        cache[c] = len(new) + (cache[c-2] if c>1 else 0)

    d2 = cache[r+2*n]+cache[r]-2*cache[r+n]
    d1 = cache[r+2*n]-cache[r+n]
    #_ = ic(cache)
    return cache[r+2*n]+(k-2)*(2*d1+(k-1)*d2)//2


# Print out the answers
print(f"\33[32m__P1__ : \33[1m{len(positions)}\33[0m")
print(f"\33[32m__P2__ : \33[1m{part2_from_reddit(grid)}\33[0m")

# Tell me how inefficecient my code is
print("\33[35mTook \33[1;35m{}\33[0m\33[35m seconds to run\33[0m".format(time.process_time_ns() / 1000000000))