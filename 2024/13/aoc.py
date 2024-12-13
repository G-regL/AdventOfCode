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

#INPUT
import re
from math import gcd
machines_raw = open(ARG_data).read().split('\n\n')

machines = []
for mr in machines_raw:
    a, b, p = mr.split('\n')

    a = re.match(r'Button A: X\+(\d+), Y\+(\d+)', a).groups()
    b = re.match(r'Button B: X\+(\d+), Y\+(\d+)', b).groups()
    p = re.match(r'Prize: X=(\d+), Y=(\d+)', p).groups()
    m = {
        "a": tuple(map(int, a)),
        "b": tuple(map(int, b)),
        "p": tuple(map(int, p)),
    }
    m["p2"] = (m["p"][0] + 10000000000000, m["p"][1] + 10000000000000)

    machines.append(m)

for m in machines:
    ax = m["a"][0] * m["a"][1]
    ay = m["b"][0] * m["a"][1]
    ap = m["p"][0] * m["a"][1]
    ap2 = (m["p2"][0]) * m["a"][1]
    #print(ax, ay, ap)

    bx = m["a"][1] * m["a"][0]
    by = m["b"][1] * m["a"][0]
    bp = m["p"][1] * m["a"][0]
    bp2 = (m["p2"][1]) * m["a"][0]
    #print(bx,by, bp)

    #print(by - ay, bp - ap)

    a_presses = (bp - ap) / (by - ay)
    a2_presses = (bp2 - ap2) / (by - ay)

    #print(f"{a_presses=}, {a_presses.is_integer()=}")

    bx_a = m["b"][0] * a_presses
    bx_a2 = m["b"][0] * a2_presses
    #print(m["b"][0], bx_a, m["p"][0])
    b_presses = (m["p"][0] - bx_a) / m["a"][0]
    b2_presses = (m["p2"][0] - bx_a2) / m["a"][0]
    #print(f"{b_presses=}, {b_presses.is_integer()=}")

    if a_presses.is_integer() and b_presses.is_integer():
        answer_p1 += b_presses * 3 + a_presses

    if a2_presses.is_integer() and b2_presses.is_integer():
        answer_p2 += b2_presses * 3 + a2_presses


# Print out the answers
print(f"\33[32m__P1__: \33[1m{int(answer_p1)}\33[0m")
print(f"\33[32m__P2__: \33[1m{int(answer_p2)}\33[0m")

# Tell me how inefficecient my code is
print(f"\33[35mTook \33[1;35m{time.process_time_ns() / 1000000000}\33[0m\33[35m seconds to run\33[0m")