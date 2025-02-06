from scip_max_flow import make_random_instance, plot_flow, max_flow
import numpy as np


def Ford_Fulkerson(adj, s, t):  # FIXME: This function is not working properly
    '''
    adj: dict - adjacency map of the graph
    s: int - source node
    t: int - target node
    return: dict - flow values for each edge
    '''
    n = len(adj)
    graph_expanded = [{} for i in range(n)]
    flow = {}
    for i in range(n):
        for j, c in adj[i].items():
            graph_expanded[i][j] = c  # forward edge
            # if i != s and j != t:
            if i not in adj[j]:
                graph_expanded[j][i] = 0  # artificial reverse edge
            flow[i, j] = 0
            flow[j, i] = 0

    def DFS(path):
        i = path[-1]
        if i == t:
            return True  # found a path from s to t
        neighbors = [ (j,c) for j, c in graph_expanded[i].items() if c > flow[i, j] and j not in path]
        neighbors.sort(key=lambda x: x[1]-flow[i, x[0]], reverse=True)
        for j, c_ij in neighbors:
            if c_ij > flow[i, j] and j not in path:
                path.append(j)
                if DFS(path):
                    return True
                path.pop()
        return False

    path = [s]
    value = 0
    ub = min(sum(adj[s].values()), sum(adj[t].values()))
    while DFS(path):
        # print(path)
        bn = np.inf  # bottleneck
        for i in range(len(path)-1):
            bn = min(bn, graph_expanded[path[i]][path[i+1]] - flow[path[i], path[i+1]])
        for i in range(len(path)-1):
            flow[path[i], path[i+1]] += bn
            flow[path[i+1], path[i]] -= bn
        value += bn
        print(f"Value: {value} UB: {ub}")
        if value == ub:
            break
        path = [s]
    # remove edges with zero or negative flow
    flow = {k: v for k, v in flow.items() if v > 0}
    return flow, value


if __name__ == '__main__':
    n = 50
    np.random.seed(9)
    points, edges = make_random_instance(n=n, min_degree=2, max_degree=5, max_capacity=100)
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
