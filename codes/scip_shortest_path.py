from pyscipopt import Model
from pyscipopt import quicksum as qsum
import numpy as np
import random
import matplotlib.pyplot as plt


def make_random_instance(n: int = 10, min_degree: int = 2, max_degree: int = 5) -> tuple:
    '''
    n: int - number of nodes
    min_degree: int - minimum degree of each node
    max_degree: int - maximum degree of each node
    return: tuple - (points, edges) where points is a np.array of shape (n, 2) and edges is a dict of dict edge[i][j] = cost
    '''
    points = np.random.rand(n, 2)  # random points
    edges = {}
    c = np.zeros(n)  # cost vector
    for i in range(n):
        for j in range(n):
            c[j] = np.linalg.norm(points[i]-points[j])
        c[i] = np.inf
        edges[i] = {}
        n_neighbors = random.randint(min_degree, max_degree+1)
        # select n_neighbors from max_degree closest nodes
        neighbors = np.argsort(c)[:max_degree]
        if len(neighbors) > n_neighbors:
            neighbors = np.random.choice(neighbors, n_neighbors, replace=False)
        for j in neighbors:
            edges[i][j] = c[j]
    return points, edges


def plot_path(points, edges, path=None, show_dist=False):
    '''
    points: np.array - list of points in the plane
    edges: dict - edge[i][j] = cost
    path: list - list of points indices
    '''
    for i in edges.keys():
        for j in edges[i].keys():
            plt.arrow(points[i, 0], points[i, 1], points[j, 0] - points[i, 0], points[j, 1] - points[i, 1],
                      head_width=0.01, length_includes_head=True, color='gray', alpha=0.5)
            # plt.text((points[i, 0] + points[j, 0]) / 2, (points[i, 1] + points[j, 1]) / 2, f'{edges[i][j]:.2f}', color='blue')

    if path is not None:
        for i in range(len(path)-1):
            plt.arrow(points[path[i], 0], points[path[i], 1], points[path[i+1], 0] - points[path[i], 0],
                        points[path[i+1], 1] - points[path[i], 1], head_width=0.02, length_includes_head=True, color='blue', width=0.01)
            
            # plt.text((points[path[i], 0] + points[path[i+1], 0]) / 2, (points[path[i], 1] + points[path[i+1], 1]) / 2,
            #          f'{edges[path[i]][path[i+1]]:.2f}', color='blue')
        # if show_dist:
        #     plt.text((points[path[-1], 0] + points[path[0], 0]) / 2, (points[path[-1], 1] + points[path[0], 1]) / 2,
        #              f'{edges[path[-1]][path[0]]:.2f}', color='blue')

    plt.scatter(points[:, 0], points[:, 1])
    plt.show()

def shortest_path(edges:dict, s: int, t: int) -> tuple:
    '''
    edges: dict - edge[i][j] = cost
    s: int - source node
    t: int - target node
    return: tuple - (min_cost, path) 
    '''
    n = len(edges)
    model = Model("shortest_path")
    x = {(i, j): model.addVar(vtype="C", lb=0,ub=1) for i in edges.keys() for j in edges[i].keys()}
    # add objective function
    model.setObjective(qsum(edges[i][j]*x[i, j] for i,j in x.keys()), "minimize")
    # add constraints
    for k in edges.keys():
        if k == s :
            model.addCons(
                qsum(x[i, j] for i, j in x.keys() if i == k) 
                - qsum(x[i, j] for i, j in x.keys() if j == k) == 1)
        elif k == t:
            model.addCons(
                qsum(x[i, j] for i, j in x.keys() if i == k) 
                - qsum(x[i, j] for i, j in x.keys() if j == k) == -1)
        else:
            model.addCons(
                qsum(x[i, j] for i, j in x.keys() if i == k) 
                - qsum(x[i, j] for i, j in x.keys() if j == k) == 0)
            # remove verbose
    model.hideOutput()
    # optimize
    model.optimize()
    print("Running time:", model.getSolvingTime())
    if model.getStatus() == "infeasible":
        return np.inf, []
    min_cost = model.getObjVal()
    path = [s]
    while path[-1] != t:
        for j in edges[path[-1]].keys():
            if j != path[-1] and model.getVal(x[path[-1], j]) > 0.5:
                path.append(j)
                break
    return min_cost, path

if __name__ == "__main__":
    points, edges = make_random_instance(n=1000, min_degree=4, max_degree=6)

    
    min_cost, path = shortest_path(edges, 0, 99)
    
    plot_path(points, edges, path, show_dist=True)
    print("Min cost:", min_cost)
    print("Path:", path)
