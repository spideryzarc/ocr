import numpy as np

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





def greedy(sets: list,partial:list =None) -> tuple:
    '''
    sets: list - list of subsets of {0,1,...,n-1}
    return: list - selected sets indices
    '''
    # n_sets = len(sets)
    # print("Number of sets:", n_sets)
    # # remove empty sets
    # sets = [s for s in sets if s]
    # # remove dominated sets
    # sets = [s for i, s in enumerate(sets) if not any(s < sets[j] for j in range(len(sets)) if i != j)]
    n_sets = len(sets)
    # print("Number of sets after removing dominated sets:", n_sets)
    itens = set.union(*sets)
    selected_sets = []
    if partial:
        itens -= set.union(*partial)
        selected_sets = partial
    itens_count = {i: sum(1 for j in sets if i in j) for i in itens}
    scores = [sum(1/itens_count[i] for i in (s & itens)) for s in sets]
    while itens:
        best_set = np.argmax(scores)
        selected_sets.append(sets[best_set])
        itens -= sets[best_set]
        scores = [sum(1/itens_count[i] for i in (s & itens)) for s in sets]
    return selected_sets

def greedy_randomized(sets: list) -> tuple:
    '''
    sets: list - list of subsets of {0,1,...,n-1}
    return: list - selected sets indices
    '''
    def select(scores: list) -> int:
        idx = np.argsort(scores)[-2:]
        weights = np.array([scores[i] for i in idx])
        return np.random.choice(idx, p=weights/sum(weights))
    
    n_sets = len(sets)
    itens = set.union(*sets)
    selected_sets = []
    itens_count = {i: sum(1 for j in sets if i in j) for i in itens}
    scores = [sum(1/itens_count[i] for i in s) for s in sets]
    while itens:
        best_set = select(scores)
        selected_sets.append(sets[best_set])
        itens -= sets[best_set]
        scores = [sum(1/itens_count[i] for i in (s & itens)) for s in sets]
    return selected_sets

def LNS(sets: list, solution:list, max_iter: int = 20, k:int=3) -> list:
    '''
    sets: list - list of subsets of {0,1,...,n-1}
    max_iter: int - maximum number of iterations
    solution: list - initial solution
    return: list - selected sets indices
    '''
    best_solution = solution
    best_cost = len(solution)
    for _ in range(max_iter):
        # remove k sets from the solution
        np.random.shuffle(best_solution)
        partial = best_solution[k:]
        partial = greedy(sets,partial)
        cost = len(partial)
        if cost < best_cost:
            best_cost = cost
            best_solution = partial
            print("LNS:", best_cost)
    return best_solution

def grasp(sets: list, max_iter: int = 10) -> list:
    '''
    sets: list - list of subsets of {0,1,...,n-1}
    max_iter: int - maximum number of iterations
    return: list - selected sets indices
    '''
    best_solution = []
    best_cost = float('inf')
    for _ in range(max_iter):
        solution = greedy_randomized(sets)
        solution = LNS(sets, solution)
        cost = len(solution)
        if cost < best_cost:
            best_cost = cost
            best_solution = solution
            print("Best Cost:", best_cost)
    return best_solution


if __name__ == "__main__":
    n, sets, costs = make_random_instance(itens=500, n_sets=500,max_item_repetitions=1000)
    # print("Sets:", sets)
    # print("Costs:", costs)
    columns = grasp(sets)
    print("grasp:", len(columns))
    columns = greedy(sets)
    print("greedy:", len(columns))
    # print("Selected Sets:", columns)
    from scip_setcovering import set_covering
    min_cost, columns = set_covering(n, sets, costs=[1]*len(sets))
    print("Min Cost:", min_cost)
    # print("Sets:", columns)
    