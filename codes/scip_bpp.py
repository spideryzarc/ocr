from pyscipopt import Model
from pyscipopt import quicksum as qsum
import numpy as np


def bpp(n: int, m: int, w: np.array, C: int) -> tuple:
    '''
    n: int - number of items
    m: int - number of bins
    w: list - list of weights of each item
    C: int - capacity of each bin
    return: tuple - (min_bins, bin_assignment)
    '''
    model = Model("bpp")
    x = {(i, j): model.addVar(vtype="B") for i in range(n) for j in range(m)}
    y = [model.addVar(vtype="B") for j in range(m)]
    # add objective function
    model.setObjective(qsum(y), "minimize")
    # add constraints
    for i in range(n):
        model.addCons(qsum(x[i, j] for j in range(m)) == 1)
    for j in range(m):
        model.addCons(qsum(w[i]*x[i, j] for i in range(n)) <= C*y[j])
    # remove verbose
    model.hideOutput()
    # optimize
    model.optimize()
    min_bins = model.getObjVal()
    bin_assignment = np.array([next(j for j in range(m) if model.getVal(x[i, j]) > 0.5) for i in range(n)])
    return min_bins, bin_assignment


if __name__ == "__main__":
    n = 20
    m = n
    C = 100
    w = np.random.randint(1, 2*C//3, n)
    print("Weights:", w)
    min_bins, bin_assignment = bpp(n, m, w, C)
    print("Min Bins:", min_bins)
    print("Bin Assignment:", bin_assignment)
    print("Bins load:", np.bincount(bin_assignment, weights=w))
    print("Bins list:", {int(i): list(filter(lambda x: bin_assignment[x] == i, range(n))) for i in np.unique(bin_assignment)})
