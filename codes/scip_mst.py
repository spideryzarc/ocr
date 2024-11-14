import time
from pyscipopt import Model
from pyscipopt import quicksum as qsum
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations as comb


def mst_all_circles(c: np.array) -> tuple:
    '''
    solve Minimum Spanning Tree (MST) with all circles elimination constraints (exponential number of constraints)
    c: np.array - cost matrix
    return: tuple - (min_cost, tour)
    '''
    n = c.shape[0]
    model = Model("mst")
    x = {(i, j): model.addVar(vtype="C", lb=0, ub=1) for j in range(1, n) for i in range(j)}
    # add objective function
    model.setObjective(qsum(c[i, j]*x[i, j] for i, j in x.keys()), "minimize")
    # add constraints
    model.addCons(qsum(x[i, j] for i, j in x.keys()) == n-1)
    # All possible subsets of nodes of size 2 to n-1 as Python generator
    S = (s for k in range(2, n) for s in comb(range(n), k))
    # Add subtour elimination constraints
    for s in S:
        model.addCons(qsum(x[i, j] for i in s for j in s if i < j) <= len(s)-1)
    # remove verbose
    model.hideOutput()
    # optimize
    model.optimize()
    min_cost = model.getObjVal()
    arcs = [(i, j) for i, j in x.keys() if model.getVal(x[i, j]) > 0.5]
    # print running time
    print("Running time: ", model.getSolvingTime())
    return min_cost, arcs


def make_random_instance(n: int = 10) -> tuple:
    '''
    n: int - number of points
    return: tuple - (points: np.array, c: np.array)
    '''
    # list of random points
    points = np.random.rand(n, 2)
    # cost matrix with Euclidean distance
    c = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            c[i, j] = np.linalg.norm(points[i] - points[j])
    return points, c


def mst_adhoc_circle(c: np.array, min_degree_const=True) -> tuple:
    '''
    solve Minimum Spanning Tree (MST) with adhoc circle elimination constraints
    c: np.array - cost matrix
    min_degree_const: bool - True if minimum degree constraint is added, False otherwise
    return: tuple - (min_cost, tour)
    '''
    n = c.shape[0]
    model = Model("mst")
    x = {(i, j): model.addVar(vtype="B") for j in range(1, n) for i in range(j)}
    # add objective function
    model.setObjective(qsum(c[i, j]*x[i, j] for i, j in x.keys()), "minimize")
    # add number of arcs constraint
    model.addCons(qsum(x.values()) == n-1)
    # add minimum degree constraint
    if min_degree_const:
        for k in range(n):
            model.addCons(qsum(x[i, j] for i, j in x.keys() if j == k or i == k) >= 1)
    # remove verbose
    model.hideOutput()
    # start time
    start = time.time()
    adj = np.zeros((n, n), dtype=bool)
    while True:
        model.optimize()
        # extract adjacency matrix
        adj.fill(False)
        for i, j in x.keys():
            if model.getVal(x[i, j]) > 0.5:
                adj[i, j], adj[j, i] = True, True
        # find a circle using DFS
        circle = find_circle(adj)
        if not circle:
            break
        # add subtour elimination constraint
        model.freeTransform()
        model.addCons(qsum(x[i, j] for i in circle for j in circle if i < j) <= len(circle)-1)
        print("Circle: ", circle)
    # end while
    min_cost = model.getObjVal()
    arcs = [(i, j) for i, j in x.keys() if model.getVal(x[i, j]) > 0.5]
    # print running time
    print("Running time: ", time.time()-start)
    # print constraints number
    print("Number of constraints: ", model.getNConss())
    return min_cost, arcs


def find_circle(adj: np.array) -> list:
    '''
    adj: np.array - adjacency matrix
    return: list - list of nodes in the circle
    '''
    n = len(adj)
    visited = np.zeros(n, dtype=bool)
    parent = np.full(n, -1, dtype=np.int16)

    def dfs(u):
        visited[u] = True
        for v in range(n):
            if adj[u][v]:
                if not visited[v]:
                    parent[v] = u
                    cycle = dfs(v)
                    if cycle:
                        return cycle
                elif v != parent[u]:
                    # Found a cycle, reconstruct the path
                    cycle = [v, u]
                    curr = u
                    while parent[curr] != -1 and parent[curr] != v:
                        curr = parent[curr]
                        cycle.append(int(curr))
                    return cycle
        return None

    for u in range(n):
        if not visited[u]:
            cycle = dfs(u)
            if cycle:
                return cycle
    return None


def plot_mst_sol(points, arcs):
    '''
    points: np.array - list of points
    arcs: list - list of arcs in the solution
    '''
    plt.scatter(points[:, 0], points[:, 1])
    for i, j in arcs:
        plt.plot([points[i, 0], points[j, 0]], [points[i, 1], points[j, 1]], 'r')
    plt.show()  # or return fig, ax in case of using this function in another function
    # return fig, ax in case of using this function in another function


if __name__ == "__main__":
    points, c = make_random_instance(50)
    # min_cost, arcs = mst_all_circles(c)
    min_cost, arcs = mst_adhoc_circle(c)
    # min_cost, arcs = mst_adhoc_circle(c, min_degree_const=False)
    print("Minimum cost: ", min_cost)
    plot_mst_sol(points, arcs)
