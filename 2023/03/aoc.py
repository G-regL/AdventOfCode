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

def in_bounds(x,y, x_offset = 0, y_offset = 0):
    if (x_limit[0] <= x + x_offset <= x_limit[1]) and (y_limit[0] <= y + y_offset <= y_limit[1]):
        #debug(f"in_bounds {x + x_offset},{y + y_offset} TRUE")
        return True
    
    #debug(f"in_bounds {x + x_offset},{y + y_offset} FALSE")
    return False

answer_p1 = 0
answer_p2 = 0

# read input data and split into list of lines
grid = open(ARG_data).read().split('\n')

x_limit = [0,len(grid[0]) - 1]
y_limit = [0,len(grid) - 1]

debug(f' foundn x_limits {x_limit}, and y_limits {y_limit}')
adjacent_delta_coords = [[0,-1], [1,-1], [1, 0], [1,1], [0, 1], [-1,1], [-1,0], [-1,-1]]

part_numbers = []
number = ""
number_touching_symbol = False

gear_ratios = []
# loop through lines
for y,line in enumerate(grid):
    for x,char in enumerate(line):


        # We don't care about things that aren't digits or *'s in our grid
        if not char.isdigit() and char != "*":
            if number_touching_symbol:
                debug(f"Adding {number} to parts list")
                part_numbers.append(int(number))
            #elif char == ".":
                #debug(f"  igoring because is .")
            #else:
            #    debug(f"{number} not ajdacent to symbol")

            number = ""
            number_touching_symbol = False
            continue

        #Part 1 detection loop
        if char.isdigit():
            number += char
            for adj in adjacent_delta_coords:
                #if the adjacent character is outside the grid, we don't do anything
                if not in_bounds(x, y, adj[0], adj[1]):
                    #debug(f"  {x + adj[0]},{y + adj[1]} is out of bounds")
                    continue

                #debug(f"  getting char at {x + adj[0]},{y + adj[1]}")
                adj_char = grid[y + adj[1]][x + adj[0]]
                #debug(f'  {adj_char} at {x + adj[0]},{y + adj[1]} ({adj[0]},{adj[1]}) is adjacent')
                #debug(f"    in bounds")
                #If the adjacent character ia a . or another digit, go to the next adjacent character
                if adj_char == "." or adj_char.isdigit():
                    #debug(f'    is . or digit')
                    continue

                #debug(f'    not . or digit')

                #debug(f"    has to be a symbol, right?")
                number_touching_symbol = True

        # Part 2 detection
        if char == "*":
            debug(f"char {char} at {x},{y}")
            
            debug(f'_P2_  is *, so doing gear ratio detection')
            found_gear_ratio = False
            found_first_gear = True
            gears = set()
            # Look around and find a number
            for adj in adjacent_delta_coords:
                if found_gear_ratio:
                    debug(f"  Found gear ratio, breaking out of adjacent adjacent_delta_coords loop")
                    break

                #if the adjacent character is outside the grid, we don't do anything
                if not in_bounds(x, y, adj[0], adj[1]):
                    #debug(f"  {x + adj[0]},{y + adj[1]} is out of bounds")
                    continue
                #debug(f"   {x + adj[0]},{y + adj[1]} in bounds")

                adj_char = grid[y + adj[1]][x + adj[0]]

                #If the adjacent character a digit, follow that 
                if adj_char.isdigit():
                    debug(f'  {adj_char} at {x + adj[0]},{y + adj[1]} ({adj[0]},{adj[1]}) is digit')
                    gear = ""
                    for offset in range(-3,3):
                        if found_gear_ratio:
                            debug(f"    Found gear ratio, breaking out of offset loop")
                            break

                        if not in_bounds(x, y, adj[0] + offset):
                            continue
                        
                        #debug(f"  distance from * ({x},{adj[0] + offset}={abs(x - (adj[0] + offset))})")
                        if abs(x - (adj[0] + offset)) > 7:
                            debug(f"  We're too far from the * ({x},{adj[0] + offset}={abs(x - (adj[0] + offset))})")
                            continue

                        adj_gear_char = grid[y + adj[1]][x + adj[0] + offset]

        
                        #debug(f'    adj_hear_char {adj_gear_char} at {x + adj[0] + offset},{y + adj[1]}')
                        # We found a digit, so look either side of it to see if that's *also* a digit
                        if adj_gear_char.isdigit():
                            #debug(f"     {adj_gear_char} is a digit")
                            gear += adj_gear_char
                            debug(f"      {gear}")
                        

                        if len(gear) > 1 or not adj_gear_char.isdigit():
                            #debug(f"      {adj_gear_char} is something other than a digit")
                            gears.add(int(gear))
                            debug(f"      adding {gear} to gears:{gears}")
                            gear = ""
                                
                            #else:
                                #debug(f"      neither of the two if things")

                        if len(gears) == 2:
                            found_gear_ratio = True
                            debug(f"        append {math.prod(gears)} to gear_ratios")
                            gear_ratios.append(math.prod(gears))
                            gears = set()
                            gear = ""

debug(f" gear ratios {gear_ratios}")





debug(f" Parts list: {part_numbers}")
# Print out the answers
print(f"__P1__ Sum of part numbers: {sum(part_numbers)}")
print(f"__P2__ Sum of gear ratios: {sum(gear_ratios)}")

# Tell me how inefficecient my code is
print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))