import csv
import queue
edgeFile = 'edges.csv'

def bfs(start, end):
    # Begin your code (Part 1)
    '''
    1. Construct adjlist with dictionary(start:[end, distance])
    2. Running bfs with queue
       While len(queue)>0
       Pop out the first node 
       Check whether adjancent nodes are visited or not
       if not visit: mark it as visited node and add it to queue:list, visited:set 
       if find end: break from the loop
    3. Backtracking for getting route and distance from start to end
    '''
    adjlist = {}
    dist = {}
    with open(edgeFile, newline='') as csvfile:
        rows = csv.reader(csvfile)
        headings = next(rows)
        for row in rows:
            temp_start = int(row[0])
            temp_end = int(row[1])
            temp_dist = float(row[2])
            if temp_start in adjlist:
                adjlist[temp_start].append([temp_end, temp_dist])
            else:
                adjlist[temp_start] = [[temp_end, temp_dist]]
    queue = []
    parent = {}
    visited = set()
    queue.append(start)
    visited.add(start)
    find = False
    while (len(queue)>0):
        temp_node = queue.pop(0)
        if adjlist.get(temp_node) == None:
            continue
        else:
            for neighbor in adjlist[temp_node]:
                if neighbor[0] not in visited :
                    queue.append(neighbor[0])
                    visited.add(neighbor[0])
                    parent[neighbor[0]] = [temp_node, neighbor[1]] 
                    if neighbor[0] == end:
                        find = True
                        break
        if find: break
    path = [end]
    dist = 0.0
    while path[-1] != start:
        dist += parent[path[-1]][1]
        path.append(parent[path[-1]][0])
    path.reverse()

    return path, dist, len(visited)-1
    #raise NotImplementedError("To be implemented")
    # End your code (Part 1)


if __name__ == '__main__':
    path, dist, num_visited = bfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')