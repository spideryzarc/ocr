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


def greedy(sets: list) -> tuple:
    '''
    sets: list - list of subsets of {0,1,...,n-1}
    return: list - selected sets indices
    '''
    n_sets = len(sets)
    itens = set.union(*sets)
    selected_sets = []
    itens_count = {i: sum(1 for j in sets if i in j) for i in itens}
    scores = [sum(1/itens_count[i] for i in s) for s in sets]
    while itens:
        best_set = np.argmax(scores)
        selected_sets.append(sets[best_set])
        itens -= sets[best_set]
        scores = [sum(1/itens_count[i] for i in (s & itens)) for s in sets]
    return selected_sets

if __name__ == "__main__":
    n, sets, costs = make_random_instance(itens=500, n_sets=1000,max_item_repetitions=1000)
    # print("Sets:", sets)
    # print("Costs:", costs)
    columns = greedy(sets)
    print("Selected:", len(columns))
    # print("Selected Sets:", columns)
    from scip_setcovering import set_covering
    min_cost, columns = set_covering(n, sets, costs=[1]*len(sets))
    print("Min Cost:", min_cost)
    # print("Sets:", columns)
    