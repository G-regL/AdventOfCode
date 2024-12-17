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

answer_p1 = -1
answer_p2 = 0

import heapq

class Node:
    def __init__(self, x, y, direction, move_cost=1, turn_cost=1000):
        self.x = x
        self.y = y
        self.direction = direction  # 'N', 'E', 'S', or 'W'
        self.move_cost = move_cost
        self.turn_cost = turn_cost
        self.visited = False
        self.distance = float('inf')
        self.prev = None
        
    def __lt__(self, other):
        return self.distance < other.distance
        
    def __eq__(self, other):
        return (self.x, self.y, self.direction) == (other.x, other.y, other.direction)

def get_neighbors(node, maze):
    directions = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
    neighbors = []
    
    for dir, (dx, dy) in directions.items():
        nx, ny = node.x + dx, node.y + dy
        
        # Check if the new position is within maze bounds and not a wall
        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] != '#':
            turn_cost = 0 if node.direction == dir else node.turn_cost
            neighbors.append((nx, ny, dir, node.move_cost + turn_cost))
    
    return neighbors

def dijkstra(maze, start, end):
    start_x, start_y = start
    end_x, end_y = end
    nodes = {}

    # Initialize nodes (four per cell for each direction)
    for x in range(len(maze)):
        for y in range(len(maze[0])):
            if maze[x][y] != '#':
                for direction in 'NESW':
                    nodes[(x, y, direction)] = Node(x, y, direction)
    
    # Define start node
    start_node = nodes[(start_x, start_y, 'E')]
    start_node.distance = 0
    
    # Priority queue for nodes to visit; initialized with start node
    queue = [(start_node.distance, start_node)]
    heapq.heapify(queue)

    shortest_path_distance = None
    
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        
        if (current_node.x, current_node.y) == (end_x, end_y):
            path = []
            current = current_node
            while current != start_node:
                path.append((current.x, current.y, current.direction))
                current = current.prev
            path.append((start_node.x, start_node.y, start_node.direction))
            path.reverse()
            return path
            # If end is reached, construct the path
            if shortest_path_distance is None:
                shortest_path_distance = current_node.distance
                print(shortest_path_distance)
            return construct_path(nodes, start_node, current_node), [(node.x, node.y, node.distance) for node in nodes.values() if node.distance <= shortest_path_distance]
        
        if current_node.visited:
            continue
        
        current_node.visited = True
        
        for nx, ny, ndir, cost in get_neighbors(current_node, maze):
            neighbor = nodes[(nx, ny, ndir)]
            if not neighbor.visited and current_node.distance + cost < neighbor.distance:
                
                neighbor.distance = current_node.distance + cost
                neighbor.prev = current_node
                heapq.heappush(queue, (neighbor.distance, neighbor))
    

    return "No path found"

def construct_path(nodes, start_node, end_node):
    path = []
    current = end_node
    while current != start_node:
        path.append((current.x, current.y, current.direction))
        current = current.prev
    path.append((start_node.x, start_node.y, start_node.direction))
    path.reverse()
    return path

# Maze representation where 'S' marks the start, 'E' marks the end, '.' marks open paths, and '#' marks walls
maze = open(ARG_data).read().split('\n')

start = None
end = None
for r, row in enumerate(maze):
    for c, char in enumerate(row):
        #maze[(r,c)] = char
        if char == "S": start = (r,c)
        if char == "E": end = (r,c)


#print(f"Start: {start}, End: {end}")
path = dijkstra(maze, start, end)

# Print the path
facing = "E"
steps = -1
turns = 0
for step in path:

    if step[2] != facing:
        turns += 1
        answer_p1 += 1000
        facing = step[2]
    
    answer_p1 += 1
    steps += 1

# Print out the answers
print(f"\33[32m__P1__: \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__: \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print(f"\33[35mTook \33[1;35m{time.process_time_ns() / 1000000000}\33[0m\33[35m seconds to run\33[0m")