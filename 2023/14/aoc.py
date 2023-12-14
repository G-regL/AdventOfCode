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
        print(f"\33[39mDEBUG:\33[0m {thing}")

answer_p1 = 0
answer_p2 = 0

# read input data and split into list of lines
data = open(ARG_data).read().split('\n')

# Rotate the gride CW because it'll be easier to deal with it on a per-line basis, versus having to run down each column.
grid = list(zip(*data))


# loop through "columns"
for c in grid:
    sections = "".join(c).split("#")
    # We don't care about anything after the first squre block, so we can just split the column at the first one, and take the part before it
    for si, s in enumerate(sections):
        s = [*s]
        #debug(f'  section pre  {s}')
        for i, char in enumerate(s):
            if char == "O":
                continue
            # Let's get down to the real work here.
            if char == ".":
                if s[i:].count("O"):
                    next_round = s.index("O", i)
                    s[next_round] = '.'
                    s[i] = "O"
        sections[si] = "".join(s)

    tilted_line = "#".join(sections)
    line_length = len(tilted_line)
    for i, char in enumerate(tilted_line):
        if char == "O":
            answer_p1 += line_length - i


# Print out the answers
print(f"\33[32m__P1__ : \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__ : \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print("\33[35mTook \33[1;35m{}\33[0m\33[35m seconds to run\33[0m".format(time.process_time_ns() / 1000000000))