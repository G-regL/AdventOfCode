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
        print(f"\33[31mUSING TEST DATA\33[0m")
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
data = open(ARG_data).read().replace("\n","")


matches = re.findall(r'mul\([\d]{1,3},[\d]{1,3}\)|don\'t\(\)|do\(\)', data)
debug(matches)
    
enabled = True
for mul in matches:
    if mul == "don't()":
        enabled = False
    elif mul == "do()":
        enabled = True

    else:
        matches = re.match(r'mul\(([\d]{1,3}),([\d]{1,3})\)', mul)
        factor1, factor2 = list(map(int, matches.group(1,2)))
        answer_p1 += factor1 * factor2
        if enabled:
            answer_p2 += factor1 * factor2







# Print out the answers
print(f"\33[32m__P1__ : \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__ : \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print("\33[35mTook \33[1;35m{}\33[0m\33[35m seconds to run\33[0m".format(time.process_time_ns() / 1000000000))