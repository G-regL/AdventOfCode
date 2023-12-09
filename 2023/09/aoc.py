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
        print(f"DEBUG: {thing}")

answer_p1 = 0
answer_p2 = 0

# read input data and split into list of lines
data = open(ARG_data).read().split('\n')

# loop through data
for line in data:
    layers = []
    # add sequence to the top of the layers
    layers.append([int(n) for n in line.split()])
    debug(f'number set {layers[0]}')
    all_zeros = False

    # While our our current layer isn't all 0s
    while not all_zeros:
        l = []
        for i in range(len(layers[-1]) - 1):
            # to the last layer, append the difference between the last, and second last values
            l.append(layers[-1][i+1] - layers[-1][i])

        # push our new layer to the stack
        layers.append(l)

        # Check our current layer to see if it's elements are all 0's
        if len([n for n in l if n == 0]) == len(l):
            all_zeros = True
    

    # Sum up the last elements from the whole layer stack to get the next value of the original sequence
    next = sum([item[-1] for item in layers])
    debug(f'  P1_line: {line}, {next}')
    answer_p1 += next
    
    #Part2
    # Reverse the layers so that we have the 0's list at the front, 
    #  allowing us to work back up the stack to find the previous entry of the original sequence
    layers.reverse()
    debug(f'  rev layers: {layers}')
    # Go all the down the layer stack, working out the previous value for each set, inserting it to the head of the layer
    #  Here "down the stack" is actually working our way back UP the "tree" depicted in the explanation
    for i, l in enumerate(layers[1:], start=1):
        l.insert(0, layers[i][0] - layers[i-1][0])

    # Since we worked our *all* the previous values, but we only care about the "top" one (aka, OG),
    #  we can just pull it off the end of the layer stack
    previous = layers[-1][0]
    debug(f'  P2_line: {line}, {previous}')
    answer_p2 += previous
    
# Print out the answers
print(f"__P1__ : {answer_p1}")
print(f"__P2__ : {answer_p2}")

# Tell me how inefficecient my code is
print("Took {} seconds to run".format(time.process_time_ns() / 1000000000))