from collections import defaultdict, deque

graph = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['E'],
    'D': ['G'],
    'E': ['G'],
    'G': []
}


def dfs_with_goal(graph, start, goal):
    visited = set()
    stack = []
    result = []

    stack.append(start)
    while stack:
        node = stack.pop()

        # Add the node to the result path
        result.append(node)

        # Check if the current node is the goal node
        if node == goal:
            break  # Stop when reaching the gaol node

        if node not in visited:
            visited.add(node)

            for neighbor in reversed(graph[node]):
                if neighbor not in visited:
                    stack.append(neighbor)
    return result


start_node = 'A'
goal_node = 'G'

dfs_result = dfs_with_goal(graph, start_node, goal_node)
print(dfs_result)
