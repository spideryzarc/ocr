from pyscipopt import Model
from pyscipopt import quicksum as qsum
import numpy as np


def set_covering(n: int, sets: list, costs: list = None) -> tuple:
    '''
    n: int - number of columns
    sets: list - list of subsets of {0,1,...,n-1}
    costs: list - list of set costs (optional)
    return: tuple - (min_cost, selected sets indices)
    '''
    model = Model("set_covering")
    x = {j: model.addVar(vtype="B") for j in range(len(sets))}
    # add objective function
    if costs is not None:
        model.setObjective(qsum(costs[j]*x[j] for j in x.keys()), "minimize")
    else:
        model.setObjective(qsum(x.values()), "minimize")
    # add constraints
    for i in range(n):
        model.addCons(qsum(x[j] for j in x.keys() if i in sets[j]) >= 1)
    # remove verbose
    model.hideOutput()
    # optimize
    model.optimize()
    if model.getStatus() != "optimal":
        print("No solution found.")
        return None, None
    min_cost = model.getObjVal()
    selected_sets = [j for j in x.keys() if model.getVal(x[j]) > 0.5]
    return min_cost, selected_sets


def make_random_instance(itens: int = 10, n_sets: int = 5, min_item_repetitions: int = 1, max_item_repetitions: int = 3) -> tuple:
    '''
    itens: int - number of itens
    n_sets: int - number of sets
    min_item_repetitions: int - minimum number of itens in each set
    max_item_repetitions: int - maximum number of itens in each set
    return: tuple - (n, sets, costs)
    '''
    n = itens
    sets = [set() for _ in range(n_sets)]
    for i in range(itens):
        set_idx = np.random.randint(n_sets, size=np.random.randint(min_item_repetitions, max_item_repetitions+1))
        for j in set_idx:
            sets[j].add(i)
    costs = np.random.randint(1, 10, size=n_sets)
    return n, sets, costs


if __name__ == "__main__":
    n, sets, costs = make_random_instance(itens=50, n_sets=20)
    print("Sets:", sets)
    min_cost, columns = set_covering(n, sets, costs=costs)
    print("Min Cost:", min_cost)
    print("Sets:", columns)
