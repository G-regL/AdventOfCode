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
data = open(ARG_data).read().split('\n')

# loop through lines
for line in data:
    # split the game number, from the cube pulls and extract the game number
    game, cube_sets = line.split(":")
    game = int(game.replace("Game ", ''))

    # split the cube pulls into a list
    cube_sets = cube_sets.strip().split(';')

    debug(f"Game {game} - {cube_sets}")

    #Set some defaults for the following loops
    # By default every game is possible, unless it's ouside the defined conditions
    game_possible = True
    # I'm using min_* var names here, despite the fact that I'm doing a max() comparison in the lower loops
    # because the wording of the questions it to find the minimum number of cubes possible for a game to be possible
    min_red = min_green = min_blue = 0

    for pull in cube_sets:
        #split this pull into it's respective cubes
        pull = pull.strip().split(',')
        debug(f'  pull - {pull}')

        # We don't know how many cubes we have in this pull, so they're all 0
        red = green = blue = 0

        #Loop through each cube in this pull
        for cube in pull:
            #Split the cube string into count, and colour
            count, colour = cube.strip().split(' ')
            debug(f'    cube - count:{count}, colour:{colour}')

            # For each colour, set it's value, and figure out if it's higher than the current min_$colour
            if colour == "red":
                red = int (count)
                min_red = max([min_red, int(count)])

            elif colour == "green":
                green = int(count)
                min_green = max([min_green, int(count)])

            elif colour == "blue":
                blue = int(count)
                min_blue = max([min_blue, int(count)])
    
        debug(f"    cubes - r{red}.g{green}.b{blue}")
        # If the number of any given cube colour in any of the pulls is higher than allowed, the whole game is impossible
        # Initially I thought it would be worth breaking out of the game loop here, but I let it run through the whole game
        if red > 12 or green > 13 or blue > 14:
            debug(f'      Found impossible pull')
            game_possible = False
    
    # If the game is in fact possible, add it's sum to the answer for Part 1
    if game_possible:
        debug(f'  Game Possible!!')
        answer_p1 += game

    #find the cumulative product for the maxium cube numbers possible.
    debug(f'  game mins - r{min_red}.g{min_green}.b{min_blue}; product:{min_red * min_green * min_blue}')
    answer_p2 += min_red * min_green * min_blue


# Print out the answers
print(f"__P1__ Sum of possible games: {answer_p1}")
print(f"__P2__ Sum of set powers: {answer_p2}")
#logger.info(line)

# Tell me how inefficecient my code is
print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))