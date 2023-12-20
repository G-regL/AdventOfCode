import sys, getopt
import time

from collections import deque
import math
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


modules = {}
broadcast_dest = []
for m in data:
    name, _, dest = m.split(maxsplit=2)
    myname = name[1:]
    if name == "broadcaster":
        broadcast_dest = dest.replace(' ', '').split(',')
        myname = '_b'
        this = {'type': 'b', 'dest': broadcast_dest}
    elif name[0] == "%":
        this = {'type': name[0], 'dest': dest.replace(' ', '').split(','), 'state': 0}
    elif name[0] == "&":
        this = {'type': name[0], 'dest': dest.replace(' ', '').split(','), 'states': {}}

    modules[myname] = this

for m in [x for x in modules if modules[x]["type"] == '&']:
    #ic(modules[m])
    modules[m]["states"] = {y: 0 for y in modules if m in modules[y]["dest"]}

pulses_high = 0
pulses_low = 0

(feed,) = [name for name, module in modules.items() if "rx" in module["dest"]]

cycle_lengths = {}
seen = {name: 0 for name, module in modules.items() if feed in module["dest"]}
presses = 0

while answer_p2 == 0:
    presses += 1
    #debug(f'___button -low-> broadcaster')
    queue = deque([('broadcast', d, 0) for d in broadcast_dest])

    pulses_low += 1 + len(broadcast_dest)

    while queue:
        s, d, t = queue.popleft()

        if not d in modules:
            continue
    
        ## Defo stole this from Hyper-Neutrino, as I don't think I would have ever gotten there..
        if d == feed and t == 1:
            seen[s] += 1

            if s not in cycle_lengths:
                cycle_lengths[s] = presses
            #else:
            #    assert presses == seen[s] * cycle_lengths[s]


            if all(seen.values()):
                x = 1
                for cycle_length in cycle_lengths.values():
                    x = x * cycle_length // math.gcd(x, cycle_length)
                #print(x)
                answer_p2 = x

        #debug(f'___{s} {"-low->" if t == 0 else "-high->"} {d}')
        # Flip-flop, but only if the pulse is low
        if modules[d]['type'] == '%' and t == 0:
            # flip our state high -> low, low -> high
            modules[d]['state'] = 0 if modules[d]['state'] == 1 else 1
            #queue up a pulse to each of our destinations
            # pulse type is the same as our (new) state
            new = [(d, x, modules[d]['state']) for _, x in enumerate(modules[d]['dest'])]
            
            if modules[d]['state'] == 1:
                pulses_high += len(new)
            else:
                pulses_low += len(new)
            queue.extend(new)
            
        # conjunction
        elif modules[d]['type'] == '&':
            modules[d]['states'][s] = t
            if sum([foo for foo in modules[d]['states'].values()]) == len(modules[d]["states"]):
                # All input states are high, queue a low pulse to all our destinations
                new = [(d, x, 0) for x in modules[d]['dest']]
                pulses_low += len(new)
            else:
                new = [(d, x, 1) for x in modules[d]['dest']]
                pulses_high += len(new)
            queue.extend(new)
    
    # Capture the pulse product at presses == 1000 for Part 1
    if presses == 1000:
        answer_p1 = pulses_low * pulses_high


# Print out the answers
print(f"\33[32m__P1__ : \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__ : \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print("\33[35mTook \33[1;35m{}\33[0m\33[35m seconds to run\33[0m".format(time.process_time_ns() / 1000000000))