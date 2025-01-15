from scip_tsp import make_random_instance, plot_tour, tsp_adhoc_subtours
import numpy as np

def nearest_neighbor(c:np.array)->list:
    n = len(c)
    unvisited = set(range(1,n))
    tour = [0]
    current = 0
    while unvisited:
        next = min(unvisited, key=lambda j: c[current,j])
        unvisited.remove(next)
        tour.append(next)
        current = next
    # tour.append(0)
    return tour

def best_insertion(c:np.array, ins_order:list,points)->list:
    n = len(c)
    assert n >= 3 and len(ins_order) == n, "Invalid input"
    tour = ins_order[:3]
    # plot_tour(points, tour)
    for i in ins_order[3:]:
        min_cost = np.inf
        for j in range(1, len(tour)):
            cost = c[tour[j-1],i] + c[i,tour[j]] - c[tour[j-1],tour[j]]
            if cost < min_cost:
                min_cost = cost
                min_idx = j
        if c[tour[-1],i] + c[i,tour[0]] - c[tour[-1],tour[0]] < min_cost:
            tour.append(i)
        else:
            tour.insert(min_idx, i)
        # plot_tour(points, tour) 
    return tour
    
def cost(c:np.array, tour:list)->float:
    return c[tour[:-1],tour[1:]].sum() + c[tour[-1],tour[0]]

def furthest_order(c:np.array)->list:
    n = len(c)
    #find i,j such that c[i,j] is maximum
    # i,j = np.unravel_index(c.argmax(), c.shape)
    i,j = max(((i,j) for i in range(n) for j in range(n) if i != j), key=lambda x: c[x])
    order = [i,j]
    dist = np.minimum(c[i], c[j])
    dist[i] = dist[j] = -1
    for _ in range(n-2):
        k = np.argmax(dist)
        order.append(k)
        dist = np.minimum(dist, c[k])
        dist[k] = -1
    return order

def or_opt(c:np.array, tour:list)->bool:
    ''' search for a improving move in the tour using or-opt
    c: cost matrix
    tour: current tour to be improved, will be modified in place
    return: True if an improving move is found, False otherwise
    '''
    n = len(c)
    if __debug__: custo_ini = cost(c, tour) # initial cost for debug only
    for i in range(n):
        ant_i = i-1
        post_i = i+1 if i < n-1 else 0
        rem_delta =  c[tour[ant_i],tour[post_i]] \
                    -c[tour[ant_i],tour[i]] - c[tour[i],tour[post_i]]
        for j in range(n):
            if j in (i, post_i): continue # skip i, i-1 and i+1 
            ant_j = j-1
            add_delta = -c[tour[ant_j],tour[j]] \
                        +c[tour[ant_j],tour[i]] + c[tour[i],tour[j]]
            if add_delta + rem_delta < -1e-6:
                if i < j:
                    tour.insert(j, tour[i])
                    tour.pop(i)
                else:
                    vi = tour.pop(i)
                    tour.insert(j, vi)
    
                if __debug__: 
                    print("OR-opt move:", tour[i], tour[j])
                    delta = cost(c, tour) - custo_ini # for debug only
                    if not np.isclose(delta, add_delta + rem_delta):
                        raise ValueError("OR-opt move error")
                return True
    return False

def two_opt(c:np.array, tour:list)->bool:
    ''' search for a improving move in the tour using 2-opt
    c: cost matrix
    tour: current tour to be improved, will be modified in place
    return: True if an improving move is found, False otherwise
    '''
    n = len(c)
    if __debug__: custo_ini = cost(c, tour) # initial cost for debug only
    for i in range(n):
        for j in range(i+2, n-(i==0)): # i+2 to avoid adjacent edges and n-1 if i==0
            delta = c[tour[i],tour[j]] + c[tour[i+1],tour[(j+1)%n]] \
                    -c[tour[i],tour[i+1]] - c[tour[j],tour[(j+1)%n]]
            if delta < -1e-6:
                if j == n-1:
                    tour[i+1:] = tour[i+1:][::-1]
                    print('opa')
                else:
                    tour[i+1:j+1] = tour[j:i:-1]
                if __debug__: 
                    print("2-opt move:", i, j)
                    delta_real = cost(c, tour) - custo_ini # for debug only
                    if not np.isclose(delta, delta_real):
                        raise ValueError("2-opt move error")
                return True
    return False
                    

def VND(c:np.array, tour:list, points)->None:
    ''' perform a VND in the tour
    c: cost matrix
    tour: current tour to be improved, will be modified in place
    points: coordinates of the points
    '''
    while True:
        if two_opt(c, tour):
            continue
        if or_opt(c, tour):
            continue
        break

if __name__ == "__main__":
    np.random.seed(42)
    points, c = make_random_instance(100)
   
    nn_tour = nearest_neighbor(c)
    print ("NN Tour Cost:", cost(c, nn_tour))
    plot_tour(points, nn_tour)
    VND(c, nn_tour, points)
    print ("NN Tour Cost:", cost(c, nn_tour))
    plot_tour(points, nn_tour)
    
    
    # order  = furthest_order(c)
    # futher_tour = best_insertion(c, order, points)
    # print("Furthest Order Cost:", cost(c, futher_tour))
    # plot_tour(points, futher_tour)
    
    # best_cost = cost(c, nn_tour)
    # best_tour = nn_tour
    # for _ in range(100):
    #     np.random.shuffle(order)
    #     bi_tour = best_insertion(c, order, points)
    #     a = cost(c, bi_tour)
    #     if a < best_cost:
    #         best_cost = a
    #         best_tour = bi_tour
    #         print("BI Tour Cost:", a)
    # plot_tour(points, bi_tour)
            
    
    # opt_cost, opt_tour = tsp_adhoc_subtours(c, plot=False, points=points)
    # print("Optimal Cost:", opt_cost)
    # plot_tour(points, opt_tour)