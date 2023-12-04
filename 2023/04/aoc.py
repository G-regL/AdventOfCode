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

# Pre-populate the card_counts as 1, because we *know* we have at least one of each
# Also helps down inthe Part 2 card count loop to ensure we're not adding cards out of range.
#card_counts = {c: 1 for c in range(1,len(data) + 1)}
card_counts = {}
for c in range(1,len(data) + 1):
    card_counts[c] = 1

# loop through cards
for card in data:
    # Get card number, winning numbers, and my numbers
    card, numbers = card.split(":")
    card = int(card.strip().split(' ')[-1])
    numbers_win, numbers_mine = [set(n.strip().split(' ')) for n in numbers.strip().split(' | ')]
    
    debug(f'{card} - winners({numbers_win}), mine({numbers_mine})')

    # Find my winning numbers
    winners = numbers_win.intersection(numbers_mine)

    # Because I'm splitting on spaces, and the numbers are column aligned, 
    # there's sometimes an extra '' element in the set, so this removes it
    winners.discard('')

    #debug(f'    matching numbers:{winners}; matches({len(winners)}); copies({card_counts[card]})')
    points = 0
    
    # Calculate points for this card
    if len(winners) - 1 >= 1:
        points += math.pow(2, int(len(winners) - 1))
    elif len(winners) == 1:
        points += 1

    answer_p1 += int(points)
    #debug(f'    points: {int(points)}')

    # Part 2 card count
    # We only add card copies if we have winners
    if len(winners) > 0:

        ## This block works just fine, but is *REALLY* slow. like 10* slower than what's below
        ## Thanks Ryne for making me feel inferior.
        # # Loop over each copy of this card
        # for _ in range(0,card_counts[card]):
        #     # For each winner we have, add a copy to the next cards, but only if they're in range
        #     for next in range(0, len(winners)+1):
        #         if next in card_counts.keys():
        #             #debug(f'    adding {1} to card {card + next}')
        #             card_counts[card + next] += 1
        
        # Loop over each copy of this card
        # For each winner we have, add a copy to the next cards, but only if they're in range
        for next in range(0, len(winners)+1):
            if next in card_counts.keys():
                #debug(f'    adding {1} to card {card + next}')
                card_counts[card + next] += card_counts[card]
                #answer_p2 += card_counts[card]
    
    debug(f'    card counts: {card_counts}')


debug(f'Final card counts: {card_counts}')

# Print out the answers
print(f"__P1__ Sum of winning cards: {answer_p1}")
print(f"__P2__ Total number of scratchcards: {sum(card_counts.values())}")

# Tell me how inefficecient my code is
print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))