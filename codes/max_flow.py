from scip_max_flow import make_random_instance, plot_flow, max_flow
import numpy as np
from copy import deepcopy


def Ford_Fulkerson(adj:list, s:int, t:int)->tuple:
    '''
    adj: dict - adjacency map of the graph where adj[i][j] is the capacity of the edge from node i to node j
    s: int - source node
    t: int - target node
    return: tuple - (flow, value) where flow is a dict of flow values for each edge and value is the maximum flow value
    '''
    n = len(adj) # number of nodes
    flow = {(i,j): 0 for i in range(n) for j in adj[i]} # flow values
    flow.update({(j,i): 0 for i in range(n) for j in adj[i]}) # reverse flow values
    graph_expanded = deepcopy(adj) # expanded graph 
    # add reverse edges with zero capacity
    for i,j in flow:
        if i!=t and j!=s and j not in adj[i]:
            graph_expanded[i][j] = 0
               
    def DFS(): # Depth First Search )    
        stack = [s] # stack of nodes to visit
        prev = {s: None} # previous node for each node, also used as visited set
        while stack:
            i = stack.pop() # deepest node
            if i == t: # target node reached
                # build path from target to source
                path = [t] 
                while prev[path[-1]] is not None:
                    path.append(prev[path[-1]])
                return path[::-1] # return path reversed
            # add not saturated and not visited neighbors to the stack
            neighbors = [j for j in graph_expanded[i] if graph_expanded[i][j] > flow[i, j] and j not in prev]
            stack.extend(neighbors) # add neighbors to the stack
            for j in neighbors:
                prev[j] = i
        return False

    value = 0
    while True:
        path = DFS()
        if not path:
            break
        # print(path)
        bn = np.inf  # bottleneck
        for i in range(len(path)-1):
            bn = min(bn, graph_expanded[path[i]][path[i+1]] - flow[path[i], path[i+1]])
        # update flow values
        for i in range(len(path)-1):
            flow[path[i], path[i+1]] += bn # forward flow
            flow[path[i+1], path[i]] -= bn # reverse flow
        value += bn # update total flow value
        print(f"Value: {value}")

    # remove edges with zero or negative flow
    flow = {k: v for k, v in flow.items() if v > 0}
    return flow, value


if __name__ == '__main__':
    n = 200
    np.random.seed(0)
    points, edges = make_random_instance(n=n, min_degree=3, max_degree=5, max_capacity=100)
    # Choose source and target nodes as the ones with minimum and maximum sum of coordinates
    s = min(range(n), key=lambda i: points[i, 0]+points[i, 1])
    t = max(range(n), key=lambda i: points[i, 0]+points[i, 1])
    max_flow_value, flow = max_flow(n, edges, s, t)
    print(f"Max flow from node {s} to node {t}: {max_flow_value}")
    
    # plot_flow(points, edges)
    # plt.show()

    # convert to adjacency map
    adj = [{} for i in range(n)]
    for i, j in edges:
        adj[i][j] = edges[i, j]

    print(f"Source node: {s}, Target node: {t}")
    flow, value = Ford_Fulkerson(adj, s, t)
    print(f"Max flow from node {s} to node {t}: {value}")
    plot_flow(points, edges, flow)
