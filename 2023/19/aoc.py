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
raw_rules, raw_parts = open(ARG_data).read().split('\n\n')

parts = []
for part in raw_parts.split('\n'):
    this = {}
    for rating in part[1:-1].split(','):
        letter, value = rating.split("=")
        this[letter] = int(value)
    parts.append(this)

#debug(f'Parts\n{parts}')
rules = {}
# loop through data
for rule in raw_rules.split('\n'):
    this = []
    name, steps = rule[:-1].split('{')
    for step in steps.split(','):
        s = {"type": "", "op": "", "comp_l": "", "comp_r": 0, "dest": ""}
        if any(x in  step for x in ['<', '>']):
            s['type'] = "compare"
            s['op'] = step[1]
            s['comp_l'] = step[0]
            s['comp_r'] = int(step[2:step.index(':')])
            s['dest'] = step[step.index(':') + 1:]
        else:
            s['type'] = "move"
            s['dest'] = step
        this.append(s)
    rules[name] = this
#debug(f'Rules\n{rules}')

for p in parts:
    #debug(f'{p}')
    location = 'in'
    while location != "A" and location != 'R':       
        for r in rules[location]:
            #debug(f'  {r}')
            if r["type"] == "compare":
                #debug(f'    compare {p[r["comp_l"]]} {r["op"]} {r["comp_r"]} -> {r["dest"]}')
                if r['op'] == '>':
                    if p[r['comp_l']] > r['comp_r']:
                        location = r['dest']
                        break
                else:
                    if p[r['comp_l']] < r['comp_r']:
                        location = r['dest']
                        break
            else:
                #debug(f'    move -> {r["dest"]}')
                location = r['dest']

            #debug(f'  loc {location}')

        if location == 'A':
            answer_p1 += sum(p.values())
        

# Print out the answers
print(f"\33[32m__P1__ : \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__ : \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print("\33[35mTook \33[1;35m{}\33[0m\33[35m seconds to run\33[0m".format(time.process_time_ns() / 1000000000))