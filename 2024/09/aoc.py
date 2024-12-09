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

disk_map = open('input.txt').read()
# read input data and split into list of lines
disk = []
data_indicies = []
space_indicies = []
data_blocks = 0
for index, block in enumerate(disk_map):
    if index % 2 == 0:
        # is data block

        disk.extend([int(index / 2) for i in range(int(block))])
        data_blocks += int(block)
    else:
        disk.extend(list("." * int(block)))
        # is blank space

        disk.insert()

for i, block in enumerate(disk):
    if block == ".":
        space_indicies.append(i)
    else:
        data_indicies.append(i)

#print("".join(map(str, disk)))
##print(f"{data_indicies=}\n{space_indicies=}")
# print(disk[:data_blocks].count("."))
# print(disk.index("."))

while space_indicies[0] < data_indicies[-1]:
    whitespace = space_indicies.pop(0)

    last_number = data_indicies.pop()
        
    disk[whitespace], disk[last_number] = disk[last_number], disk[whitespace]

    #print("".join(map(str, disk)))

#print(disk)
for index, block in enumerate(disk):
    #print(f"{index=}, {block=}")
    if block == ".":
        break
    answer_p1 += index * int(block)


# Print out the answers
print(f"\33[32m__P1__: \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__: \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print(f"\33[35mTook \33[1;35m{time.process_time_ns() / 1000000000}\33[0m\33[35m seconds to run\33[0m")