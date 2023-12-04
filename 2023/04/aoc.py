import sys, getopt
import time

import math

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
        print(f"DEBUG:{thing}")

winning_cards = []
answer_p2 = 0

# read input data and split into list of lines
data = open(ARG_data).read().split('\n')


# loop through rows/columns
for card in data:
    pass


# Print out the answers
print(f"__P1__ Sum of winning cards: {sum(winning_cards)}")
#print(f"__P2__ Sum of gear ratios: {sum(gear_ratios)}")

# Tell me how inefficecient my code is
print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))