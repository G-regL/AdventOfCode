import sys, getopt
import time

from collections import Counter

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

def get_hand_type(counts):
    # 5 of a kind
    if counts[0] == 5:
        t = '5oak'
    # 4 of a kind
    elif counts[0] == 4:
        t = '4oak'
    # Full House
    elif counts[0] == 3 and counts[1] == 2:
        t = 'fh'
    # 3 of a kind
    elif counts[0] == 3:
        t = '3oak'
    # Two pair
    elif counts[0] == 2 and counts[1] == 2:
        t = '2p'
    # one pair
    elif counts[0] == 2 and counts[1] == 1:
        t = '1p'
    else:
        t = 'hc'
    return t

answer_p1 = 0
answer_p2 = 0

# read input data and split into list of lines
data = open(ARG_data).read().split('\n')

hands = hands_p2 = {'hc': [], '1p': [], '2p': [], '3oak': [], 'fh': [], '4oak': [], '5oak': []}

# loop through data
for line in data:

    cards, bid = line.split(' ')
    debug(f' cards({cards}), bid({bid})')
    counts = list(Counter(cards).values())
    counts.sort(reverse=True)

    #Part 1
    t = get_hand_type(counts)
    hands[t].append((cards, int(bid), t))


    #Part 2
    jays = cards.count('J')
    counts_p2 = sorted([cards.count(card) for card in set(cards) if card != "J"], reverse=True)
    # If there are jokers, add their count to the count of the most common card
    if jays == 5:
        counts_p2.append(5)
    elif jays > 0:
        counts_p2[0] += jays
    t_p2 = get_hand_type(counts_p2)
    hands_p2[t_p2].append((cards, int(bid), t_p2))

    
#Part 1
final_list = []
for hand_type in list(hands.keys()):
    hands[hand_type].sort(key=lambda h: h[0].translate(str.maketrans('AKQJT', 'EDCBA')))
    final_list += hands[hand_type]

for i, h in enumerate(final_list):
    debug(f'Hand: {h[0]}; Bid: {h[1]}; Rank: {i + 1}; winnings: {(i + 1) * h[1]}; type: {h[2]}')
    answer_p1 += (i + 1) * h[1]
    

# Part 2
final_list_p2 = []
for hand_type in list(hands_p2.keys()):
    hands_p2[hand_type].sort(key=lambda h: h[0].translate(str.maketrans('AKQJT', 'EDC0A')))
    final_list_p2 += hands_p2[hand_type]

for i, h in enumerate(final_list_p2):
    debug(f'Hand: {h[0]}; Bid: {h[1]}; Rank: {i + 1}; winnings: {(i + 1) * h[1]}; type: {h[2]}')
    answer_p2 += (i + 1) * h[1]


# Print out the answers
print(f"__P1__ Total Winnings: {answer_p1}")
print(f"__P2__ Total Winnings with Jokers: {answer_p2}")

# Tell me how inefficecient my code is
print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))