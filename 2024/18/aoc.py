import sys, getopt
import time

# By default I want the real input, and *not* to debug.
ARG_data = 'input.txt'
ARG_debugLogging = False
ARG_drawGrid = False

grid_size = 70
num_bytes = 1024

# Get the args off the command-line
opts, args = getopt.getopt(sys.argv[1:],"tdg",["test","debug","grid"])
for opt, arg in opts:
    if opt in ("-t", "--test"):
        print(f"\33[31mUSING TEST DATA\33[0m")
        ARG_data = 'test.txt'
        grid_size = 6
        num_bytes = 12
    elif opt in ("-d", "--debug"):
        ARG_debugLogging = True
    elif opt in ("-g", "--grid"):
        ARG_drawGrid = True

# Useful during testing to see what the hell is going on
def debug(thing):
    if ARG_debugLogging:
        print(f"\33[39mDEBUG:\33[0m {thing}")

def draw_grid(size, bytes, path):
    for r in range(size +1):
        line = ""
        for c in range(size +1):
            if (r, c) in bytes:
                line += "#"
            elif (r, c) in path:
                line += "O"
            else:
                line += "."
        print(line)

answer_p1 = 0
answer_p2 = 0

from collections import deque
#INPUT
bytes = [(int(line.split(",")[1]), int(line.split(",")[0])) for line in open(ARG_data).read().split('\n') ]

def bfs(bytes, grid_size):
    seen = set(bytes)

    queue = deque([((0,0), set([(0,0)]))])
    shortest = float("inf")
    shortest_path = []
    while queue:
        (row, column), path = queue.popleft()
        #print(row, column, path)
        #new_path = set()
        #new_path.add

        if (row, column) == (grid_size, grid_size):
            #print(f"Found end")
            if len(path) < shortest:
                #print(f"({len(path)}) smaller than {shortest=}")
                shortest_path = path
                shortest = len(path)
        
        if (row, column) in bytes or (row, column) in seen:
            continue

        seen.add((row, column))

        for (dr, dc) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            row_new, column_new = row + dr, column + dc
            if 0 > row_new or row_new > grid_size or 0 > column_new or column_new > grid_size:
                #print(f"dir ({row_new},{column_new}) out of bounds")
                continue
            


            if (row_new, column_new) not in path:
                new_path = set(path)
                #print(f"({row_new},{column_new}) not seen, and not in path")
                new_path.add((row_new, column_new))
                queue.append(((row_new, column_new), new_path))
        
        #ic(queue)
        #print("\n")
    return shortest - 1, shortest_path

answer_p1, p1_path = bfs(bytes[:num_bytes], grid_size)

# Repeat until the pointers low and high meet each other
high = len(bytes) - 1
low = num_bytes
while low < high:
    mid = (low + high) //2

    path_length, _ = bfs(bytes[:mid], grid_size)

    if path_length == float("inf"):
        high = mid
    else:
        low = mid + 1




answer_p2 = f"{bytes[low -1][1]},{bytes[low -1][0]}"
# Print out the answers
print(f"\33[32m__P1__: \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__: \33[1m{answer_p2}\33[0m")

if ARG_drawGrid:

    draw_grid(grid_size, bytes[:num_bytes], p1_path )


# Tell me how inefficecient my code is
print(f"\33[35mTook \33[1;35m{time.process_time_ns() / 1000000000}\33[0m\33[35m seconds to run\33[0m")