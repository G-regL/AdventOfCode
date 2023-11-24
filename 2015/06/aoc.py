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

grid = [[0 for i in range(1000)] for j in range(1000)]
lightsOn = 0

for line in data.split('\n'):
    parts = line.split(' ')
    if len(parts) == 5:
        _ , instruction, start, _, end = parts 
    else:
        instruction, start, _, end = parts 
    logger.debug(f"do %s, for box from %s - %s", instruction, start, end)

    start_x, start_y = list(map(lambda n: int(n), start.split(',')))
    end_x, end_y = list(map(lambda n: int(n), end.split(',')))
    pre = lightsOn
    for x in range(start_x, end_x+1):
        for y in range(start_y, end_y+1):
            if instruction == "on":
                #logger.debug(f"Turned on light at {x}:{y}")
                grid[x][y] = 1
                lightsOn += 1
            elif instruction == "off":
                #logger.debug(f"Turned off light at {x}:{y}")
                grid[x][y] = 0
                lightsOn -= 1
            else:
                if grid[x][y] == 0:
                    #logger.debug(f"Toggled on light at {x}:{y}")
                    grid[x][y] = 1
                    lightsOn += 1
                else:
                    #logger.debug(f"Toggled off light at {x}:{y}")
                    grid[x][y] = 0
                    lightsOn -= 1

    if lightsOn < 0:
        lightsOn = 0

    logger.debug(f"  changed %d lights", abs(pre - lightsOn))
    logger.debug(f"  Lights on: %d", lightsOn)
    #input("  Press Enter to continue...")


for x in range(1000):
    for y in range(1000):
        if grid[x][y]:
            answer_p1 += 1

print(f"__P1__ Lights on (loop):", lightsOn)
print(f"__P1__ Lights on (count):", answer_p1)
#print(f"__P2__ Nice strings:", answer_p2)

print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))