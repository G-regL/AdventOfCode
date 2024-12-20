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


data = open(ARG_data).read().split('\n')

max_r = len(data)
max_c = len(data[0])

grid = {(r,c): char for r, row in enumerate(data) for c, char in enumerate(row)}

start = dict((v,k) for k,v in grid.items())["S"]
end = dict((v,k) for k,v in grid.items())["E"]

from collections import deque
from itertools import combinations

def bfs(grid):
    queue = deque([(start, 0)])
    #visited = set()
    distances = {start: 0}
    while queue:
        (row, column), length = queue.popleft()
        if (row, column) == end: continue
        for (nr, nc) in [(row + 1, column), (row - 1, column), (row, column + 1), (row, column - 1)]:
            if 0 > nr or nr >= max_r or 0 > nc or nc >= max_c: continue
            if grid[(nr, nc)] == "#": continue
            if (nr, nc) in distances: continue

            #visited.add((nr, nc))
            queue.append(((nr, nc), length + 1))
            distances[(nr, nc)] = length + 1
    
    #print(distances)

    return (length + 1), distances

_, distances = bfs(grid)
#print(distances)

# race_length = sum([1 for c in grid.values() if c == "."]) + 1

def find_cheats(distances, cheat_length = 2, minium_cheat = 20):
    valid_cheats = 0
    for (pos1, dist1), (pos2, dist2) in combinations(distances.items(), 2):
        manhattan = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
        if manhattan <= cheat_length:
            shortcut_distance = dist2 - dist1 - manhattan
            #print(shortcut_distance)
            if shortcut_distance >= minium_cheat:
                #print(pos1, pos2, dist2 - dist1 - manhattan)
                valid_cheats += 1

    return valid_cheats

answer_p1 = find_cheats(distances, minium_cheat=100)
answer_p2 = find_cheats(distances, minium_cheat=100, cheat_length=20)


# Print out the answers
print(f"\33[32m__P1__: \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__: \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print(f"\33[35mTook \33[1;35m{time.process_time_ns() / 1000000000}\33[0m\33[35m seconds to run\33[0m")