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
rules_raw, updates_raw = open('input.txt').read().split('\n\n')

rules = {}
for rule in rules_raw.split("\n"):
    first, second = list(map(int, rule.split("|")))
    if first in rules:
        rules[first].append(second)
    else:
        rules[first] = [second]
debug(rules)

updates = []
for update in updates_raw.split("\n"):
    updates.append(list(map(int,update.split(","))))
debug(updates)

# Part 1
safe = set()
unsafe = set()
for update in updates:
    debug(f"{update=}")
    is_unsafe = False
    for i,page in enumerate(update[:-1]):
        page_next = update[i + 1]

        if page in rules:
            debug(f"{page=}, {page_next=}, {rules[page]=}")
            if page_next not in rules[page]:
                is_unsafe = True
                debug("UNSAFE")
        else:
            if page in rules[page_next]:
                is_unsafe = True
                debug("UNSAFE")
    
    if not is_unsafe:
        safe.add(tuple(update))
    else:
        unsafe.add(tuple(update))
    debug("")

debug(f"{safe=}")
debug(f"{unsafe=}")

for item in safe:
    temp = list(item)
    answer_p1 += temp[int((len(temp) - 1)/2)]



# Print out the answers
print(f"\33[32m__P1__: \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__: \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print(f"\33[35mTook \33[1;35m{time.process_time_ns() / 1000000000}\33[0m\33[35m seconds to run\33[0m")