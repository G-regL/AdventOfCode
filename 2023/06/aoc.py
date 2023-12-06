import sys, getopt
import time

import math

# By default I want the real input, and *not* to debug.
races_p1 = [  
    {"t": 44, "d": 202},
    {"t": 82, "d": 1076},
    {"t": 69, "d": 1138},
    {"t": 81, "d": 1458}
]
race_p2 = {"t": 44826981, "d": 202107611381458}
ARG_debugLogging = False

# Get the args off the command-line
opts, args = getopt.getopt(sys.argv[1:],"td",["test","debug"])
for opt, arg in opts:
    if opt in ("-t", "--test"):
        races_p1 = [  
            {"t": 7, "d": 9},
            {"t": 15, "d": 40},
            {"t": 30, "d": 200}
        ]
        race_p2 = {"t": 71530, "d": 940200}
    elif opt in ("-d", "--debug"):
        ARG_debugLogging = True

# Useful during testing to see what the hell is going on
def debug(thing):
    if ARG_debugLogging:
        print(f"DEBUG: {thing}")

answer_p2 = 0

# read input data and split into list of lines
#data = open(ARG_data).read().split('\n')

distances_p1 = []

# loop through data
for r in races_p1:
    race_distances = []
    debug(f"race: {r}")
    for ms in range(1, r['t'] - 1):
        debug(f'  ms {ms}') 
        race_distance = (r['t'] - ms) * ms
        
        if race_distance > r['d']:
            debug(f'    adding race_distance {race_distance}')
            race_distances.append(race_distance)
    debug(f'    furthest distance {max(race_distances)}')

    distances_p1.append(len(race_distances))
debug(f"distances: {distances_p1}")

# # This works, but is very slow
# race_distances_p2 = []
# for ms in range(1, race_p2['t'] - 1):
#     race_distance = (race_p2['t'] - ms) * ms
#     if race_distance > race_p2['d']:
#         debug(f'    adding race_distance {race_distance}')
#         race_distances_p2.append(race_distance)
# answer_p2 = len(race_distances_p2)

# # This is better, I think because I'm not appending the full distance for each ms, just whether it's longer than the record
# race_distances_p2 = []
# for ms in range(1, race_p2['t'] - 1):
#     #race_distance = 
#     if (race_p2['t'] - ms) * ms > race_p2['d']:
#         race_distances_p2.append(True)
# answer_p2 = sum(race_distances_p2)

# This is *much* faster. I think because we're not storing all values, just their true/false
answer_p2 = sum([b*(race_p2['t']-b) > race_p2['d'] for b in range(race_p2['t'])])


# Print out the answers
print(f"__P1__ Product of possible record distances: {math.prod(distances_p1)}")
print(f"__P2__ Number of ways to beat record: {answer_p2}")

# Tell me how inefficecient my code is
print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))