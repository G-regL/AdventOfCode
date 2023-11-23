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
#answer_p2 = 0

nice_vowels = ['a', 'e', 'i', 'o', 'u']
nice_doubles = ['aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh', 'ii', 'jj', 'kk', 'll', 'mm', 
                'nn', 'oo', 'pp', 'qq', 'rr', 'ss', 'tt', 'uu', 'vv', 'ww', 'xx', 'yy', 'zz']
naughty_sets = ['ab', 'cd', 'pq', 'xy']

for niceString in data.split('\n'):

    logger.debug(niceString)
    foundNiceVowel = 0
    foundNiceDouble = foundNaughtySet = False
    for naughty in naughty_sets:
        if niceString.count(naughty) >= 1:
            logger.debug("  Found Naughty set %s", naughty)
            foundNaughtySet = True

    if foundNaughtySet:
        continue
    
    for nice in nice_vowels:
        this_vowel_count = niceString.count(nice)
        if this_vowel_count >= 1:
            logger.debug("  Found Nice vowel %s", nice)
            foundNiceVowel += this_vowel_count
    
    for nice in nice_doubles:
        if niceString.count(nice) >= 1:
            logger.debug("  Found Nice double %s", nice)
            foundNiceDouble = True

    if foundNiceVowel >= 3 and foundNiceDouble:
        answer_p1 += 1


print(f"__P1__ Nice strings:", answer_p1)
    #print(f"__P2__ Number is:", answer_p2)

print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))