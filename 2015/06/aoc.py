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
grid_P2 = [[0 for i in range(1000)] for j in range(1000)]

for line in data.split('\n'):
    parts = line.split(' ')
    if len(parts) == 5:
        _ , instruction, start, _, end = parts 
    else:
        instruction, start, _, end = parts 
    logger.debug(f"do %s, for box from %s - %s", instruction, start, end)

    start_x, start_y = list(map(lambda n: int(n), start.split(',')))
    end_x, end_y = list(map(lambda n: int(n), end.split(',')))

    for x in range(start_x, end_x+1):
        for y in range(start_y, end_y+1):
            if instruction == "on":
                grid[x][y] = 1
                grid_P2[x][y] += 1
            elif instruction == "off":
                grid[x][y] = 0
                if grid_P2[x][y] > 0:
                    grid_P2[x][y] -= 1
            else: #toggle
                grid[x][y] = 1 if grid[x][y] == 0 else 0
                grid_P2[x][y] += 2

#Count it all up
# I tried doing this inline above, but it didn't work. Not sure why.
for x in range(1000):
    for y in range(1000):
        if grid[x][y]:
            answer_p1 += 1
        answer_p2 += grid_P2[x][y]

print(f"__P1__ Lights on (count):", answer_p1)
print(f"__P2__ Total brightness:", answer_p2)

print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))