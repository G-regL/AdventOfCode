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

#points = []

directions = {
    "U":(-1, 0), "D":(1, 0), "L": (0, -1), "R": (0, 1), 
    "3":(-1, 0), "1":(1, 0), "2": (0, -1), "0": (0, 1)
    }

dir_trans = ["R", "D", "L", "U"]

position = (0,0)
position_p2 = (0,0)
boundary = 0
boundary_p2 = 0

shoeguy = 0
shoeguy_p2 = 0
# loop through data
for line in data:
    dir, dist, colour = line.split()

    #Part 1
    dist = int(dist)
    next_x = position[0] + (directions[dir][0] * dist)
    next_y = position[1] + (directions[dir][1] * dist)

    shoeguy += position[0] * next_y - position[1] * next_x
    position = (next_x, next_y)
    boundary += dist

    #Part 2
    dist_p2 = int(colour[2:-2],16)
    debug(f' dist_p2 ({dist_p2}) ({colour[2:-2]})')
    debug(f' direction_p2 ({dir_trans[int(colour[-2])]})')
    next_x_p2 = position_p2[0] + (directions[colour[-2]][0] * dist_p2)
    next_y_p2 = position_p2[1] + (directions[colour[-2]][1] * dist_p2)
    
    shoeguy_p2 += position_p2[0] * next_y_p2 - position_p2[1] * next_x_p2
    position_p2 = (next_x_p2, next_y_p2)
    boundary_p2 += dist_p2


#debug(f' Final shoeguy = {abs(shoeguy) // 2}')
#debug(f' boundary = {boundary} ')
answer_p1 = (abs(shoeguy) // 2) - (boundary // 2) + 1 + boundary

answer_p2 = (abs(shoeguy_p2) // 2) - (boundary_p2 // 2) + 1 + boundary_p2


# Print out the answers
print(f"\33[32m__P1__ : \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__ : \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print("\33[35mTook \33[1;35m{}\33[0m\33[35m seconds to run\33[0m".format(time.process_time_ns() / 1000000000))