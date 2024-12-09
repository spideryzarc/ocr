import numpy as np

def first_fit_dec(w:np.array, C:int) -> tuple:
    '''
    w: np.array - list of weights of each item
    C: int - capacity of each bin
    return: tuple - (min_bins, bin_assignment)
    '''
    n = len(w)
    #sort the weights in decreasing order
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
    return len(loads), loads, bins
    

def next_fit(w:np.array, C:int, order_idx:list = None) -> tuple:
    '''
    w: np.array - list of weights of each item
    C: int - capacity of each bin
    return: tuple - (min_bins, bin_assignment)
    '''
    n = len(w)
    bins = [[]]
    loads = [0]
    if order_idx is None:
        order_idx = range(n)
    for i in order_idx:
        w_i = w[i]
        if loads[-1] + w_i <= C:
            bins[-1].append(w_i)
            loads[-1] += w_i
        else:
            bins.append([w_i])
            loads.append(w_i)
    return len(loads), loads, bins

def best_fit_dec(w:np.array, C:int) -> tuple:
    '''
    w: np.array - list of weights of each item
    C: int - capacity of each bin
    return: tuple - (min_bins, bin_assignment)
    '''
    n = len(w)
    #sort the weights in decreasing order
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
    return len(loads), loads, bins

def worst_fit_dec(w:np.array, C:int) -> tuple:
    '''
    w: np.array - list of weights of each item
    C: int - capacity of each bin
    return: tuple - (min_bins, bin_assignment)
    '''
    n = len(w)
    #sort the weights in decreasing order
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
    return len(loads), loads, bins


if __name__ == "__main__":
    n = 5000
    m = n
    C = 100
    w = np.random.randint(1, 2*C//3, n)
    # print("Weights:", w)
    print(first_fit_dec(w, C)[0])
    
    order_idx = np.argsort(w)[::-1]
    print (next_fit(w, C, order_idx)[0])
    # best = np.inf
    # for _ in range(100000):
    #     sol = next_fit(w, C,np.random.permutation(n))
    #     if sol[0] < best:
    #         best = sol[0]
    #         print(sol[0])
    print(best_fit_dec(w, C)[0])
    print(worst_fit_dec(w, C)[0])