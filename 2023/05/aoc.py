import sys, getopt
import time
import pprint

# By default I want the real input, and *not* to debug.
ARG_data = 'input.txt'
ARG_debugLogging = False

# Get the args off the command-line
for opt, arg in getopt.getopt(sys.argv[1:],"td",["test","debug"])[0]:
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
data = open(ARG_data).read().split('\n\n')

#Pull the first line, split at the colon, take the numbers and split them, casting to a list of ints
seeds = [int(s) for s in data[0].split(':')[1].split()]
#debug(f'seeds: {seeds}')

blocks = {}

# loop through data
for block in data[1:]:
    lines = block.split("\n")
    
    blocks[lines[0].split(' ')[0]] = []
    for l in lines[1:]:
        blocks[lines[0].split(' ')[0]].append([int(v) for v in l.split()])


location_min = 10000000000000000000
for s in seeds:
    debug(f'Seed:{s}')
    seed_position = s
    for b in blocks.keys():
        block_pos = seed_position
        debug(f'  {b}')
        for m in blocks[b]:
            if m[1] <= block_pos < m[1] + m[2]:#      m[1] <= seed_position and m[1] + m[2] - 1 >= seed_position:
                seed_position = m[0] + (seed_position - m[1])   
                debug(f'      new pos {seed_position}')
                break
            debug(f'    location: {seed_position}; {m}')


    if seed_position < location_min:
        location_min = seed_position

    debug(f'  Final location:{seed_position}')
    debug(f'  best location:{location_min}')


# Print out the answers
print(f"__P1__ : {location_min}")
print(f"__P2__ : {answer_p1}")

# Tell me how inefficecient my code is
print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))