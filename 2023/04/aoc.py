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

answer_p1 = 0
answer_p2 = 0

# read input data and split into list of lines
data = open(ARG_data).read().split('\n')


# loop through rows/columns
for card in data:
    card, numbers = card.split(":")
    card = card.strip().split("Card ")
    numbers_win, numbers_mine = [set(n.strip().split(' ')) for n in numbers.strip().split(' | ')]
    
    debug(f'{card}; winners({numbers_win}), mine({numbers_mine})')

    winners = numbers_win.intersection(numbers_mine)

    winners.discard('')

    debug(f'  matching numbers: {winners}; matches ({len(winners)})')
    points = 0
    if len(winners) - 1 > 1:
        points += math.pow(2, int(len(winners) - 1))
    elif len(winners) - 1 == 1:
        points += 2
    elif len(winners) == 1:
        points += 1

    answer_p1 += int(points)
    debug(f'  points: {int(points)}')


# Print out the answers
print(f"__P1__ Sum of winning cards: {answer_p1}")
#print(f"__P2__ Sum of gear ratios: {sum(gear_ratios)}")

# Tell me how inefficecient my code is
print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))