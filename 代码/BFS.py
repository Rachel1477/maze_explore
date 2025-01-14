def bfs(maze):
    start = None
    end = None
    startpos=-1
    endpos=4
    # Traverse the maze to find the starting point (1) and exit point (4)
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == startpos and start is None:
                start = (i, j)  # The first accessible location serves as the starting point
            if maze[i][j] == endpos and end is None:
                end = (i, j)  # exit
    # If the starting or exit point cannot be found, return 'no path'
    if not start or not end:
        return []
    # The four defined directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # Initialize queues and access records
    queue = [start]  # Simulate a queue using a list
    visited = set([start])
    # Storage path information
    parent = {start: None}
    # BFS search
    while queue:
        x, y = queue.pop(0)  # The head of the queue exits the queue
        # If the current point is an exit point, construct a path
        if (x, y) == end:
            path = []
            while (x, y) != start:
                path.append((x, y))
                x, y = parent[(x, y)]
            path.append(start)
            del path[0]
            del path[-1]
            return path[::-1]  # Return the path from the starting point to the exit (reverse)
        # Traverse four directions
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] != 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))  # Join the queue at the end of the queue
                parent[(nx, ny)] = (x, y)
    # If no path is found, return 'no path'
    return []
#  调用BFS函数
# result = bfs(maze7_1)
# print(result)
