import sys, getopt
import time

# By default I want the real input, and *not* to debug.
ARG_data = 'input.txt'
ARG_debugLogging = False
ARG_p1_start = 'AAA'
ARG_p1_end = 'ZZZ'
ARG_p2_wanted_z = 6

# Get the args off the command-line
opts, args = getopt.getopt(sys.argv[1:],"td",["test","debug"])
for opt, arg in opts:
    if opt in ("-t", "--test"):
        ARG_data = 'test.txt'
        ARG_p1_start = '11A'
        ARG_p1_end = '11Z'
        ARG_p2_wanted_z = 2
    elif opt in ("-d", "--debug"):
        ARG_debugLogging = True

# Useful during testing to see what the hell is going on
def debug(thing):
    if ARG_debugLogging:
        print(f"DEBUG: {thing}")

answer_p1 = 0
answer_p2 = 0

# read input data and split into list of lines
data = open(ARG_data).read().split('\n')

directions = data[0]

current_coords_p2 = {}

moves = {}
# loop through data
for line in data[2:]:
    coord, pair = line.split(' = ')
    pair = pair[1:-1].split(', ')
    p = {"L": pair[0], "R": pair[1]}
    moves[coord] = p

    if coord[2] == 'A':
        current_coords_p2[coord] = coord

# Part 1
current_coord = ARG_p1_start
move_incrementer = 0
while current_coord != ARG_p1_end:
    if move_incrementer >= len(directions):
        move_incrementer = 0

    past_coord = current_coord
    current_coord = moves[current_coord][directions[move_incrementer]]
    debug(f'P1 - Moved {past_coord} -> {current_coord}; move_incrementer({move_incrementer}), answer_p1({answer_p1})')
    move_incrementer += 1
    answer_p1 += 1


# Part 2
from math import gcd
from functools import reduce
a_coord_counts = []
for a_coord, current_coord_p2 in current_coords_p2.items():
    a_coord_steps = 0
    move_incrementer = 0
    
    while current_coord_p2[2] != 'Z':
        if move_incrementer >= len(directions):
            move_incrementer = 0
    
        current_coord_p2 = moves[current_coord_p2][directions[move_incrementer]]
        move_incrementer += 1
        a_coord_steps += 1

    a_coord_counts.append(a_coord_steps)

answer_p2 = reduce((lambda x, y: int(x * y / gcd(x, y))), a_coord_counts)

# Print out the answers
print(f"__P1__ Steps to reach {ARG_p1_end}: {answer_p1}")
print(f"__P2__ Steps to simultaneously reach all Z-ending locations: {answer_p2}")

# Tell me how inefficecient my code is
print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))