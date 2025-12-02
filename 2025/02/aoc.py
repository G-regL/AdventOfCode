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
productIDs = [r.split("-") for r in open('input.txt').read().split(',')]

# Do things!!
invalid = []
for start,end in productIDs:
    debug(f"Range {start}-{end}")
    for pid in range(int(start), int(end)+1):
        debug(f"  {pid}")
        pid = str(pid)
        if len(pid) % 2 != 0:
            continue
        half = int(len(pid) / 2)
        debug(f"    {half}")
        debug(f"    {pid[:half]} <> {pid[half:]}")
        if pid[:half] == pid[half:]:
            invalid.append(pid)
        

debug(invalid)
answer_p1 = sum(list(map(int,invalid)))

# Print out the answers
print(f"\33[32m__P1__: \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__: \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print(f"\33[35mTook \33[1;35m{time.process_time_ns() / 1000000000}\33[0m\33[35m seconds to run\33[0m")