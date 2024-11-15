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
    c = np.zeros(n)  # cost matrix
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
                      head_width=0.01, length_includes_head=True, color='gray')
            # plt.text((points[i, 0] + points[j, 0]) / 2, (points[i, 1] + points[j, 1]) / 2, f'{edges[i][j]:.2f}', color='blue')

    if path is not None:
        for i in range(len(path)-1):
            plt.arrow(points[path[i], 0], points[path[i+1], 0] - points[path[i], 0], points[path[i+1], 1] - points[path[i], 1],
                      head_width=0.02, length_includes_head=True, color='red')
            plt.text((points[path[i], 0] + points[path[i+1], 0]) / 2, (points[path[i], 1] + points[path[i+1], 1]) / 2,
                     f'{edges[path[i]][path[i+1]]:.2f}', color='blue')
        plt.arrow(points[path[-1], 0], points[path[0], 0] - points[path[-1], 0], points[path[0], 1] - points[path[-1], 1],
                  head_width=0.02, length_includes_head=True, color='red')
        if show_dist:
            plt.text((points[path[-1], 0] + points[path[0], 0]) / 2, (points[path[-1], 1] + points[path[0], 1]) / 2,
                     f'{edges[path[-1]][path[0]]:.2f}', color='blue')

    plt.scatter(points[:, 0], points[:, 1])
    plt.show()


if __name__ == "__main__":
    points, edges = make_random_instance(n=10, min_degree=2, max_degree=3)

    plot_path(points, edges)

    print("Points:", points)
    print("Edges:", edges)
