import numpy as np


def first_fit(w: np.array, C: int, sort_dec: bool = True) -> tuple:
    '''
    w: np.array - list of weights of each item
    C: int - capacity of each bin
    sort_dec: bool - sort the weights in decreasing order
    return: tuple - (min_bins, bin_assignment)
    '''
    n = len(w)
    # sort the weights in decreasing order
    if sort_dec:
        w = np.sort(w)[::-1]
    bins = [[]]
    loads = [0]
    for w_i in w:
        for j in range(len(bins)):
            if loads[j] + w_i <= C:
                bins[j].append(w_i)
                loads[j] += w_i
                break
        else:
            bins.append([w_i])
            loads.append(w_i)
    return loads, bins


def next_fit(w: np.array, C: int) -> tuple:
    '''
    w: np.array - list of weights of each item
    C: int - capacity of each bin
    return: tuple - (min_bins, bin_assignment)
    '''
    n = len(w)
    bins = [[]]
    loads = [0]
    for w_i in w:
        if loads[-1] + w_i <= C:
            bins[-1].append(w_i)
            loads[-1] += w_i
        else:
            bins.append([w_i])
            loads.append(w_i)
    return loads, bins


def best_fit(w: np.array, C: int, sort_dec: bool = True) -> tuple:
    '''
    w: np.array - list of weights of each item
    C: int - capacity of each bin
    sort_dec: bool - sort the weights in decreasing order
    return: tuple - (min_bins, bin_assignment)
    '''
    n = len(w)
    # sort the weights in decreasing order
    if sort_dec:
        w = np.sort(w)[::-1]
    bins = [[]]
    loads = [0]
    for w_i in w:
        best_j = -1
        best_load = 0
        for j in range(len(bins)):
            if loads[j] + w_i <= C and loads[j] + w_i > best_load:
                best_j = j
                best_load = loads[j] + w_i
        if best_j != -1:
            bins[best_j].append(w_i)
            loads[best_j] += w_i
        else:
            bins.append([w_i])
            loads.append(w_i)
    return loads, bins


def worst_fit(w: np.array, C: int, sort_dec: bool = True) -> tuple:
    '''
    w: np.array - list of weights of each item
    C: int - capacity of each bin
    sort_dec: bool - sort the weights in decreasing order
    return: tuple - (min_bins, bin_assignment)
    '''
    n = len(w)
    # sort the weights in decreasing order
    if sort_dec:
        w = np.sort(w)[::-1]
    bins = [[]]
    loads = [0]
    for w_i in w:
        worst_j = -1
        worst_load = np.inf
        for j in range(len(bins)):
            if loads[j] + w_i <= C and loads[j] + w_i < worst_load:
                worst_j = j
                worst_load = loads[j] + w_i
        if worst_j != -1:
            bins[worst_j].append(w_i)
            loads[worst_j] += w_i
        else:
            bins.append([w_i])
            loads.append(w_i)
    return loads, bins


def local_search(w: np.array, C: int, sol: list, lb: int = 0) -> tuple:
    ''' try to improve the solution by local search. The solution is flattened and the items are swapped, best_fit is used to decode the permutation to bins.
    w: np.array - list of weights of each item
    C: int - capacity of each bin
    sol: list of list - bin assignment
    lb: int - lower bound of the number of bins
    return: tuple - (min_bins, bin_assignment)
    '''
    itens = np.concatenate(sol)  # flatten the solution
    n_bins = len(sol)  # number of bins
    loads = [np.sum(bin) for bin in sol]  # loads of each bin
    sq_sum = np.sum(np.square(loads))  # sum of the square of the loads
    imp = True  # flag to indicate if the solution was improved
    # map each item to its bin
    bin_map = np.empty(len(itens), dtype=int)
    j = 0
    for i, bin in enumerate(sol):
        bin_map[j:j+len(bin)] = i
        j = i + len(bin)
    while imp:  # while the solution is improved
        imp = False
        for i in range(len(itens)-1,-1,-1):
            if imp:
                break
            for j in range(i+1, len(itens)):
                # skip if the items are in the same bin or are the same item (weights are equal)
                if bin_map[i] == bin_map[j] or itens[i] == itens[j]:
                    continue
                itens[i], itens[j] = itens[j], itens[i]  # swap
                # decode permutation to bins using best_fit
                loads, bins = best_fit(itens, C, sort_dec=False)
                # loads, bins = first_fit(itens, C, sort_dec=False)
                # loads, bins = worst_fit(itens, C, sort_dec=False)
                # loads, bins = next_fit(itens, C)
                new_n_bins = len(loads)  # number of bins
                if new_n_bins <= n_bins:  # first criteria to accept the new solution
                    new_sq_sum = np.sum(np.square(loads))  # sum of the square of the loads
                    if new_n_bins < n_bins or new_sq_sum > sq_sum:  # second criteria to accept the new solution
                        imp = True
                        # update the solution
                        n_bins = new_n_bins
                        sq_sum = new_sq_sum
                        sol = bins
                        # update flatten solution
                        itens = np.concatenate(sol)
                        # update map
                        k = 0
                        for l, bin in enumerate(sol):
                            bin_map[k:k+len(bin)] = l
                            k = l + len(bin)
                        print('new solution:', n_bins, sq_sum)
                        # print([int(l) for l in loads])
                        if n_bins == lb:
                            return sol
                        break # break j loop
                    else:
                        itens[i], itens[j] = itens[j], itens[i]  # swap back
                else:
                    itens[i], itens[j] = itens[j], itens[i]  # swap back

    return sol


if __name__ == "__main__":
    # np.random.seed(7)
    n = 200
    m = n
    C = 100
    while True:
        w = np.random.randint(1, 2*C//3, n)
        # print('input:', w)
        _, sol = best_fit(w, C)

        lb = int(np.ceil(np.sum(w)/C))
        if len(sol) > lb:
            print('best_fit_dec:', len(sol), lb)
            local_search(w, C, sol, lb)
            break
