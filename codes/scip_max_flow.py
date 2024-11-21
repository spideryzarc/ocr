from pyscipopt import Model
from pyscipopt import quicksum as qsum
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def make_random_instance(n: int = 10, min_degree: int = 2, max_degree: int = 5, max_capacity: int = 100) -> tuple:
    '''
    n: int - number of nodes
    min_degree: int - minimum degree of each node
    max_degree: int - maximum degree of each node
    max_capacity: int - maximum capacity of each edge
    return: tuple - (points, edges) where points is a np.array of shape (n, 2) and edges is a dict of dict edge[i,j] = capacity
    '''
    points = np.random.rand(n, 2)  # random points
    edges = {}
    # Precompute the distance matrix (copilot made it, don't you ask me how it does it)
    D = np.linalg.norm(points[:, np.newaxis, :] - points[np.newaxis, :, :], axis=2)
    np.fill_diagonal(D, np.inf)
    for i in range(n):
        n_neighbors = random.randint(min_degree, max_degree)
        # Select neighbors based on precomputed distances
        neighbors = np.argsort(D[i])[:max_degree]
        if len(neighbors) > n_neighbors:
            neighbors = np.random.choice(neighbors, n_neighbors, replace=False)
        for j in neighbors:
            edges[i, j] = random.randint(1, max_capacity)
    return points, edges


def plot_flow(points, edges, flow=None):
    fig, ax = plt.subplots()
    for (i, j), capacity in edges.items():
        arrow = mpatches.FancyArrow(points[i, 0], points[i, 1],
                                    points[j, 0] - points[i, 0],
                                    points[j, 1] - points[i, 1],
                                    width=0.001, length_includes_head=True,
                                    color='#cfb6b6')
        ax.add_patch(arrow)
    plt.scatter(points[:, 0], points[:, 1], color='black')
    if flow is not None and len(flow) > 0:
        # Normalize flow values for color mapping
        flow_values = np.array(list(flow.values()))
        norm = plt.Normalize(vmin=flow_values.min(), vmax=flow_values.max())
        cmap = plt.cm.viridis
        for (i, j), value in flow.items():
            if value > 0:
                color = cmap(norm(value))
                arrow = mpatches.FancyArrow(points[i, 0], points[i, 1],
                                            points[j, 0] - points[i, 0],
                                            points[j, 1] - points[i, 1],
                                            width=0.005, length_includes_head=True,
                                            color=color)
                ax.add_patch(arrow)
                # Add flow label near the arrow with improved visibility
                mid_x = (points[i, 0] + points[j, 0]) / 2
                mid_y = (points[i, 1] + points[j, 1]) / 2
                ax.text(mid_x, mid_y, f'{value:.0f}',
                        color='black',
                        fontsize=8,
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2', alpha=0.7))
        # Add colorbar
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        plt.colorbar(sm, ax=ax, label='Flow Value')
    ax.set_aspect('equal', adjustable='box')
    plt.show()


def max_flow(n: int, edges: dict, s: int, t: int) -> tuple:
    '''
    n: int - number of nodes
    edges: dict - edges with capacities edges[i, j]
    s: int - source node
    t: int - sink node
    return: tuple - (max_flow_value, flow_dict)
    '''
    model = Model("max_flow")
    x = {(i, j): model.addVar(vtype="C", lb=0, ub=capacity)
         for (i, j), capacity in edges.items()}
    # Objective: maximize total flow out of source
    model.setObjective(qsum(x[s, j] for j in range(n) if (s, j) in x), "maximize")
    # Flow conservation constraints
    for k in range(n):
        if k == s or k == t:
            continue
        model.addCons(qsum(x[i, k] for i in range(n) if (i, k) in x) ==
                      qsum(x[k, j] for j in range(n) if (k, j) in x))
    model.addCons(qsum(x[i, s] for i in range(n) if (i, s) in x) == 0)
    model.addCons(qsum(x[t, j] for j in range(n) if (t, j) in x) == 0)
    model.addCons(qsum(x[i, t] for i in range(n) if (i, t) in x) ==
                  qsum(x[s, j] for j in range(n) if (s, j) in x))

    # Solve the model
    model.hideOutput()
    model.optimize()
    if model.getStatus() != "optimal":
        return 0, {}
    max_flow_value = model.getObjVal()
    flow = {(i, j): model.getVal(x[i, j]) for (i, j) in x}
    return max_flow_value, flow


if __name__ == "__main__":
    # Generate random instance
    n = 20
    points, edges = make_random_instance(n=n, min_degree=4, max_degree=5, max_capacity=100)
    # Choose source and sink nodes
    s = min(range(n), key=lambda i: points[i, 0] + points[i, 1])
    t = max(range(n), key=lambda i: points[i, 0] + points[i, 1])
    # Compute max flow
    max_flow_value, flow = max_flow(n, edges, s, t)
    print(f"Max flow from node {s} to node {t}: {max_flow_value}")
    # print("Flow values:")
    # for (i, j), value in flow.items():
    #     if value > 0:
    #         print(f"Flow from node {i} to node {j}: {value}")
    # # Plot the flow
    plot_flow(points, edges, flow)
