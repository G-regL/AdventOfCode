import sys, getopt
import logging
import math

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
 
with open(ARG_data) as f:
    data = f.read()

answer_p1 = 0
#answer_p2 = None
for line in data.split('\n'):



    #Part 1
    dimensions = line.split('x')
    logger.debug(f"present dimensions: l=%d; w=%d; h=%d", int(dimensions[0]), int(dimensions[1]), int(dimensions[2]))
    sides = [int(dimensions[0]) * int(dimensions[1]), int(dimensions[1]) * int(dimensions[2]), int(dimensions[2]) * int(dimensions[0])]
    logger.debug(f"present sides: lw=%d; wh=%d; hl=%d", sides[0], sides[1], sides[2])
    present_paper = (2 * sides[0]) + (2 * sides[1]) + (2 * sides[2])
    
    sides.sort()
    present_slack = sides[0]

    answer_p1 += present_paper + present_slack
    logger.debug(f"this present needs %d square feet, plus %d slack = %d", present_paper, present_slack, (present_paper + present_slack))



print(f"__P1__ Total square feet:", answer_p1)
#print(f"__P2__ We got to basement at step:", answer_p2)
#logger.info(line)