from scip_max_flow import make_random_instance, plot_flow, max_flow
import numpy as np
from copy import deepcopy
from time import time
# linked list
import collections


def Ford_Fulkerson(adj: list, s: int, t: int) -> tuple:
    '''
    adj: dict - adjacency map of the graph where adj[i][j] is the capacity of the edge from node i to node j
    s: int - source node
    t: int - target node
    return: tuple - (flow, value) where flow is a dict of flow values for each edge and value is the maximum flow value
    '''
    n = len(adj)  # number of nodes
    flow = {(i, j): 0 for i in range(n) for j in adj[i]}  # flow values
    flow.update({(j, i): 0 for i in range(n)
                for j in adj[i]})  # add reverse flow values
    graph_expanded = deepcopy(adj)  # expanded graph
    # add reverse edges with zero capacity
    for i, j in flow:
        if i != t and j != s and j not in adj[i]:
            graph_expanded[i][j] = 0

    def DFS():  # Depth First Search )
        stack = [s]  # stack of nodes to visit
        # previous node for each node, also used as visited set
        prev = {s: None}
        while stack:
            i = stack.pop()  # deepest node
            if i == t:  # target node reached
                # build path from target to source
                path = [t]
                while prev[path[-1]] is not None:
                    path.append(prev[path[-1]])
                return path[::-1]  # return path reversed
            # add not saturated and not visited neighbors to the stack
            neighbors = [j for j in graph_expanded[i]
                         if graph_expanded[i][j] > flow[i, j] and j not in prev]
            if t in neighbors:
                stack.append(t)  # add only target node to the stack
            else:
                stack.extend(neighbors)  # add all neighbors to the stack
            for j in neighbors:
                prev[j] = i
        return False

    max_flow = 0
    while True:
        path = DFS()
        if not path:
            break
        # print(path)
        bn = np.inf  # bottleneck
        for i in range(len(path)-1):
            bn = min(bn, graph_expanded[path[i]][path[i+1]]
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


def Edmonds_Karp(adj: list, s: int, t: int) -> tuple:
    '''
    adj: dict - adjacency map of the graph where adj[i][j] is the capacity of the edge from node i to node j
    s: int - source node
    t: int - target node
    return: tuple - (flow, value) where flow is a dict of flow values for each edge and value is the maximum flow value
    '''
    n = len(adj)  # number of nodes
    flow = {(i, j): 0 for i in range(n) for j in adj[i]}  # flow values
    flow.update({(j, i): 0 for i in range(n)
                for j in adj[i]})  # add reverse flow values
    graph_expanded = deepcopy(adj)  # expanded graph
    # add reverse edges with zero capacity
    for i, j in flow:
        if i != t and j != s and j not in adj[i]:
            graph_expanded[i][j] = 0

    def BFS():  # Breadth First Search
        queue = collections.deque([s])  # queue of nodes to visit
        # previous node for each node, also used as visited set
        prev = {s: None}
        while queue:
            i = queue.popleft()  # shallowest node
            if i == t:  # target node reached
                # build path from target to source
                path = [t]
                while prev[path[-1]] is not None:
                    path.append(prev[path[-1]])
                return path[::-1]  # return path reversed
            # add not saturated and not visited neighbors to the stack
            neighbors = [j for j in graph_expanded[i]
                         if graph_expanded[i][j] > flow[i, j] and j not in prev]
            if t in neighbors:
                queue.append(t)  # add only target node to the stack
            else:
                queue.extend(neighbors)  # add all neighbors to the stack
            for j in neighbors:
                prev[j] = i
        return False

    max_flow = 0
    while True:
        path = BFS()
        if not path:
            break
        # print(path)
        bn = np.inf  # bottleneck
        for i in range(len(path)-1):
            bn = min(bn, graph_expanded[path[i]][path[i+1]]
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


def push_relabel(adj: list, s: int, t: int) -> tuple:
    '''
    adj: dict - adjacency map of the graph where adj[i][j] is the capacity of the edge from node i to node j
    s: int - source node
    t: int - target node
    return: tuple - (flow, value) where flow is a dict of flow values for each edge and value is the maximum flow value
    '''
    n = len(adj)  # number of nodes
    flow = {(i, j): 0 for i in range(n) for j in adj[i]}  # flow values
    flow.update({(j, i): 0 for i in range(n)
                for j in adj[i]})  # add reverse flow values
    graph_expanded = deepcopy(adj)  # expanded graph
    # add reverse edges with zero capacity
    for i, j in flow:
        if i != t and j not in adj[i]:
            graph_expanded[i][j] = 0

    excess = [0]*n  # preflow values
    excess[s] = sum(graph_expanded[s].values())  # source node has excess flow
    labels = [0]*n  # labels for each node
    labels[s] = n  # source node has highest label

    queue = collections.deque([s])  # queue of nodes to visit
    while queue:
        i = queue.popleft()  # oldest node
        if excess[i] == 0:
            continue
        for j in graph_expanded[i]:
            if labels[i] > labels[j] and graph_expanded[i][j] > flow[i, j]:
                df = min(excess[i], graph_expanded[i][j] - flow[i, j])
                flow[i, j] += df
                flow[j, i] -= df
                excess[j] += df
                excess[i] -= df
                if j != s and j != t:
                    queue.append(j)
                    # labels[j] = min(labels[k] for k in graph_expanded[j]
                    #                 if graph_expanded[j][k] > flow[j, k]) + 1
                if excess[i] == 0:
                    break
        else:  # excess[i] > 0
            if i == s:
                continue
            # labels[i] = min(labels[j] for j in graph_expanded[i]
            #                 if graph_expanded[i][j] > flow[i, j]) + 1
            labels[i] += 1
            queue.append(i)
    # remove edges with zero or negative flow
    flow = {k: v for k, v in flow.items() if v > 0}
    return flow, sum(flow[i, t] for i in range(n) if (i, t) in flow)


if __name__ == '__main__':
    n = 1000
    np.random.seed(1)
    points, edges = make_random_instance(
        n=n, min_degree=15, max_degree=100, max_capacity=1000)
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
