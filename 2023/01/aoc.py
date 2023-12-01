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


# # Define custom logger (inspired by https://stackoverflow.com/q/3220284/4483858)
# logger = logging.getLogger("AoC")
# logger.setLevel(ARG_logLevel)
# # create console handler and set level to debug
# ch = logging.StreamHandler()
# ch.setLevel(ARG_logLevel)
# # create formatter
# formatter = logging.Formatter("%(message)s")
# # add formatter to ch
# ch.setFormatter(formatter)
# # add ch to logger
# logger.addHandler(ch)
# #without replace()

answer_p1 = 0
answer_p2 = None
data = open(ARG_data).read()


for line in data.split('\n'):
    chars = [*line]   
    res = list(map(lambda n: int(n), [str(i) for i in chars if i.isdigit()]))
    if len(res) == 1:
        num = f"{res[0]}{res[0]}"
    else:
        num = f"{res[0]}{res[-1]}"

    debug(f"line:{line}; res:{res}; num:{num}")

    answer_p1 += int(num)




print(f"__P1__ Sum of calibration values: {answer_p1}")
print(f"__P2__ We got to basement at step: {answer_p2}")
#logger.info(line)

print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))