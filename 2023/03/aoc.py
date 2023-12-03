import sys, getopt
import time

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

answer_p1 = 0
answer_p2 = 0

# read input data and split into list of lines
grid = open(ARG_data).read().split('\n')

x_limit = [0,len(grid[0])]
y_limit = [0,len(grid)]

debug(f' foundn x_limits {x_limit}, and y_limits {y_limit}')
adjacent_delta_coords = [[0,-1], [1,-1], [1, 0], [1,1], [0, 1], [-1,1], [-1,0], [-1,-1]]

part_numbers = []
number = ""
number_touching_symbol = False
# loop through lines
for y,line in enumerate(grid):
    for x,char in enumerate(line):

        #debug(f"char {char} at {x},{y}")
        # We don't care about non digits in our grid
        if not char.isdigit():

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


        #Main detection loop
        if char.isdigit():
            number += char
            for adj in adjacent_delta_coords:
                #if the adjacent character is outside the grid, we don't do anything
                if not (x_limit[0] < x + adj[0] < x_limit[1]) or not (y_limit[0] < y + adj[1] < y_limit[1]):
                    #debug(f"  {x + adj[0]},{y + adj[1]} is out of bounds")
                    continue

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
            

        






debug(f" Parts list: {part_numbers}")
# Print out the answers
print(f"__P1__ Sum of part numbers: {sum(part_numbers)}")
#print(f"__P2__ Sum of set powers: {answer_p2}")

# Tell me how inefficecient my code is
print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))