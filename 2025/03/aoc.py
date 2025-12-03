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
banks = open('input.txt').read().split('\n')

# Do things!!
for bank in banks:
    jolts = "0"
    for b in range(0, len(bank) -1):
        if bank[b]> jolts:
            jolts = bank[b]
    #print(jolts)

    jolts += "0"
    for b in range(bank.find(jolts[0]) + 1, len(bank)):
        if bank[b] > jolts[1]:
            jolts = jolts[0] + bank[b]

    #print(jolts)
    answer_p1 += int(jolts)

# Print out the answers
print(f"\33[32m__P1__: \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__: \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print(f"\33[35mTook \33[1;35m{time.process_time_ns() / 1000000000}\33[0m\33[35m seconds to run\33[0m")