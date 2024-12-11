import sys, getopt
import time

# By default I want the real input, and *not* to debug.
ARG_data = 'input.txt'
ARG_debugLogging = False

# Get the args off the command-line
opts, args = getopt.getopt(sys.argv[1:],"td",["test","debug"])
for opt, arg in opts:
    if opt in ("-t", "--test"):
        print(f"\33[31mUSING TEST DATA\33[0m")
        ARG_data = 'test.txt'
    elif opt in ("-d", "--debug"):
        ARG_debugLogging = True

# Useful during testing to see what the hell is going on
def debug(thing):
    if ARG_debugLogging:
        print(f"\33[39mDEBUG:\33[0m {thing}")

answer_p1 = 0
answer_p2 = 0

#INPUT
# #Generate single list of lines
# data = open(ARG_data).read().split('\n')

# #Generate a 2d matrix for a grid, including 
# #In/out of range checks are done with in_grid(row, column)
# grid = [list(map(int, list(row))) for row in data]
# limits = (len(grid[0]), len(grid))
# def in_grid(row, col) -> bool:
#     global limits
#     return 0 <= row < limits[0] and 0 <= col < limits[1]

# #Same, but using a dictionary, with keys being (row, column) tuples
# #Makes in/out of range checks dead simple, using grid.get((r,c))
# #    None if it doesn't exist, value otherwise
# grid = {(r,c): int(char) for r, row in enumerate(data) for c, char in enumerate(row)}


# Do things!!
stones = list(map(int, open(ARG_data).read().split(' ')))


#This was the original Part 1 solution
# It works perfectly, but is a bit slow.
# Doesn't scale beyond about 40 blinks (and even that takes over 45 seconds)
# for blink in range(25):
#     new_stones = []
#     #print(stones)
#     for stone in stones:
#         if stone == 0:
#             new_stones.append(1)
#         elif len(str(stone)) % 2 == 0:
#             ss = str(stone)
#             new_stones.append(int(ss[:len(ss)//2]))
#             new_stones.append(int(ss[len(ss)//2:]))
#         else:
#             new_stones.append(stone * 2024)
#     stones = new_stones

from functools import cache
@cache
def count_stones(stone, blink):
    if blink == 0:
        return 1
    if stone == 0:
        return count_stones(1, blink - 1)
    elif len(str(stone)) % 2 == 0:
        ss = str(stone)
        l = len(ss)
        return count_stones(int(ss[:l//2]), blink - 1) + count_stones(int(ss[l//2:]), blink - 1)
        new_stones.append(int(ss[int(len(ss)/2):]))
    else:
        return count_stones(stone * 2024, blink - 1)
    

answer_p1 = sum(count_stones(stone, 25) for stone in stones)

answer_p2 = sum(count_stones(stone, 75) for stone in stones)

# Print out the answers
print(f"\33[32m__P1__: \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__: \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print(f"\33[35mTook \33[1;35m{time.process_time_ns() / 1000000000}\33[0m\33[35m seconds to run\33[0m")