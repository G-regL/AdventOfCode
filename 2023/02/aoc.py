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

answer_p1 = 0
answer_p2 = 0
data = open(ARG_data).read().split('\n')


for line in data:
    game, cube_sets = line.split(":")
    game = int(game.replace("Game ", ''))

    cube_sets = cube_sets.strip().split(';')

    debug(f"Game {game} - {cube_sets}")
    game_possible = True
    for pull in cube_sets:
        #pull = pulls.split(';')

        pull = pull.strip().split(',')
        debug(f'  pull - {pull}')

        red = green = blue = 0
        for cube in pull:
            count, colour = cube.strip().split(' ')
            debug(f'    cube - count:{count}, colour:{colour}')
            if colour == "red":
                red = int (count)
            elif colour == "green":
                green = int(count)
            elif colour == "blue":
                blue = int(count)
    
        debug(f"    cubes - r{red}.g{green}.b{blue}")
        if red > 12 or green > 13 or blue > 14:
            debug(f'      Found impossible pull')
            game_possible = False
                

    if game_possible:
        debug(f'  Game Possible!!')
        answer_p1 += game


print(f"__P1__ Sum of possible games: {answer_p1}")
print(f"__P2__ Sum of calibration values: {answer_p2}")
#logger.info(line)

print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))