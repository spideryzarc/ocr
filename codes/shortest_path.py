import numpy as np
from scip_shortest_path import make_random_instance, plot_path
from heapq import heappush as push, heappop as pop


def Dijkstra(adj: dict, s: int, t: int) -> tuple:
    '''
    adj: dict - adjacency list
    s: int - source node
    t: int - target node
    return: tuple - (min_cost, path)
    '''
    n = len(adj)  # number of nodes
    dist = [np.inf]*n  # known shortest distance from source to i
    dist[s] = 0  # distance from source to itself is 0
    prev = [-1]*n  # previous node in the shortest path
    heap = [(0, s)]  # (distance, node) pairs to be explored
    while heap:  # while there are nodes to be explored
        c_si, i = pop(heap)  # get the node with the smallest distance
        if i == t:  # target node is reached
            break
        if c_si > dist[i]:  # if the distance is not the shortest,
            continue  # skip this node, it has already been explored
        for j, c_ij in adj[i]:  # for each neighbor j of i
            if dist[j] > c_si + c_ij:  # if the distance from source to j is shorter via i
                dist[j] = c_si + c_ij  # update the distance
                prev[j] = i  # update the previous node in the shortest path
                push(heap, (dist[j], j))  # add j to the nodes to be explored
    if i != t:  # target node is not reachable
        raise ValueError("Target node is not reachable")
    path = [t]  # reconstruct the shortest path from target to source
    while path[-1] != s:
        path.append(prev[path[-1]])
    return dist[t], path[::-1]  # return the shortest distance and the path in reverse order


def Bellman_Ford(adj: dict, s: int, t: int) -> tuple:
    '''
    adj: dict - adjacency list
    s: int - source node
    t: int - target node
    return: tuple - (min_cost, path)
    '''
    n = len(adj)  # number of nodes
    dist = [np.inf]*n  # known shortest distance from source to i
    dist[s] = 0  # distance from source to itself is 0
    prev = [-1]*n  # previous node in the shortest path
    for k in range(n):  # repeat n times
        flag = False  # flag to check if the distance is updated
        for i in range(n):  # for each node i
            for j, c_ij in adj[i]:  # for each neighbor j of i
                if dist[j] > dist[i] + c_ij:  # Relaxation
                    flag = True  # distance is updated
                    dist[j] = dist[i] + c_ij  # update the distance
                    prev[j] = i  # update the previous node in the shortest path
                    if k == n-1:  # if the distance is updated in the n-th iteration
                        raise ValueError("Negative cycle detected")
        if not flag:  # if the distance is not updated in the k-th iteration
            print("Converged at iteration", k)
            break
    if dist[t] == np.inf:  # target node is not reachable
        raise ValueError("Target node is not reachable")
    path = [t]  # reconstruct the shortest path from target to source
    while path[-1] != s:
        path.append(prev[path[-1]])
    return dist[t], path[::-1]  # return the shortest distance and the path in reverse order


def Floyd_Warshall(adj: dict) -> np.ndarray:
    '''
    adj: dict - adjacency list
    return: np.ndarray - shortest distance matrix
    '''
    n = len(adj)  # number of nodes
    dist = np.full((n, n), np.inf)  # known shortest distance from i to j
    nxt = np.full((n, n), -1, dtype=int)  # 
    np.fill_diagonal(dist, 0)  # distance from i to itself is 0
    for i in adj:  # for each node i
        for j, c_ij in adj[i]:  # for each neighbor j of i
            dist[i, j] = c_ij  # update the distance from i to j
            nxt[i, j] = j  # update the intermediate node in the shortest path
    for k in range(n):  # for each intermediate node k
        for i in range(n):  # for each node i
            for j in range(n):  # for each node j
                if dist[i, j] > dist[i, k] + dist[k, j]:  # Relaxation
                    dist[i, j] = dist[i, k] + dist[k, j]  # update the distance from i to j
                    nxt[i, j] = nxt[i, k] # update the intermediate node in the shortest path
    return dist, nxt  # return the shortest distance matrix and the intermediate node matrix

def Floyd_Warshall_path(nxt: np.ndarray, s: int, t: int) -> list:
    '''
    prev: np.ndarray - intermediate node matrix
    s: int - source node
    t: int - target node
    return: list - shortest path from s to t
    '''
    nxt = nxt[:,t]  # get matrix column for target node
    path = [s]  # reconstruct the shortest path from s to t
    while path[-1] != t:
        if nxt[path[-1]] == -1:  # target node is not reachable
            raise ValueError("Target node is not reachable")
        path.append(nxt[path[-1]])
    return path  # return the shortest path from s to t

if __name__ == "__main__":
    # Generate random instance
    n = 200
    np.random.seed(0)
    # np.random.seed(0)
    points, edges = make_random_instance(n=n, min_degree=4, max_degree=7)

    # convert to adjacency list
    adj = {i: [] for i in range(n)}
    for i, j in edges:
        adj[i].append((j, edges[i, j]))

    # Choose source and target nodes as the ones with minimum and maximum sum of coordinates
    s = min(range(n), key=lambda i: points[i, 0]+points[i, 1])
    t = max(range(n), key=lambda i: points[i, 0]+points[i, 1])

    # min_cost, path = Dijkstra(adj, s, t)
    # min_cost, path = Bellman_Ford(adj, s, t)
    dist, nxt = Floyd_Warshall(adj)
    
    path = Floyd_Warshall_path(nxt, s, t)

    plot_path(points, edges, path)
    # print("Min cost:", min_cost)
    # print("Path:", path)
