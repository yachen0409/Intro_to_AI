import csv
import queue
edgeFile = 'edges.csv'


def ucs(start, end):
    # Begin your code (Part 3)
    '''
    1. Construct adjlist with dictionary(start:{end:distance})
    2. Running ucs with q = queue.priorityQueue()
       While len(q)>0
       Pop out the first node with smallest distance value 
       if find end: break from the loop
       Calculate newdist with mindist:dict and adjlist
       if newdist < mindist: update mindist, record parent node, and but it into q again
    3. Backtracking for getting route from start to end
    '''

    adjlist = {}
    mindist = {}
    file = open(edgeFile)
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        temp_start = int(row[0])
        temp_end = int(row[1])
        temp_dist = float(row[2])
        if temp_start not in adjlist:
            adjlist[temp_start] = {}
        adjlist[temp_start][temp_end] = temp_dist
        if temp_start not in mindist:
            mindist[temp_start] = float("inf")
    
    q = queue.PriorityQueue()
    visited = []
    parent = {}
    mindist[start] = 0
    visited.append(start)
    q.put([mindist[start], start])
    while not q.empty():
        cur_dist, current = q.get()
        if current == end:
            break
        for neighbor in adjlist[current]:
            newdist = mindist[current] + adjlist[current][neighbor]
            if neighbor in mindist:
                if newdist < mindist[neighbor]:
                    mindist[neighbor] = newdist
                    parent[neighbor] = current
                    q.put([mindist[neighbor], neighbor]) 
                    # if neighbor not in visited:
                    visited.append(neighbor)                    
    
    path = [end]
    while path[-1] != start:
        current = path[-1]
        path.append(parent[current])

    return path, mindist[end], len(visited)    
    #raise NotImplementedError("To be implemented")
    # End your code (Part 3)

if __name__ == '__main__':
    path, dist, num_visited = ucs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
