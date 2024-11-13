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
    x = {(i, j): model.addVar(vtype="C", lb=0,ub=1) for j in range(1,n) for i in range(j)}
    # add objective function
    model.setObjective(qsum(c[i, j]*x[i, j] for i,j in x.keys()), "minimize")
    # add constraints
    model.addCons(qsum(x[i,j] for i,j in x.keys()) == n-1)
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
    arcs = [(i, j) for i,j in x.keys() if model.getVal(x[i, j]) > 0.5]
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

def mst_adhoc_circle(c: np.array) -> tuple:
    '''
    solve Minimum Spanning Tree (MST) with adhoc circle elimination constraints
    c: np.array - cost matrix
    return: tuple - (min_cost, tour)
    '''
    n = c.shape[0]
    model = Model("mst")
    x = {(i, j): model.addVar(vtype="C", lb=0,ub=1) for j in range(1,n) for i in range(j)}
    # add objective function
    model.setObjective(qsum(c[i, j]*x[i, j] for i,j in x.keys()), "minimize")
    # add constraints
    model.addCons(qsum(x[i,j] for i,j in x.keys()) == n-1)
    for k in range(n):
        model.addCons(qsum(x[i, j] for i,j in x.keys() if j==k or i==k) >= 1)
        # model.addCons(qsum(x[i, k] for i in range(k)) + qsum(x[k, j] for j in range(k+1, n)) >= 1)
    # remove verbose
    model.hideOutput()
    while True:
        # optimize
        model.optimize()
        # extract adjacency matrix
        adj = np.zeros((n, n), dtype=bool)
        for i, j in x.keys():
            if model.getVal(x[i, j]) > 0.5:
                adj[i, j] = True
                adj[j, i] = True
        circle = find_circle(adj)
        if not circle:
            break
        model.freeTransform()
        model.addCons(qsum(x[i, j] for i in circle for j in circle if i < j) <= len(circle)-1)
        print("Circle: ", circle)
    # end while
    min_cost = model.getObjVal()
    arcs = [(i, j) for i,j in x.keys() if model.getVal(x[i, j]) > 0.5]
    # print running time
    print("Running time: ", model.getSolvingTime())
    # print constraints number
    print("Number of constraints: ", model.getNConss())
    return min_cost, arcs

def find_circle(adj):
    n = len(adj)
    visited = [False] * n
    parent = [-1] * n

    def dfs(u, p):
        visited[u] = True
        for v in range(n):
            if adj[u][v]:
                if not visited[v]:
                    parent[v] = u
                    cycle = dfs(v, u)
                    if cycle:
                        return cycle
                elif v != p:
                    # Found a cycle, reconstruct the path
                    cycle = [v, u]
                    curr = u
                    while parent[curr] != -1 and parent[curr] != v:
                        curr = parent[curr]
                        cycle.append(curr)
                    cycle.reverse()
                    return cycle
        return None

    for u in range(n):
        if not visited[u]:
            cycle = dfs(u, -1)
            if cycle:
                return cycle
    return []

def plot_mst_sol(points, arcs):
    '''
    points: np.array - list of points
    arcs: list - list of arcs in the solution
    '''
    plt.scatter(points[:, 0], points[:, 1])
    for i, j in arcs:
        plt.plot([points[i, 0], points[j, 0]], [points[i, 1], points[j, 1]], 'r')
    plt.show() # or return fig, ax in case of using this function in another function
    # return fig, ax in case of using this function in another function

if __name__ == "__main__":
    points, c = make_random_instance(50)
    # min_cost, arcs = mst_all_circles(c)
    min_cost, arcs = mst_adhoc_circle(c)
    # TODO está errado, corrigir
    print("Minimum cost: ", min_cost)
    plot_mst_sol(points, arcs)
