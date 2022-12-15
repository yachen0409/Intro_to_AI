import csv
edgeFile = 'edges.csv'


def dfs(start, end):
    # Begin your code (Part 2)
    '''
    1. Construct adjlist with dictionary(start:[end, distance])
    2. Running bfs with stack:list
       While len(queue)>0
       Pop out the last node 
       Check whether adjancent nodes are visited or not
       if not visit: mark it as visited node and add it to stack:list, visited:set 
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
    stack = []
    parent = {}
    visited = set()
    stack.append(start)
    visited.add(start)
    find = False
    while (len(stack)>0):
        temp_node = stack.pop()
        if adjlist.get(temp_node) == None:
            continue
        else:
            for neighbor in adjlist[temp_node]:
                if neighbor[0] not in visited :
                    stack.append(neighbor[0])
                    visited.add(neighbor[0])
                    # if neighbor in parent:
                    #     parent[neighbor[0]].append ([temp_node, neighbor[1]])
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
    # End your code (Part 2)


if __name__ == '__main__':
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')