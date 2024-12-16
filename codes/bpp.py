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
    

def next_fit(w:np.array, C:int) -> tuple:
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

def best_fit_dec(w:np.array, C:int, sort:bool =True) -> tuple:
    '''
    w: np.array - list of weights of each item
    C: int - capacity of each bin
    sort: bool - sort the weights in decreasing order
    return: tuple - (min_bins, bin_assignment)
    '''
    n = len(w)
    #sort the weights in decreasing order
    if sort:
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


def local_search(w:np.array, C:int,sol:list) -> tuple:
    '''
    w: np.array - list of weights of each item
    C: int - capacity of each bin
    sol: list of list - bin assignment
    return: tuple - (min_bins, bin_assignment)
    '''
    itens = np.concatenate(sol)
    n_bins = len(sol)
    loads = [np.sum(bin) for bin in sol]
    sq_sum = np.sum(np.square(loads))
    imp = True
    while imp:
        imp = False
        for i in range(1,len(itens)):
            for j in range(i):
                itens[i], itens[j] = itens[j], itens[i] #swap
                loads, bins = best_fit_dec(itens, C,False)
                new_n_bins = len(loads)
                if new_n_bins <= n_bins:
                    new_sq_sum = np.sum(np.square(loads))
                    if new_n_bins < n_bins or new_sq_sum > sq_sum:
                        n_bins = new_n_bins
                        sq_sum = new_sq_sum
                        sol = bins
                        imp = True
                        print('new solution:', n_bins, sq_sum)
                    else:
                        itens[i], itens[j] = itens[j], itens[i] #swap back
                else:
                    itens[i], itens[j] = itens[j], itens[i] #swap back
                    
    return sol      
                
    

if __name__ == "__main__":
    # np.random.seed(7)
    n = 200
    m = n
    C = 100
    while True:
        w = np.random.randint(1, 2*C//3, n)
        # print('input:', w)
        _, sol = best_fit_dec(w, C)
        
        lb = int(np.ceil(np.sum(w)/C))
        if len(sol) > lb:  
            print('best_fit_dec:', len(sol), lb)
            local_search(w, C,sol) #[[i] for i in w])
            break