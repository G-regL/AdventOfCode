import sys, getopt
import time
import re

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
steps = open(ARG_data).read().split(',')

def calculate_value(thing):
    value = 0
    for c in thing:
        value = ((value + ord(c)) * 17 ) % 256
    return value

boxes = [[] for _ in range(256)]

# loop through data
for step in steps:
    #Part 1
    v = calculate_value(step)
    answer_p1 += v
    debug(f"value after {step} - {v}")

    #Part 2
    label, focal_length = re.split("=|-", step)
    box = calculate_value(label)
    debug(f"box for {label} - {box}")
    if "=" in step:
        updated = False
        for i,(lens_label, _) in enumerate(boxes[box]):
            if label == lens_label:
                debug(f'  Found label({label}) at index({i}) in box({box})')
                boxes[box][i] = (label, focal_length)
                updated = True
        
        if not updated:
            debug(f'  no label({label}) at in box({box}), appending {(label, focal_length)}')
            boxes[box].append((label, focal_length))

    elif '-' in step:
        for i,(lens_label, _) in enumerate(boxes[box]):
            if label == lens_label:
                debug(f'  deleting label({label}) in box({box})')
                del boxes[box][i]

for box_index, box in enumerate(boxes, start=1):
    for lens_index, lens in enumerate(box, start=1):
        debug(f' box_index({box_index})')
        answer_p2 += box_index * lens_index * int(lens[1])

# Print out the answers
print(f"\33[32m__P1__ : \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__ : \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print("\33[35mTook \33[1;35m{}\33[0m\33[35m seconds to run\33[0m".format(time.process_time_ns() / 1000000000))