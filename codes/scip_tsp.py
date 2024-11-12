from pyscipopt import Model, SCIP_EVENTTYPE, SCIP_RESULT, Conshdlr, SCIP_PRESOLTIMING, SCIP_PROPTIMING
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


def tsp_all_subtours(c: np.array) -> tuple:
    '''
    solve TSP with all subtours elimination constraints (exponential number of constraints)
    c: np.array - cost matrix
    return: tuple - (min_cost, tour)
    '''
    n = c.shape[0]
    model = Model("tsp")
    x = {(i, j): model.addVar(vtype="M", lb=0, ub=1) for i in range(n) for j in range(n) if i != j}
    # add objective function
    model.setObjective(qsum(c[i, j]*x[i, j] for i in range(n) for j in range(n) if i != j), "minimize")
    # add constraints
    for i in range(n):
        model.addCons(qsum(x[i, j] for j in range(n) if i != j) == 1)
        model.addCons(qsum(x[j, i] for j in range(n) if i != j) == 1)

        # All possible subsets of nodes of size 2 to n-1 as Python generator
    S = (s for k in range(2, n//2) for s in comb(range(n), k))
    # Add subtour elimination constraints
    for s in S:
        model.addCons(qsum(x[i, j] for i in s for j in s if i != j) <= len(s) - 1)
    # remove verbose
    model.hideOutput()
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


def tsp_adhoc_subtours(c: np.array) -> tuple:
    '''
    solve TSP with ad-hoc subtours elimination constraints
    c: np.array - cost matrix
    return: tuple - (min_cost, tour)
    '''
    n = c.shape[0]
    model = Model("tsp")
    x = {(i, j): model.addVar(vtype="B") for i in range(n) for j in range(n) if i != j}
    # add objective function
    model.setObjective(qsum(c[i, j]*x[i, j] for i in range(n) for j in range(n) if i != j), "minimize")
    # add constraints (degree constraints)
    for i in range(n):
        model.addCons(qsum(x[i, j] for j in range(n) if i != j) == 1)
        model.addCons(qsum(x[j, i] for j in range(n) if i != j) == 1)
    # remove verbose
    model.hideOutput()
    run_time = 0
    while True:
        model.optimize()
        run_time += model.getSolvingTime()
        tour = [0]
        while True:
            nxt = next(i for i in range(n) if tour[-1] != i and model.getVal(x[tour[-1], i]) > 0.5)
            if nxt == 0:
                break
            tour.append(nxt)
        if len(tour) == n:
            break
        print("Subtour found:", tour)
        # reset model
        model.freeTransform()
        # add subtour elimination constraint
        model.addCons(qsum(x[i, j] for i in range(n) for j in range(n) if i != j and (i in tour) and (j in tour)) <= len(tour) - 1)
    min_cost = model.getObjVal()
    # print running time
    print("Running time: ", run_time)
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
    points, c = make_random_instance(25)
    # min_cost, tour = tsp_mtz(c)
    # min_cost, tour = tsp_all_subtours(c)
    min_cost, tour = tsp_adhoc_subtours(c)
    print("Min Cost:", min_cost)

    # plot tour
    plot_tour(points, tour)
