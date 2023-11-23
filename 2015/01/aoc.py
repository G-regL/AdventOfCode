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
formatter = logging.Formatter("%(message)s")
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
#without replace()
 
with open(ARG_data) as f:
    data = f.read()


for line in data.split('\n'):
    answer_p1 = None
    answer_p2 = None


    #Part 1
    ups = line.count("(")
    downs = line.count(")")
    logger.debug(f"count of chars: up=%d; down=%d", ups, downs)
    answer_p1 = ups - downs

    #Part 2
    floor = 0
    for i, v in enumerate(line):
        #logger.debug(f"movement: %s", v)
        if v == "(":
            floor += 1
        if v == ")":
            floor -= 1
            
        logger.debug(f"movement: %s, floor: %d", v, floor)
        
        if floor < 0:
            logger.debug("Found basement!")
            logger.debug(f"We got to basement at step: %d", i+1)

            answer_p2 = i+1
            break


    print(f"__P1__ End up on floor: {answer_p1}")
    print(f"__P2__ We got to basement at step: {answer_p2}")
    #logger.info(line)

print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))