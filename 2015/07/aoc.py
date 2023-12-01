import sys, getopt
import logging
import time

ARG_data = 'input.txt'
ARG_logLevel = 'INFO'

opts, args = getopt.getopt(sys.argv[1:],"td",["test","debug"])
for opt, arg in opts:
    if opt == '-h':
        print ('test.py -i <inputfile> -o <outputfile>')
        sys.exit()
    elif opt in ("-t", "--test"):
        ARG_data = 'test.txt'
    elif opt in ("-d", "--debug"):
        ARG_logLevel = 'DEBUG'


# Define custom logger (inspired by https://stackoverflow.com/q/3220284/4483858)
logger = logging.getLogger("AoC")
logger.setLevel(ARG_logLevel)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(ARG_logLevel)
# add formatter to ch
ch.setFormatter(logging.Formatter("%(message)s"))
# add ch to logger
logger.addHandler(ch)

data = open(ARG_data).read()

answer_p1 = 0
answer_p2 = 0

class op():
    def __init__(self, text) -> None:
        self.f1 = self.f2 = self.type = self.dest = None
        if any(x in text for x in ['LSHIFT', 'RSHIFT', 'OR', 'AND']):
            self.f1, self.type, self.f2, _, self.dest = text.split(' ')
        elif "NOT" in text:
            self.type, self.f1, _, self.dest = text.split(' ')
        else:
            self.f1, _, self.dest = text.split(' ')
            self.type = "ASSIGN"
        pass

    def __str__(self) -> str:
        if self.type == "ASSIGN":
            return f"{self.type}; {self.f1} -> {self.dest}"
        elif self.type == "NOT":
            return f"{self.type}; {self.f1} -> {self.dest}"
        else:
            return f"{self.type}; {self.f1}, {self.f2} -> {self.dest}"

operations = []
wires = dict()

for line in data.split('\n'):
    thisop = op(line)
    operations.append(thisop)
    if thisop.f1 and thisop.f1.isalpha():
        wires[thisop.f1] = 0x0000
    if thisop.f2 and thisop.f2.isalpha():
        wires[thisop.f2] = 0x0000
    if thisop.dest and thisop.dest.isalpha():
        wires[thisop.dest] = 0x0000


cycles = 0
while cycles < 500:
    cycles += 1
    for o in operations:
        #logger.debug(o)
        if o.type == "ASSIGN" and o.f1.isnumeric():
            wires[o.dest] = int(o.f1)
            operations.remove(o)
        
        if o.type == "AND":
            if o.f1.isnumeric() and (o.f2.isalpha() and wires[o.f2]):
                wires[o.dest] = int(o.f1) & wires[o.f2]
                operations.remove(o)
            elif (o.f1.isalpha() and wires[o.f1]) and (o.f2.isalpha() and wires[o.f2]):
                wires[o.dest] = wires[o.f1] & wires[o.f2]
                operations.remove(o)
        
        if o.type == "OR":
            if wires[o.f1] and wires[o.f2]:
                wires[o.dest] = wires[o.f1] | wires[o.f2]
                operations.remove(o)
        
        if o.type == "LSHIFT":
            if wires[o.f1]:
                wires[o.dest] = wires[o.f1] << int(o.f2)
                operations.remove(o)

        if o.type == "RSHIFT":
            if wires[o.f1]:
                wires[o.dest] = wires[o.f1] >> int(o.f2)
                operations.remove(o)

        if o.type == "NOT":
            if wires[o.f1]:
                wires[o.dest] = ~ wires[o.f1]
                operations.remove(o)

        wires[o.dest] = wires[o.dest] & 0xffff

    logger.debug(len(operations))
    #logger.debug(wires)
    logger.debug(len([e for i, e in enumerate(wires) if wires[e] == 0]))

print(f"__P1__ Signal on a:", answer_p1)
#print(f"__P2__ Total brightness:", answer_p2)

print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))