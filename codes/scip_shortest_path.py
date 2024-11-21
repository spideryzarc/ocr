from pyscipopt import Model
from pyscipopt import quicksum as qsum
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def make_random_instance(n: int = 10, min_degree: int = 2, max_degree: int = 5) -> tuple:
    '''
    n: int - number of nodes
    min_degree: int - minimum degree of each node
    max_degree: int - maximum degree of each node
    return: tuple - (points, edges) where points is a np.array of shape (n, 2) and edges is a dict of dict edge[i,j] = cost
    '''
    points = np.random.rand(n, 2)  # random points
    edges = {}
    # Precompute the distance matrix (copilot  made it, don't you ask me how it does it)
    D = np.linalg.norm(points[:, np.newaxis, :] - points[np.newaxis, :, :], axis=2)
    np.fill_diagonal(D, np.inf)
    for i in range(n):
        n_neighbors = random.randint(min_degree, max_degree)
        # Select neighbors based on precomputed distances
        neighbors = np.argsort(D[i])[:max_degree]
        if len(neighbors) > n_neighbors:
            neighbors = np.random.choice(neighbors, n_neighbors, replace=False)
        for j in neighbors:
            edges[i, j] = D[i, j]
    return points, edges


def plot_path(points, path=None):
    '''
    points: np.array - list of points in the plane
    edges: dict - edge[i][j] = cost
    path: list - list of points indices
    '''
    fig, ax = plt.subplots()
    for i, j in edges.keys():
        arrow = mpatches.FancyArrow(points[i, 0], points[i, 1],
                                    points[j, 0] - points[i, 0],
                                    points[j, 1] - points[i, 1],
                                    width=0.001, length_includes_head=True,
                                    color='#cfb6b6')
        ax.add_patch(arrow)
        # plt.text((points[i, 0] + points[j, 0]) / 2, (points[i, 1] + points[j, 1]) / 2, f'{edges[i][j]:.2f}', color='blue')

    plt.scatter(points[1:-1, 0], points[1:-1, 1], color='black')
    # Highlight source and target points
    plt.scatter(points[path[0], 0], points[path[0], 1], color='#4c9242', s=50, label='Source')
    plt.scatter(points[path[-1], 0], points[path[-1], 1], color='#c94b4b', s=50, label='Target')

    if path is not None:
        for i in range(len(path)-1):
            arrow = mpatches.FancyArrow(points[path[i], 0], points[path[i], 1],
                                        points[path[i+1], 0] - points[path[i], 0],
                                        points[path[i+1], 1] - points[path[i], 1],
                                        width=0.005, length_includes_head=True,
                                        color='#42adc0')
            ax.add_patch(arrow)
    ax.set_aspect('equal', adjustable='box')
    plt.show()


def shortest_path(n: int, edges: dict, s: int, t: int) -> tuple:
    '''
    n: int - number of nodes
    edges: dict - edge[i][j] = cost
    s: int - source node
    t: int - target node
    return: tuple - (min_cost, path)
    '''
    model = Model("shortest_path")
    x = {(i, j): model.addVar(vtype="C", lb=0, ub=1) for i, j in edges}
    # add objective function
    model.setObjective(qsum(edges[i, j]*x[i, j] for i, j in edges), "minimize")
    # add constraints
    for k in range(n):
        if k == s:
            model.addCons(qsum(x[k, j] for j in range(n) if (k, j) in edges)
                          - qsum(x[i, k] for i in range(n) if (i, k) in edges) == 1)
        elif k == t:
            model.addCons(qsum(x[k, j] for j in range(n) if (k, j) in edges)
                          - qsum(x[i, k] for i in range(n) if (i, k) in edges) == -1)
        else:
            model.addCons(qsum(x[k, j] for j in range(n) if (k, j) in edges)
                          - qsum(x[i, k] for i in range(n) if (i, k) in edges) == 0)
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
        path.append(next(j for i, j in edges if i == path[-1] and model.getVal(x[i, j]) > 0.5))
    return min_cost, path


if __name__ == "__main__":
    # Generate random instance
    n = 100
    points, edges = make_random_instance(n=n, min_degree=4, max_degree=5)

    # Choose source and target nodes as the ones with minimum and maximum sum of coordinates
    s = min(range(n), key=lambda i: points[i, 0]+points[i, 1])
    t = max(range(n), key=lambda i: points[i, 0]+points[i, 1])

    min_cost, path = shortest_path(n, edges, s, t)

    plot_path(points, path)
    print("Min cost:", min_cost)
    print("Path:", path)
