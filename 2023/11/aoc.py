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

galaxies = []

#        x  y
empty = [[],[]]

# loop through data
for y, line in enumerate(grid):
    if line.count("#") == 0:
        empty[1].append(y)
    #grid.append(line)

# Spin the gride 90 degres clock-wise
spun = list(zip(*grid[::-1]))

for x, line in enumerate(spun):
    if line.count("#") == 0:
        empty[0].append(x)

galaxies_x_p1 = []
galaxies_y_p1 = []

expansion = 1000000
galaxies_x_p2 = []
galaxies_y_p2 = []
for y, line in enumerate(grid):
    for x, char in enumerate(line):
        if char == "#":
            galaxies_x_p1.append(x + sum(1 for i in empty[0] if i < x) * (2 - 1))
            galaxies_y_p1.append(y + sum(1 for i in empty[1] if i < y) * (2 - 1))
            galaxies_x_p2.append(x + sum(1 for i in empty[0] if i < x) * (expansion - 1))
            galaxies_y_p2.append(y + sum(1 for i in empty[1] if i < y) * (expansion - 1))


def distancesum (arr, n):
    # sorting the array.
    arr.sort()
    # for each point, finding 
    # the distance.
    res = 0
    sum = 0
    for i in range(n):
        res += (arr[i] * i - sum)
        sum += arr[i]
    return res

def totaldistancesum( x , y , n ):
    return distancesum(x, n) + distancesum(y, n)

answer_p1 = totaldistancesum(galaxies_x_p1, galaxies_y_p1, len(galaxies_x_p1))
answer_p2 = totaldistancesum(galaxies_x_p2, galaxies_y_p2, len(galaxies_x_p2))


# Print out the answers
print(f"\33[32m__P1__ : \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__ : \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print("\33[35mTook \33[1;35m{}\33[0m\33[35m seconds to run\33[0m".format(time.process_time_ns() / 1000000000))