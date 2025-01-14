def dijkstra(maze):
    rows, cols = len(maze), len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    start = None
    end = None
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == -1:
                start = (i, j)
            elif maze[i][j] == 4:
                end = (i, j)
    if not start or not end:
        return []

    dist = [[float('inf')] * cols for _ in range(rows)]
    dist[start[0]][start[1]] = 0
    parent = {start: None}
    queue = [(0, start)]
    visited = set()
    while queue:
        queue.sort()
        current_dist, (x, y) = queue.pop(0)
        if (x, y) in visited:
            continue
        visited.add((x, y))

        if (x, y) == end:
            path = []
            while (x, y) != start:
                path.append((x, y))
                x, y = parent[(x, y)]
            path.append(start)
            del path[0]
            del path[-1]
            return path[::-1]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != 0:
                if maze[nx][ny] == 1 or maze[nx][ny] == 5:
                    time = 1
                elif maze[nx][ny] == 2:
                    time = 3
                else:
                    time = 0
                new_dist = current_dist + time
                if new_dist < dist[nx][ny]:
                    dist[nx][ny] = new_dist
                    parent[(nx, ny)] = (x, y)
                    queue.append((new_dist, (nx, ny)))
    return []



if __name__ == '__main__':
    maze = [
        [-1, 1, 0, 0, 0],
        [1, 2, 1, 0, 0],
        [1, 0, 2, 1, 1],
        [0, 1, 0, 2, 1],
        [0, 1, 1, 1, 4]
    ]

    path = dijkstra(maze)
    print(path)
