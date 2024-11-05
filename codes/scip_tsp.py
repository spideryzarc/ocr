from pyscipopt import Model
from pyscipopt import quicksum as qsum
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations as comb
from itertools import product


def tsp_mtz(c: np.array) -> tuple:
    '''
    c: np.array - cost matrix
    return: tuple - (min_cost, tour)
    '''
    n = c.shape[0]
    model = Model("tsp")
    x = {(i, j): model.addVar(vtype="B") for i in range(n) for j in range(n) if i != j}
    u = [model.addVar(vtype="C") for i in range(n)]
    # add objective function
    model.setObjective(qsum(c[i, j]*x[i, j] for i in range(n) for j in range(n) if i != j), "minimize")
    # add constraints
    for i in range(n):
        model.addCons(qsum(x[i, j] for j in range(n) if i != j) == 1)
        model.addCons(qsum(x[j, i] for j in range(n) if i != j) == 1)
    for i in range(n):
        for j in range(1, n):
            if i != j:
                model.addCons(u[i] - u[j] + n*x[i, j] <= n-1)
    # remove verbose
    # model.hideOutput()
    # optimize
    model.optimize()
    min_cost = model.getObjVal()
    u_val = [model.getVal(u[i]) for i in range(n)]
    print(u_val)
    tour = np.argsort(u_val)
    # print running time
    print("Running time: ", model.getSolvingTime())
    return min_cost, tour


def tsp_subtour(c: np.array, use_lazy: bool = False) -> tuple:
    '''
    c: np.array - cost matrix
    use_lazy: bool - if True, use subtour elimination constraints as lazy constraints
    return: tuple - (min_cost, tour)
    '''
    n = c.shape[0]
    model = Model("tsp")
    x = {(i, j): model.addVar(vtype="B") for i in range(n) for j in range(n) if i != j}
    # add objective function
    model.setObjective(qsum(c[i, j]*x[i, j] for i in range(n) for j in range(n) if i != j), "minimize")
    # add constraints
    for i in range(n):
        model.addCons(qsum(x[i, j] for j in range(n) if i != j) == 1)
        model.addCons(qsum(x[j, i] for j in range(n) if i != j) == 1)

    if use_lazy:
        pass # TODO: add callback to add subtour elimination constraints as lazy constraints in SCIP
    else:
        # All possible subsets of nodes of size 2 to n-1 as Python generator
        S = (s for k in range(2, n) for s in comb(range(n), k))
        # Add subtour elimination constraints
        for s in S:
            model.addCons(qsum(x[i, j] for i, j in product(s, s) if i != j) <= len(s)-1)
    # remove verbose
    # model.hideOutput()
    # optimize
    model.optimize()
    min_cost = model.getObjVal()
    tour = [0]
    while True:
        nxt = next(i for i in range(n) if tour[-1] != i and model.getVal(x[tour[-1], i]) > 0.5)
        if nxt == 0:
            break
        tour.append(nxt)

    # print running time
    print("Running time: ", model.getSolvingTime())
    # print number of constraints
    print("Number of constraints: ", model.getNConss())
    return min_cost, tour


def plot_tour(points: np.array, tour: np.array):
    '''
    points: np.array - list of points
    tour: np.array - list of tour
    '''
    n = points.shape[0]
    # add first point to the end
    tour = np.append(tour, tour[0])
    # create axis
    fig, ax = plt.subplots()
    # plot tour
    ax.plot(points[tour, 0], points[tour, 1], color='#202020', linestyle='-', linewidth=1)
    # plot points
    ax.plot(points[:, 0], points[:, 1], 'o', color='#624d6b', markersize=13, markeredgewidth=1, markeredgecolor='#202020')
    for i in range(n):
        ax.annotate(str(i), (points[i, 0], points[i, 1]), color='white', weight='bold', fontsize=8, ha='center', va='center')
    plt.show()


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


if __name__ == "__main__":
    points, c = make_random_instance(10)
    # min_cost, tour = tsp_mtz(c)
    min_cost, tour = tsp_subtour(c, use_lazy=False)

    print("Min Cost:", min_cost)

    # plot tour
    plot_tour(points, tour)
