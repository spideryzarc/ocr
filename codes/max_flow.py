from scip_max_flow import make_random_instance, plot_flow, max_flow
import numpy as np
from copy import deepcopy
from time import time
from collections import deque



def residual_graph_n_flow(graph: list[dict[int, int]]) -> tuple[list[dict[int, int]], dict[tuple[int, int], int]]:
    '''
    graph: list - adjacency map of the graph where adj[i][j] is the capacity of the edge from node i to node j
    return: tuple - (residual_graph, flow) where residual_graph is the adjacency map of the residual graph and flow is a dict of flow values for each edge 
    '''
    n = len(graph)  # number of nodes
    flow = {(i, j): 0 for i in range(n) for j in graph[i]}  # flow values
    flow.update({(j, i): 0 for i in range(n) for j in graph[i]})  # add reverse flow values
    residual_graph = deepcopy(graph)  # expanded graph
    # add reverse edges with zero capacity
    for i, j in flow:
        if i != t and j not in graph[i]:
            residual_graph[i][j] = 0
    return residual_graph, flow


def Ford_Fulkerson(adj: list[dict[int, int]], s: int, t: int) -> tuple[dict[tuple[int, int], int], int]:
    '''
    adj: dict - adjacency map of the graph where adj[i][j] is the capacity of the edge from node i to node j
    s: int - source node
    t: int - target node
    return: tuple - (flow, value) where flow is a dict of flow values for each edge and value is the maximum flow value
    '''
    n = len(adj)  # number of nodes
    capacity, flow = residual_graph_n_flow(adj)  # expanded graph and flow values

    def DFS():  # Depth First Search )
        stack = [s]  # stack of nodes to visit
        # previous node for each node, also used as visited set
        prev = [-1]*n
        while stack:
            if prev[t] != -1:  # target node reached
                path = [t]
                while prev[path[-1]] != -1:
                    path.append(prev[path[-1]])
                return path[::-1]  # return path reversed
            i = stack.pop()  # deepest node
            # add not saturated and not visited neighbors to the stack
            neighbors = [j for j in capacity[i]
                         if j != s and capacity[i][j] > flow[i, j] and prev[j] == -1]
            stack.extend(neighbors)  # add all neighbors to the stack
            for j in neighbors:
                prev[j] = i
        return False

    max_flow = 0
    MAX = max(capacity[s].values())  # maximum flow value
    while True:
        path = DFS()
        if not path:
            break
        # print(path)
        bn = MAX  # bottleneck
        for i in range(len(path)-1):
            bn = min(bn, capacity[path[i]][path[i+1]]
                     - flow[path[i], path[i+1]])
        # update flow values
        for i in range(len(path)-1):
            flow[path[i], path[i+1]] += bn  # forward flow
            flow[path[i+1], path[i]] -= bn  # reverse flow
        max_flow += bn  # update total flow value
        # print(f"Value: {max_flow}")

    # remove edges with zero or negative flow
    flow = {k: v for k, v in flow.items() if v > 0}
    return flow, max_flow


def Edmonds_Karp(adj: list[dict[int, int]], s: int, t: int) -> tuple[dict[tuple[int, int], int], int]:
    '''
    adj: dict - adjacency map of the graph where adj[i][j] is the capacity of the edge from node i to node j
    s: int - source node
    t: int - target node
    return: tuple - (flow, value) where flow is a dict of flow values for each edge and value is the maximum flow value
    '''
    n = len(adj)  # number of nodes
    capacity, flow = residual_graph_n_flow(adj)  # expanded graph and flow values

    def BFS():  # Breadth First Search
        queue = deque([s])  # queue of nodes to visit
        # previous node for each node, also used as visited set
        prev = [-1]*n
        while queue:
            if prev[t] != -1:  # target node reached
                path = [t]
                while prev[path[-1]] != -1:
                    path.append(prev[path[-1]])
                return path[::-1]  # return path reversed
            i = queue.popleft()  # shallowest node
            # add not saturated and not visited neighbors to the stack
            neighbors = [j for j in capacity[i]
                         if j != s and capacity[i][j] > flow[i, j] and prev[j] == -1]
            neighbors.sort(key=lambda j: capacity[i][j] - flow[i, j], reverse=True)  # sort by residual capacity (speedup)
            queue.extend(neighbors)  # add all neighbors to the stack
            for j in neighbors:
                prev[j] = i
        return False

    max_flow = 0
    MAX = max(capacity[s].values())  # maximum flow value
    while True:
        path = BFS()
        if not path:
            break
        # print(path)
        bn = MAX  # bottleneck
        for i in range(len(path)-1):
            bn = min(bn, capacity[path[i]][path[i+1]]
                     - flow[path[i], path[i+1]])
        # update flow values
        for i in range(len(path)-1):
            flow[path[i], path[i+1]] += bn  # forward flow
            flow[path[i+1], path[i]] -= bn  # reverse flow
        max_flow += bn  # update total flow value
        # print(f"Value: {max_flow}")

    # remove edges with zero or negative flow
    flow = {k: v for k, v in flow.items() if v > 0}
    return flow, max_flow



