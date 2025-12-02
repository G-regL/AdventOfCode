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

moves = [[l[0],int(l[1:]) % 100, int(l[1:])] for l in open(ARG_data).read().split('\n')]

dial_position = 50

for m in moves:
    dial_position_old = dial_position
    debug(f"- {m}")
    debug(f"  start dial {dial_position:3}")
    if m[0] == "R":
        dial_position = dial_position + m[1]
    else:
        dial_position = dial_position - m[1]

    dial_position = dial_position % 100
    
    if dial_position != 0 and dial_position_old != 0:
        if m[0] == "R" and dial_position_old + m[1] > 99:
            debug(f"  Crossed 0 ↷ {dial_position_old + m[1]}")
            answer_p2 += 1
        elif m[0] == "L" and dial_position_old - m[1] < 0:
            debug(f"  Crossed 0 ↶ {dial_position_old - m[1]}")
            answer_p2 += 1

    
    if dial_position == 0:
        debug(f"  dial at 0, incrementing")
        answer_p1 += 1
        answer_p2 += 1

    if m[2] > 100:
        rotations = int(m[2] / 100)
        debug(f"  add rotations, {rotations}")
        answer_p2 += rotations 


# Print out the answers
print(f"\33[32m__P1__: \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__: \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print(f"\33[35mTook \33[1;35m{time.process_time_ns() / 1000000000}\33[0m\33[35m seconds to run\33[0m")