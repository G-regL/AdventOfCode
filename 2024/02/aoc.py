import sys, getopt
import time

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
data = open(ARG_data).read().split('\n')


def safe(levels) -> bool:
    decreasing = [levels[i-1] > v for i,v in enumerate(levels[1:], 1)]
    increasing = [levels[i-1] < v for i,v in enumerate(levels[1:], 1)]
    gaps = [0 < abs(levels[i-1] - v) < 4 for i,v in enumerate(levels[1:], 1)]

    debug(f"{levels=}")
    if (all(decreasing) or all(increasing)) and all(gaps):
        return True
    else:
        return False

# loop through data
for report in data:
    levels = list(map(int, report.split()))
    if safe(levels):
        debug("Safe P1")
        answer_p1 += 1

    for r in range (len(report)):
        #create a new report, with a single level removed, and see if it's safe
        new_levels = levels[:r] + levels[r + 1 :]

        debug(f"{levels=}, {new_levels=}")
        if safe(new_levels):
            debug("Safe P2")
            answer_p2 += 1
            break

# Print out the answers
print(f"\33[32m__P1__ : \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__ : \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print("\33[35mTook \33[1;35m{}\33[0m\33[35m seconds to run\33[0m".format(time.process_time_ns() / 1000000000))