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
#formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s; %(message)s")
formatter = logging.Formatter("%(message)s")
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

    grid_p2 = [[0 for i in range(5000)] for j in range(5000)]
    position_p2 = {"santa": [0,0], "robo": [0,0]}
    multiple_presents_p2 = set()

    grid[0][0] = 1
    grid_p2[0][0] = 1
    multiple_presents.add("0:0")
    multiple_presents_p2.add("0:0")

    #Part 1
    for line_index, line_value in enumerate(line):
        who = ("santa" if line_index % 2 != 1 else "robo")
        myposition = position_p2[who]
        #print("santa" if who != 1 else "robo")
        if line_value == ">": # Right
            position = [position[0] + 1, position[1]]
            myposition = [myposition[0] + 1, myposition[1]]

        elif line_value == "<": # Left
            position = [position[0] - 1, position[1]]
            myposition = [myposition[0] - 1, myposition[1]]

        elif line_value == "^": # Up
            position = [position[0], position[1] + 1]
            myposition = [myposition[0], myposition[1] + 1]

        elif line_value == "v": # Down
            position = [position[0], position[1] - 1]
            myposition = [myposition[0], myposition[1] - 1]
        


        grid[position[0]][position[1]] += 1
        logger.debug(f"p1 - move %s, new pos: %d:%d, presents here: %d", 
                        line_value, position[0], position[1], grid[position[0]][position[1]])

        if grid[position[0]][position[1]] >= 1:
            logger.debug(f"p1 - At least one present, adding %d:%d to set", position[0], position[1])
            multiple_presents.add(str(position[0]) + ":" + str(position[1]))



        grid_p2[myposition[0]][myposition[1]] += 1
        logger.debug(f"p2 - move %s, new %s pos: %d:%d, presents here: %d",
                        line_value, who, myposition[0], myposition[1], grid_p2[myposition[0]][myposition[1]])
        if grid_p2[myposition[0]][myposition[1]] >= 1:
            logger.debug(f"p2 - At least one present, adding %d:%d to p2 set", myposition[0], myposition[1])
            multiple_presents_p2.add(str(myposition[0]) + ":" + str(myposition[1]))
        position_p2[who] = myposition


    answer_p1 = len(multiple_presents)
    answer_p2 = len(multiple_presents_p2)

    print(f"__P1__ Houses with at least one present:", answer_p1)
    print(f"__P2__ Houses with at least one present:", answer_p2)

print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))