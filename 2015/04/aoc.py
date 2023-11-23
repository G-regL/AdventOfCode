import sys, getopt
import logging
import time

import hashlib


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


for secretKey in data.split('\n'):

    answer_p1 = 0
    answer_p2 = 0

    counter = 0
    while answer_p1 == 0 or answer_p2 == 0:

        hash = hashlib.md5((secretKey + str(counter)).encode()).hexdigest()

        #print(hash)
        if answer_p1 == 0 and hash[:5].count("0") == 5:
            logger.debug(f"found p1: %d, %s", counter, hash)
            answer_p1 = counter
        
        if answer_p2 == 0 and hash[:6].count("0") == 6:
            logger.debug(f"found p2: %d, %s", counter, hash)
            answer_p2 = counter

        counter += 1

    print(f"__P1__ Number is:", answer_p1)
    print(f"__P2__ Number is:", answer_p2)

print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))