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

dataTestP2 = ['qjhvhtzxzqqjkmpb', 'xxyxx', 'uurcxstgmygtbstg', 'ieodomkazucvgmuy']

answer_p1 = 0
answer_p2 = 0

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
        logger.debug(f'  %s is NICE!', niceString)
        answer_p1 += 1

if ARG_data == 'test.txt':
    data = "\n".join(dataTestP2)

for niceString in data.split('\n'):

    logger.debug(niceString)
    

    pairs = [niceString[i:i+2] for i in range(0, len(niceString), 2)] + \
            [niceString[i:i+2] for i in range(1, len(niceString) -1, 2)]
    pairs = list(filter(lambda x: len(x) == 2, pairs))
    logger.debug(f"  {pairs}")

    repeats = [niceString[i:i+3] for i in range(0, len(niceString), 3)] + \
                [niceString[i:i+3] for i in range(1, len(niceString), 3)] + \
                [niceString[i:i+3] for i in range(2, len(niceString), 3)]
    repeats = list(filter(lambda x: len(x) == 3, repeats))
    logger.debug(f"  {repeats}")

    foundP2Pair = False
    foundP2Repeat = False
    for p in pairs:
        if len(p) == 2 and niceString.count(p) >= 2:
            logger.debug("  Found Nice pair %s", p)
            foundP2Pair = True
    
    for r in repeats:
        if len(r) == 3 and r[0] == r[2] and r[0] != r[1]:
            logger.debug("  Found Nice repeat %s", r)
            foundP2Repeat = True

    if foundP2Pair and foundP2Repeat:
        logger.debug(f'  %s is NICE!', niceString)
        answer_p2 += 1


print(f"__P1__ Nice strings:", answer_p1)
print(f"__P2__ Nice strings:", answer_p2)

print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))