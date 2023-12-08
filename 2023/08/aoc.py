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
        print(f"DEBUG: {thing}")

answer_p1 = 0
answer_p2 = 0

# read input data and split into list of lines
data = open(ARG_data).read().split('\n')

directions = data[0]

moves = {}
# loop through data
for line in data[2:]:
    coord, pair = line.split(' = ')
    pair = pair[1:-1].split(', ')
    moves[coord] = {"L": pair[0], "R": pair[1]}

debug(f'{moves}')
debug(len(directions))

FoundZZZ = False
current_coord = 'AAA'
move_incrementer = 0
#steps = 1
while current_coord != 'ZZZ':
    if move_incrementer >= len(directions):
        debug(f'Reset move_incrementer')
        move_incrementer = 0
    past_coord = current_coord
    current_coord = moves[current_coord][directions[move_incrementer]]
    debug(f'Moved {past_coord} -> {current_coord}; move_incrementer({move_incrementer}), answer_p1({answer_p1})')
    move_incrementer += 1
    answer_p1 += 1

# Print out the answers
print(f"__P1__ : {answer_p1}")
print(f"__P2__ : {answer_p2}")

# Tell me how inefficecient my code is
print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))