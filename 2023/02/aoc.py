import sys, getopt
#import logging
import time

ARG_data = 'input.txt'
ARG_logLevel = False

opts, args = getopt.getopt(sys.argv[1:],"td",["test","debug"])
for opt, arg in opts:
    if opt == '-h':
        print ('aoc.py -t -d')
        sys.exit()
    elif opt in ("-t", "--test"):
        ARG_data = 'test.txt'
    elif opt in ("-d", "--debug"):
        ARG_logLevel = True

def debug(thing):
    if ARG_logLevel:
        print(f"DEBUG:{thing}")

answer_p1 = 0
answer_p2 = 0
data = open(ARG_data).read().split('\n')


for line in data:
   


print(f"__P1__ Sum of calibration values: {answer_p1}")
print(f"__P2__ Sum of calibration values: {answer_p2}")
#logger.info(line)

print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))