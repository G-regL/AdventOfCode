import getopt
import sys
import time

# By default I want the real input, and *not* to debug.
ARG_data = "input.txt"
ARG_debugLogging = False

# Get the args off the command-line
opts, args = getopt.getopt(sys.argv[1:], "td", ["test", "debug"])
for opt, arg in opts:
    if opt in ("-t", "--test"):
        print(f"\33[31mUSING TEST DATA\33[0m")
        ARG_data = "test.txt"
    elif opt in ("-d", "--debug"):
        ARG_debugLogging = True


# Useful during testing to see what the hell is going on
def debug(thing):
    if ARG_debugLogging:
        print(f"\33[39mDEBUG:\33[0m {thing}")


answer_p1 = 0
answer_p2 = 0

# INPUT
import re

data = [re.findall(r"\S+", line) for line in open("input.txt").read().split("\n")]

sheet = []
for line in data[:-1]:
    sheet.append(list(map(int, line)))

sheet.append(data[-1])
sheet = list(zip(*sheet[::-1]))


# Do things!!
from math import prod

for line in sheet:
    if line[0] == "*":
        answer_p1 += prod(line[1:])
    elif line[0] == "+":
        answer_p1 += sum(line[1:])


# Print out the answers
print(f"\33[32m__P1__: \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__: \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print(
    f"\33[35mTook \33[1;35m{time.process_time_ns() / 1000000000}\33[0m\33[35m seconds to run\33[0m"
)
