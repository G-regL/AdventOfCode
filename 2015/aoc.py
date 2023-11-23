import sys, getopt
import logging
import time

ARG_data = 'input.txt'
ARG_logLevel = 'INFO'

opts, args = getopt.getopt(sys.argv[1:],"htd",["help","test","debug"])
for opt, arg in opts:
    if opt == '-h':
        print ('aoc2015.py -t -d')
        sys.exit()
    elif opt in ("-t", "--test"):
        ARG_data = 'test.txt'
    elif opt in ("-d", "--debug"):
        ARG_logLevel = 'DEBUG'


# Define custom logger (inspired by https://stackoverflow.com/q/3220284/4483858)
logger = logging.getLogger("AoC_2015")
logger.setLevel(ARG_logLevel)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(ARG_logLevel)
# create formatter
formatter = logging.Formatter("%(name)s; %(message)s")
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
#without replace()



#with open(ARG_data) as f:
#    data = f.read()
