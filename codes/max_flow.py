from scip_max_flow import make_random_instance, plot_flow
import numpy as np


def Ford_Fulkerson(adj, s, t): #FIXME: This function is not working properly
    '''
    adj: dict - adjacency map of the graph
    s: int - source node
    t: int - target node
    return: dict - flow values for each edge
    '''
    n = len(adj)
    graph_expanded = {i: {} for i in range(n)}
    flow = {}
    for i in adj:
        for j, c in adj[i].items():
            graph_expanded[i][j] = c  # forward edge
            if i != s and j != t:
                if i not in adj[j]:
                    graph_expanded[j][i] = 0  # artificial reverse edge
            flow[i, j] = 0
            flow[j, i] = 0

    def DFS(path):
        i = path[-1]
        if i == t:
            return True  # found a path from s to t
        for j, c_ij in graph_expanded[i].items():
            if c_ij > flow[i, j] and j not in path:
                path.append(j)
                if DFS(path):
                    return True
                path.pop()
        return False

    path = [s]
    value = 0
    while DFS(path):
        print(path)
        bn = np.inf  # bottleneck
        for i in range(len(path)-1):
            bn = min(bn, graph_expanded[path[i]][path[i+1]] - flow[path[i], path[i+1]])        
        for i in range(len(path)-1):
            flow[path[i], path[i+1]] += bn
            flow[path[i+1], path[i]] -= bn
        value += bn
        path = [s]
    # remove edges with zero or negative flow
    flow = {k: v for k, v in flow.items() if v > 0}
    return flow, value


if __name__ == '__main__':
    n = 10
    np.random.seed(4)
    points, edges = make_random_instance(n=n, min_degree=2, max_degree=5, max_capacity=100)
    # plot_flow(points, edges)
    # plt.show()

    # convert to adjacency map
    adj = {i: {} for i in range(n)}
    for i, j in edges:
        adj[i][j] = edges[i, j]

    # Choose source and target nodes as the ones with minimum and maximum sum of coordinates
    s = min(range(n), key=lambda i: points[i, 0]+points[i, 1])
    t = max(range(n), key=lambda i: points[i, 0]+points[i, 1])
    print(f"Source node: {s}, Target node: {t}")
    flow,value = Ford_Fulkerson(adj, s, t)
    print(f"Max flow from node {s} to node {t}: {value}")
    plot_flow(points, edges, flow)
    
