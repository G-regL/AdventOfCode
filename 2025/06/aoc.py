import getopt
import re
import sys
import time
from math import prod

# By default I want the real input, and *not* to debug.
ARG_data = "input.txt"
ARG_debugLogging = False

# Get the args off the command-line
opts, args = getopt.getopt(sys.argv[1:], "td", ["test", "debug"])
for opt, arg in opts:
    if opt in ("-t", "--test"):
        print(f"\33[31mUSING TEST DATA\33[0m")
        ARG_data = "test.txt"
    elif opt in ("-d", "--debug"):
        ARG_debugLogging = True


# Useful during testing to see what the hell is going on
def debug(thing):
    if ARG_debugLogging:
        print(f"\33[39mDEBUG:\33[0m {thing}")


answer_p1 = 0
answer_p2 = 0

# INPUT

data_raw = open(ARG_data).read().split("\n")
data_p1 = [re.findall(r"\S+", line) for line in data_raw]

sheet_p1 = []
for line in data_p1[:-1]:
    sheet_p1.append(list(map(int, line)))

sheet_p1.append(data_p1[-1])
sheet_p1 = list(zip(*sheet_p1[::-1]))

# Part 2 parsing..
# This was a pain, but it works..
lines = open(ARG_data).read().split("\n")
# ['123 328  51 64 ', ' 45 64  387 23 ', '  6 98  215 314', '*   +   *   +  ']
# Find column widths by regexing the operation line
col_widths = [len(col) - 1 for col in re.findall(r"([\+\*] +)", lines[-1])]
# Increment the last width by 1
col_widths[-1] += 1

# Loop through the lines, pulling the right "columns" into a new array of numbers
data_p2 = []
for line in lines:
    col = 0
    row = []
    for i in col_widths:
        number = line[col : col + i]
        row.append(number)
        col += i + 1
    data_p2.append(row)

# spin the sheet
data_p2 = list(zip(*data_p2[::-1]))
# It now looks like this
# [('*  ', '  6', ' 45', '123'),
#  ('+  ', '98 ', '64 ', '328'),
#  ('*  ', '215', '387', ' 51'),
#  ('+  ', '314', '23 ', '64 ')]

sheet_p2 = []
# Loop through the data (again), this time generating new numbers from the colmns
for line in data_p2:
    # Add the op to the front
    numbers = [line[0].strip()]
    # Go through each horizontal number, and build the new vertical number
    for idx in range(len(line[0])):
        # pull the idx-th char out of each line item, reverse the order, and append it
        n = [char[idx] for char in line[1:]]
        n.reverse()
        numbers.append(int("".join(n)))
    # Append the new numbers to the sheet
    sheet_p2.append(numbers)
# It looks like this now
# [['*', 1, 24, 356],
#  ['+', 369, 248, 8],
#  ['*', 32, 581, 175],
#  ['+', 623, 431, 4]]

# Do things!!
for line in sheet_p1:
    if line[0] == "*":
        answer_p1 += prod(line[1:])
    elif line[0] == "+":
        answer_p1 += sum(line[1:])

# There's probably a better way to do both P1 and P2 in a single loop, but... this is fine.
for line in sheet_p2:
    if line[0] == "*":
        answer_p2 += prod(line[1:])
    elif line[0] == "+":
        answer_p2 += sum(line[1:])


# Print out the answers
print(f"\33[32m__P1__: \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__: \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print(
    f"\33[35mTook \33[1;35m{time.process_time_ns() / 1000000000}\33[0m\33[35m seconds to run\33[0m"
)
