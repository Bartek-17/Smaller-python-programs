import random
from collections import deque

# Create a set of cities with random integer coordinates
num_cities = 9
cities = {}
for city_nr in range(1, num_cities + 1):
    x = random.randint(-100, 100)
    y = random.randint(-100, 100)
    cities[city_nr] = (x, y)


def euclidean_distance(city1, city2):
    return round(((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2) ** 0.5, 2)


# Create the weighted graph
def create_graph(connection_probability=1.0):
    graph = {}
    for city_id in cities.keys():
        graph[city_id] = {}

    for city_id1 in cities:
        for city_id2 in cities:
            if city_id1 != city_id2:
                if random.random() < connection_probability:
                    distance = euclidean_distance(cities[city_id1], cities[city_id2])
                    graph[city_id1][city_id2] = distance
                    graph[city_id2][city_id1] = distance
    return graph


graph_all_connections = create_graph(connection_probability=1)
print('Weighted graph with all connections')

for City, connections in graph_all_connections.items():
    print(f"City {City}: {connections}")


# print(graph_all_connections)

# Calculate the total travel cost
def calculate_path_cost(path, graph):
    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += graph[path[i]][path[i + 1]]
    if path[-1] in graph[path[0]]:
        total_cost += graph[path[-1]][path[0]]  # Cost of returning to the starting city from the last city
    return total_cost


# Implement Breadth First Search
def tsp_bfs(start_city, graph):
    queue = deque([(start_city, [start_city])])
    shortest_path = None
    min_cost = float('inf')

    while queue:
        current_city, path = queue.popleft()  # FIFO ( much faster than pop(0) )

        if len(path) == len(graph):
            path_cost = calculate_path_cost(path, graph)
            if path_cost < min_cost:
                min_cost = path_cost
                shortest_path = path
        else:
            for next_city in graph[current_city]:
                if next_city not in path:
                    queue.append((next_city, path + [next_city]))

    return shortest_path, round(min_cost, 2)


# Implement Depth First Search
def tsp_dfs(start_city, graph):
    stack = [(start_city, [start_city])]
    shortest_path = None
    min_cost = float('inf')

    while stack:
        current_city, path = stack.pop()  # LIFO
        if len(path) == len(graph):
            path_cost = calculate_path_cost(path, graph)
            if path_cost < min_cost:
                min_cost = path_cost
                shortest_path = path
        else:
            for next_city in graph[current_city]:
                if next_city not in path:
                    stack.append((next_city, path + [next_city]))

    return shortest_path, round(min_cost, 2)


# Solve TSP using BFS
main_city = 1

bfs_path, bfs_cost = tsp_bfs(main_city, graph_all_connections)
print(f"BFS - Shortest Path: {bfs_path}, Cost: {bfs_cost}")

# Solve TSP using DFS
dfs_path, dfs_cost = tsp_dfs(main_city, graph_all_connections)
print(f"DFS - Shortest Path: {dfs_path}, Cost: {dfs_cost}")


# Ex 3 b - Approximate the solution using Minimum Spanning Tree (minimum total edge weight for spanning all nodes)

# find the minimum spanning tree using Prim's algorithm
def prim_mst(graph, start):
    mst = {}
    for city in graph:
        mst[city] = []

    visited = {start}
    # Initialize the edges list with edges from the start city (cost, start city Nr, end city nr)
    edges = []
    for to, cost in graph[start].items():
        edges.append((cost, start, to))

    while edges:
        # Sort the edges and pop the shortest one
        edges.sort(reverse=True)
        cost, frm, to = edges.pop()

        if to not in visited:
            # Add this edge to the MST
            visited.add(to)
            mst[frm].append(to)
            mst[to].append(frm)

            # Add all edges from the new city to the edges list
            for to_next, cost in graph[to].items():
                if to_next not in visited:
                    edges.append((cost, to, to_next))
    print(mst)
    return mst


# preorder traversal
def path_calculation(tree, start):
    path = []
    stack = [start]
    visited = set()

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            path.append(node)
            # Add neighbors to the stack in reverse order to maintain preorder
            neighbors = sorted(tree[node], reverse=True)
            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append(neighbor)

    return path


# Function to approximate TSP using MST
def tsp_mst_approximation(start_city, graph):
    mst = prim_mst(graph, start_city)
    path = path_calculation(mst, start_city)
    total_cost = calculate_path_cost(path, graph)
    return path, round(total_cost, 2)


# Solve TSP using MST approximation
approx_path_mst, approx_cost_mst = tsp_mst_approximation(main_city, graph_all_connections)
print(f"MST Approximation - Shortest Path: {approx_path_mst}, Cost: {approx_cost_mst}")


# Ex 3 c - Greedy approximation

def tsp_greedy(start_city, graph):
    current_city = start_city
    path = [current_city]
    visited = {current_city}

    while len(visited) < len(graph):
        min_cost = float('inf')
        next_city = None
        for city, cost in graph[current_city].items():
            if city not in visited and cost < min_cost:
                min_cost = cost
                next_city = city
        path.append(next_city)
        visited.add(next_city)
        current_city = next_city

    # Calculate total cost using the calculate_path_cost function
    total_cost = calculate_path_cost(path, graph)

    return path, round(total_cost, 2)


# Solve TSP using Greedy approximation
approx_path_greedy, approx_cost_greedy = tsp_greedy(main_city, graph_all_connections)
print(f"Greedy Approximation - Shortest Path: {approx_path_greedy}, Cost: {approx_cost_greedy}")


# Ex 4


# returns meeting point
def bidirectional_bfs(graph, start_city, end_city):
    if start_city not in graph or end_city not in graph:
        return None, float('inf')  # Return None and infinity cost if start or end city is not in the graph

    if start_city == end_city:
        return [start_city], 0

    # queues for both directions
    queue_start = deque([start_city])
    queue_end = deque([end_city])

    # visited sets and parent dictionaries
    visited_start = {start_city}
    visited_end = {end_city}

    parent_start = {start_city: None}
    parent_end = {end_city: None}

    # Perform the bidirectional search
    while queue_start and queue_end:
        # Expand from the start side
        if queue_start:
            current_start = queue_start.popleft()
            for neighbor, cost in graph[current_start].items():
                if neighbor not in visited_start:
                    visited_start.add(neighbor)
                    parent_start[neighbor] = current_start
                    queue_start.append(neighbor)
                    if neighbor in visited_end:
                        return reconstruct_path(parent_start, parent_end, neighbor, graph)

        # Expand from the end side
        if queue_end:
            current_end = queue_end.popleft()
            for neighbor, cost in graph[current_end].items():
                if neighbor not in visited_end:
                    visited_end.add(neighbor)
                    parent_end[neighbor] = current_end
                    queue_end.append(neighbor)
                    if neighbor in visited_start:
                        return reconstruct_path(parent_start, parent_end, neighbor, graph)

    return None, float('inf')


def reconstruct_path(parent_start, parent_end, meeting_point, graph):
    # Reconstruct path from start to meeting point
    path_start = []
    current_city = meeting_point
    while current_city is not None:
        path_start.append(current_city)
        current_city = parent_start[current_city]
    path_start.reverse()

    # Reconstruct path from meeting point to end
    path_end = []
    current_city = parent_end[meeting_point]
    while current_city is not None:
        path_end.append(current_city)
        current_city = parent_end[current_city]

    # Combine both parts of the path
    full_path = path_start + path_end
    total_cost = calculate_path_cost(full_path, graph)
    return full_path, total_cost


graph_partial_connections = create_graph(connection_probability=0.2)
print('partial connections:')
print(graph_partial_connections)

bi_start_city = 1
bi_end_city = 5
bi_path, bi_path_cost = bidirectional_bfs(graph_partial_connections, bi_start_city, bi_end_city)
if (bi_path is not None) and (len(bi_path) == 2):
    bi_path_cost /= 2
if bi_path:
    print(f"Shortest Path: {bi_path}, Cost: {bi_path_cost}")
else:
    print(f"No path found between city {bi_start_city} and city {bi_end_city}.")
