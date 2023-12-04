import sys, getopt
import time

import math

# By default I want the real input, and *not* to debug.
ARG_data = 'input.txt'
ARG_debugLogging = False

# Get the args off the command-line
opts, args = getopt.getopt(sys.argv[1:],"td",["test","debug"])
for opt, arg in opts:
    if opt in ("-t", "--test"):
        ARG_data = 'test.txt'
    elif opt in ("-d", "--debug"):
        ARG_debugLogging = True

# Useful during testing to see what the hell is going on
def debug(thing):
    if ARG_debugLogging:
        print(f"DEBUG:{thing}")

#created this method, as I was originally using it a bunch of times for P2, but in the end didn't need to. Still makes life easier though.
def in_bounds(x,y, x_offset = 0, y_offset = 0):
    if (x_limit[0] <= x + x_offset <= x_limit[1]) and (y_limit[0] <= y + y_offset <= y_limit[1]):
        return True
    return False

answer_p1 = 0
answer_p2 = 0

# read input data and split into list of lines
grid = open(ARG_data).read().split('\n')

# the lower/upper bounds of our grid, so we can check for out of bounds
x_limit = [0,len(grid[0]) - 1]
y_limit = [0,len(grid) - 1]


debug(f' foundn x_limits {x_limit}, and y_limits {y_limit}')

# This is the list of offsets for the 8 grid locations around any given point
adjacent_delta_coords = [[0,-1], [1,-1], [1, 0], [1,1], [0, 1], [-1,1], [-1,0], [-1,-1]]

# Setup some vars, I guess.
part_numbers = []
number = ""
number_touching_symbol = False
number_touching_gear = ""
gears = {}
gear_ratios = []

# loop through rows/columns
for y,line in enumerate(grid):
    for x,char in enumerate(line):

        # We don't care about things that aren't digits or *'s in our grid
        if not char.isdigit():
            if number_touching_symbol:
                debug(f"Adding {number} to parts list")
                part_numbers.append(int(number))
                            
            # Part 2 detection
            if number_touching_gear:
                debug(f" found gear at {number_touching_gear}")
                if number_touching_gear in gears.keys():
                    gears[number_touching_gear].append(int(number))
                else:
                    gears[number_touching_gear] = [int(number)]

            #reset the vars for the next number
            number = ""
            number_touching_symbol = False
            number_touching_gear = ""
            continue

        #Part 1 detection loop
        if char.isdigit():
            number += char
            for adj in adjacent_delta_coords:
                #if the adjacent character is outside the grid, we don't do anything
                if not in_bounds(x, y, adj[0], adj[1]):
                    continue

                # save the current adjacent char to a variable for easy re-use later.
                adj_char = grid[y + adj[1]][x + adj[0]]

                #If the adjacent character ia a . or another digit, go to the next adjacent character
                if adj_char == "." or adj_char.isdigit():
                    continue

                # Save the location of a gear, for use in Part 2
                if adj_char == "*":
                    number_touching_gear = str(x + adj[0]) + "-" + str(y + adj[1])

                # If the adjacent char isn't out of bounds, a ., or a digit, it *must*be a symbol, so we've found a part
                number_touching_symbol = True

debug(f" gears: {gears}")
for _ , gear in gears.items():
    #We only calculate gear ratios between two parts..
    if len(gear) == 2:
        gear_ratios.append(math.prod(gear))
debug(f" gear ratios {gear_ratios}")

debug(f" Parts list: {part_numbers}")
# Print out the answers
print(f"__P1__ Sum of part numbers: {sum(part_numbers)}")
print(f"__P2__ Sum of gear ratios: {sum(gear_ratios)}")

# Tell me how inefficecient my code is
print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))