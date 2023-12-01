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
answer_p2 = 0
data = open(ARG_data).read()


for line in data.split('\n'):
    chars = [*line]   
    res = list(map(lambda n: int(n), [str(i) for i in chars if i.isdigit()]))
    if len(res) == 1:
        num = f"{res[0]}{res[0]}"
    else:
        num = f"{res[0]}{res[-1]}"

    debug(f"P1 line:{line}; res:{res}; num:{num}")

    answer_p1 += int(num)


if ARG_data == "test.txt":
    data = 'two1nine\neightwothree\nabcone2threexyz\nxtwone3four\n4nineeightseven2\nzoneight234\n7pqrstsixteen'
    # extra test cases pulled from input
    data += '\ndkvjxhxl8twoeightwog\nponeightnthnsmkrsixgqvmzoneninetwo7\n414dzfxfkqkf9onefourmdxh\nfnm3oneightsdn'

numbers = ['__', 'one','two','three','four','five','six','seven','eight','nine']
for line in data.split('\n'):

    debug(f"line:{line}")
    # first_pos = 100000
    # first = ""
    # last_pos = 0
    # last = ""

    # for n in numbers:
    #     pos = line.find(n)
    #     if pos != -1 and pos < first_pos:
    #         #debug(f"  found new first; {pos}, {n}")
    #         first_pos = pos
    #         first = n
    #     rpos = line.rfind(n)
    #     if rpos != -1 and rpos > last_pos:
    #         #debug(f"  found new last; {pos}, {n}")
    #         last_pos = rpos
    #         last = n
    
    # debug(f"  first_pos:{first_pos}; first:{first}; last_pos:{last_pos}; last:{last}; ")

    # if first:
    #     line = line[:first_pos] + str(numbers.index(first)) + line[first_pos + len(first):]
    #     debug(f"  new_line_first:{line}")

    # if last and (first_pos != last_pos or last_pos == 0):
    #     if first_pos + len(first) <= last_pos:
    #         debug(f"  default")
    #         line = line[:last_pos - len(first) + 1] + str(numbers.index(last)) + line[last_pos + len(last) - len(first) + 1:]
    #     else:
    #         debug(f"  ??")
    #         line = line[:last_pos - len(first) + 1] + str(numbers.index(last)) + line[last_pos + len(last) - len(first) + 1:]
    #     debug(f"  new_line_last :{line}")
    
    #ends with one
    line = line.replace('twone', '21')

    #ends with two
    line = line.replace('eightwo', '82')

    #ends with three
    line = line.replace('eighthree', '83')

    #ends with eight
    line = line.replace('oneight', '18')
    line = line.replace('threeight', '38')
    line = line.replace('fiveight', '58')
    line = line.replace('nineight', '89')
    
    line = line.replace('one', '1')
    line = line.replace('two', '2')
    line = line.replace('three', '3')
    line = line.replace('four', '4')
    line = line.replace('five', '5')
    line = line.replace('six', '6')
    line = line.replace('seven', '7')
    line = line.replace('eight', '8')
    line = line.replace('nine', '9')

    chars = [*line]   
    res = list(map(lambda n: int(n), [str(i) for i in chars if i.isdigit()]))
    if len(res) == 1:
        num = f"{res[0]}{res[0]}"
    else:
        num = f"{res[0]}{res[-1]}"

    debug(f"  line:{line}; res:{res}; num:{num}")

    answer_p2 += int(num)

    #answer_p2 += int(num)

print(f"__P1__ Sum of calibration values: {answer_p1}")
print(f"__P2__ Sum of calibration values: {answer_p2}")
#logger.info(line)

print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))