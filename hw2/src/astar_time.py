import csv
import queue
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar_time(start, end):
    # Begin your code (Part 6)
    '''
    1. Construct adjlist with dictionary(start:{end:time})
    2. Running ucs with q = queue.priorityQueue()
       While len(q)>0
       Pop out the first node with smallest travel time 
       if find end: break from the loop
       Calculate newtime with mintime:dict and herusticlist:dict(dict)
       if newtime < mintime: update mintime, record parent node, and but it into q again
    3. Backtracking for getting route from start to end
    '''
    adjlist = {}
    mintime = {}
    speed = []
    file = open(edgeFile)
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        temp_start = int(row[0])
        temp_end = int(row[1])
        temp_speed = (float(row[3])/3.6)
        speed.append(temp_speed)
        temp_time = float(row[2])/temp_speed
        if temp_start not in adjlist:
            adjlist[temp_start] = {}
        adjlist[temp_start][temp_end] = temp_time
        if temp_start not in mintime:
            mintime[temp_start] = float("inf")
    heuristiclist = {}
    file = open(heuristicFile)
    csvreader = csv.reader(file)
    header = next(csvreader)
    max_speed = max(speed)
    for row in csvreader:
        temp_node = int(row[0])
        heuristiclist[temp_node] = {}
        heuristiclist[temp_node][int(header[1])] = float(row[1])/max_speed
        heuristiclist[temp_node][int(header[2])] = float(row[2])/max_speed
        heuristiclist[temp_node][int(header[3])] = float(row[3])/max_speed

    q = queue.PriorityQueue()
    visited = []
    parent = {}
    mintime[start] = 0
    visited.append(start)
    q.put([mintime[start], start])
    while not q.empty():
        cur_dist, current = q.get()
        if current == end:
            break
        for neighbor in adjlist[current]:
            newtime = mintime[current] + adjlist[current][neighbor]
            if neighbor in mintime:
                if newtime < mintime[neighbor]:
                    mintime[neighbor] = newtime
                    priority = mintime[neighbor] + heuristiclist[neighbor][end]
                    parent[neighbor] = current
                    q.put([priority, neighbor]) 
                    visited.append(neighbor)
    path = [end]
    while path[-1] != start:
        current = path[-1]
        path.append(parent[current])
    return path, mintime[end], len(visited)
    # End your code (Part 6)


if __name__ == '__main__':
    path, time, num_visited = astar_time(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total second of path: {time}')
    print(f'The number of visited nodes: {num_visited}')
