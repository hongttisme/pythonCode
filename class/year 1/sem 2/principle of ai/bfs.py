from collections import defaultdict, deque

graph = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['E'],
    'D': ['G'],
    'E': ['G'],
    'G': []
}


# Define a function for Breadth-First Search (BFS) with a goal
def bfs_with_goal(graph, start, goal):
    # Initialize data structures for BFS
    visited = set()  # Set to keep track of visited nodes
    queue = deque()  # Queue for BFS traversal
    result = []  # list to store the BFS traversal path

    queue.append(start)

    while queue:
        # Dequeue the first node from the queue
        node = queue.popleft()

        # Add the node to the result path
        result.append(node)

        # Check if the current node is the goal node
        if node == goal:
            break  # Stop when reaching the gaol node

        for neighbor in graph[node]:
            # Check if the neighbor has not been visited
            if neighbor not in visited:
                # Enqueue the unvisited neighbor
                queue.append(neighbor)
                # Mark the neighbor as visited
                visited.add(neighbor)
    # Return the BFS traversal path
    return result


start_node = 'A'
goal_node = 'G'

bfs_result = bfs_with_goal(graph, start_node, goal_node)
print(bfs_result)

