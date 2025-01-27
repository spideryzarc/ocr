import numpy as np
from scip_shortest_path import make_random_instance, plot_path
from heapq import heappush as push, heappop as pop

def Dijkstra(adj:dict, s:int, t:int) -> tuple:
    '''
    adj: dict - adjacency list
    s: int - source node
    t: int - target node
    return: tuple - (min_cost, path)
    '''
    n = len(adj)
    dist = [np.inf]*n
    dist[s] = 0
    prev = [-1]*n
    heap = [(0, s)] # (cost from source to i, i)
    while heap:
        c_si, i = pop(heap)
        if i == t:
            break
        if c_si > dist[i]:
            continue
        for j, c_ij in adj[i]:
            if dist[j] > c_si + c_ij:
                dist[j] = c_si + c_ij
                prev[j] = i
                push(heap, (dist[j], j))
    if i != t: # target node is not reachable
        raise ValueError("Target node is not reachable")
    path = [t]
    while path[-1] != s:
        path.append(prev[path[-1]])
    return dist[t], path[::-1]


def Bellman_Ford(adj:dict, s:int, t:int) -> tuple:
    '''
    adj: dict - adjacency list
    s: int - source node
    t: int - target node
    return: tuple - (min_cost, path)
    '''
    n = len(adj)
    dist = [np.inf]*n
    dist[s] = 0
    prev = [-1]*n
    for k in range(n):
        flag = False
        for i in range(n):
            for j, c_ij in adj[i]:
                if dist[j] > dist[i] + c_ij:
                    flag = True
                    dist[j] = dist[i] + c_ij
                    prev[j] = i
                    if k == n-1:
                        raise ValueError("Negative cycle detected")
        if not flag:
            print("Converged at iteration", k)
            break
    if dist[t] == np.inf: # target node is not reachable
        raise ValueError("Target node is not reachable")
    path = [t]
    while path[-1] != s:
        path.append(prev[path[-1]])
    return dist[t], path[::-1]    

if __name__ == "__main__":
    # Generate random instance
    n = 1000
    # np.random.seed(0)
    points, edges = make_random_instance(n=n, min_degree=4, max_degree=5)

    #convert to adjacency list
    adj = {i: [] for i in range(n)}
    for i, j in edges:
        adj[i].append((j, edges[i, j]))

    # Choose source and target nodes as the ones with minimum and maximum sum of coordinates
    s = min(range(n), key=lambda i: points[i, 0]+points[i, 1])
    t = max(range(n), key=lambda i: points[i, 0]+points[i, 1])

    # min_cost, path = dijkstra(adj, s, t)
    min_cost, path = Bellman_Ford(adj, s, t)

    plot_path(points, edges, path)
    # print("Min cost:", min_cost)
    # print("Path:", path)