def push_relabel(adj: list[dict[int, int]], s: int, t: int) -> tuple[dict[tuple[int, int], int], int]:
    '''
    adj: dict - adjacency map of the graph where adj[i][j] is the capacity of the edge from node i to node j
    s: int - source node
    t: int - target node
    return: tuple - (flow, value) where flow is a dict of flow values for each edge and value is the maximum flow value
    '''
    n = len(adj)  # number of nodes
    capacity, flow = residual_graph_n_flow(adj)  # expanded graph and flow values

    excess = [0]*n  # pre-flow values
    excess[s] = sum(capacity[s].values())  # source node has excess flow
    labels = [0]*n  # labels for each node (height)
    labels[s] = n  # source node has highest label

    queue = deque([s], n)  # queue of nodes to visit
    while queue:
        i = queue.popleft()  # node to visit
        if excess[i] == 0:
            continue
        for j in capacity[i]:
            if labels[i] > labels[j] and capacity[i][j] > flow[i, j]:
                df = min(excess[i], capacity[i][j] - flow[i, j])
                flow[i, j] += df
                flow[j, i] -= df
                excess[j] += df
                excess[i] -= df
                if j != s and j != t and excess[j] == df:
                    queue.append(j)
                if excess[i] == 0:
                    break
        if excess[i] > 0 and i != s:  # relabel node i if it has excess flow
            # labels[i] = min(labels[j] for j in capacity[i]
            #                 if capacity[i][j] > flow[i, j]) + 1
            labels[i] += 1
            queue.append(i)
    # remove edges with zero or negative flow
    flow = {k: v for k, v in flow.items() if v > 0}
    return flow, sum(flow[i, t] for i in range(n) if (i, t) in flow)


if __name__ == '__main__':
    n = 500
    np.random.seed(1)
    points, edges = make_random_instance(
        n=n, min_degree=5, max_degree=400, max_capacity=1000)
    # Choose source and target nodes as the ones with minimum and maximum sum of coordinates
    s = min(range(n), key=lambda i: points[i, 0]+points[i, 1])
    t = max(range(n), key=lambda i: points[i, 0]+points[i, 1])
    # max_flow_value, flow = max_flow(n, edges, s, t)
    # print(f"Max flow from node {s} to node {t}: {max_flow_value}")

    # plot_flow(points, edges)
    # plt.show()

    # convert to adjacency map
    adj = [{} for i in range(n)]
    for i, j in edges:
        adj[i][j] = edges[i, j]

    print(f"Source node: {s}, Target node: {t}")
    t0 = time()
    flow, value = Ford_Fulkerson(adj, s, t)
    print(
        f"Ford-Fulkerson algorithm took {time()-t0:.2f} seconds - Value: {value}")
    t0 = time()
    flow, value = Edmonds_Karp(adj, s, t)
    print(
        f"Edmonds-Karp algorithm took {time()-t0:.2f} seconds - Value: {value}")
    t0 = time()
    flow, value = push_relabel(adj, s, t)
    print(
        f"Push-Relabel algorithm took {time()-t0:.2f} seconds - Value: {value}")

    # print(f"Max flow from node {s} to node {t}: {value}")
    # plot_flow(points, edges, flow)
