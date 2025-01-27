from scip_mst import make_random_instance, plot_mst_sol
import numpy as np

def Kruskal(c:np.ndarray, edges:list = None) -> list:
    '''
    c: np.array - cost matrix
    edges: list - list of edges (i,j), if None, complete graph is considered
    return: list - list of arcs in the solution
    '''
    n = len(c)
    
    if edges is None: # complete graph
        edges = [(i, j) for i in range(n) for j in range(i)]
        
    edges.sort(key=lambda x: c[x[0], x[1]])
    
    parent = list(range(n))

    def find(u):
        if parent[u] != u:
            parent[u] = find(parent[u])
        return parent[u]

    arcs = []
    for u, v in edges:
        pu, pv = find(u), find(v)
        if pu != pv: # u and v are in different components
            arcs.append((u, v))
            parent[pu] = pv
        
    return arcs


def Prim(c:np.ndarray,edges:list = None)->list:
    '''
    c: np.array - cost matrix
    edges: list - list of edges (i,j), if None, complete graph is considered
    return: list - list of arcs in the solution
    '''
    n = len(c)
    if edges is not None:
        c_ = np.full((n, n), np.inf)
        idx_i,idx_j = zip(*edges)
        c_[idx_i, idx_j] = c[idx_i, idx_j]
        c = c_
        
    closest_in_tree = np.zeros(n, dtype=int)
    min_dist = c[0]
    non_tree = set(range(1, n))
    arcs = []
    while non_tree: # while non_tree is not empty
        u = min(non_tree, key=lambda x: min_dist[x])
        if min_dist[u] == np.inf:
            raise Exception("Graph is not connected")
        non_tree.remove(u)
        v = closest_in_tree[u]
        arcs.append((u, v))
        for w in non_tree: # update min_dist and closest_in_tree
            if c[u, w] < min_dist[w]:
                min_dist[w] = c[u, w]
                closest_in_tree[w] = u
    return arcs
        


if __name__ == "__main__":
    points, c = make_random_instance(2000)
    # min_cost, arcs = mst_all_circles(c)
    # arcs = Kruskal(c)
    arcs = Prim(c)
    plot_mst_sol(points, arcs)
    