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
# create formatter
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s; %(message)s")
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
#without replace()
 
data = open(ARG_data).read()

answer_p1 = 0
answer_p2 = 0
for line in data.split('\n'):

    grid = [[0 for i in range(5000)] for j in range(5000)]
    position = [0,0]
    multiple_presents = set()
    #Part 1
    for line_index, line_value in enumerate(line):
        if line_value == ">": # Right
            position = [position[0] + 1, position[1]]
        elif line_value == "<": # Left
            position = [position[0] - 1, position[1]]
        elif line_value == "^": # Up
            position = [position[0], position[1] + 1]
        elif line_value == "v": # Down
            position = [position[0], position[1] - 1]
        
        grid[position[0]][position[1]] += 1
        logger.debug(f"move %s, new pos: %d:%d, presents here: %d", line_value, position[0], position[1], grid[position[0]][position[1]])

        if grid[position[0]][position[1]] >= 1:
            logger.debug(f"More than one present, adding %d:%d to set", position[0], position[1])
            multiple_presents.add(str(position[0]) + ":" + str(position[1]))

    answer_p1 = len(multiple_presents)

    # dimensions = list(map(lambda n: int(n), line.split('x')))

    # logger.debug(f"present dimensions: l=%d; w=%d; h=%d", dimensions[0], dimensions[1], dimensions[2])
    # sides = [dimensions[0] * dimensions[1], dimensions[1] * dimensions[2], dimensions[2] * dimensions[0]]
    # logger.debug(f"present sides: lw=%d; wh=%d; hl=%d", sides[0], sides[1], sides[2])
    # present_paper = (2 * sides[0]) + (2 * sides[1]) + (2 * sides[2])
    
    # sides.sort()
    # present_slack = sides[0]

    # answer_p1 += present_paper + present_slack
    # logger.debug(f"Paper - %d square feet, plus %d slack = %d", present_paper, present_slack, (present_paper + present_slack))




    print(f"__P1__ Houses with at least one present:", answer_p1)
#print(f"__P2__ Total feet of ribbon:", answer_p2)

print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))