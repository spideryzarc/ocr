from scip_tsp import make_random_instance, plot_tour, tsp_adhoc_subtours
import numpy as np

def nearest_neighbor(c:np.ndarray)->list:
    ''' find a tour using the nearest neighbor heuristic
    c: cost matrix
    return: a list with the tour
    '''
    n = len(c) # number of cities
    unvisited = set(range(1,n)) # set of unvisited cities (all except 0)
    tour = [0] # start at city 0
    current = 0 # current city
    while unvisited:
        # witch unvisited city is the nearest?
        next = min(unvisited, key=lambda j: c[current,j])
        unvisited.remove(next) # remove from unvisited set
        tour.append(next) # add to the tour
        current = next # move to the next city
    # tour.append(0)
    return tour

def best_insertion(c:np.ndarray, ins_order:list,points:list=None)->list:
    ''' find a tour using the best insertion heuristic, with a given order of the cities
    c: cost matrix
    ins_order: order of the cities to be inserted
    points: coordinates of the cities (for plotting only)
    return: a list with the tour
    '''
    n = len(c) # number of cities
    if n < len(ins_order):
        raise ValueError("The number of cities is less than the number of cities to be inserted")
    if len(ins_order) <= 3:
        return ins_order # trivial case
    tour = ins_order[:3] # start with the first 3 cities
    if points: 
        plot_tour(points, tour)
    for i in ins_order[3:]: # insert the remaining cities
        # find the best place to insert city i
        min_cost = np.inf
        for j in range(1, len(tour)):
            # cost of inserting i between j-1 and j
            cost = c[tour[j-1],i] + c[i,tour[j]] - c[tour[j-1],tour[j]]
            if cost < min_cost:
                min_cost = cost
                min_idx = j
                
        if c[tour[-1],i] + c[i,tour[0]] - c[tour[-1],tour[0]] < min_cost:
            # better to insert at the end
            tour.append(i)
        else:
            tour.insert(min_idx, i)
        if points:
            plot_tour(points, tour)
    return tour
    
def cost(c:np.ndarray, tour:list)->float:
    ''' calculate the cost of a tour
    c: cost matrix
    tour: list with the tour
    return: the cost of the tour
    '''
    return c[tour[:-1],tour[1:]].sum() + c[tour[-1],tour[0]]

def furthest_order(c:np.ndarray)->list:
    ''' find an order of the cities based on the furthest neighbor heuristic, 
    where the first two cities are the furthest apart, the third city is the one 
    that is furthest from the first two, and so on.
    c: cost matrix
    return: a list with the order of the cities
    '''
    n = len(c) # number of cities
    i,j = np.unravel_index(c.argmax(), c.shape) # find the furthest pair
    order = [i,j] # start with the furthest pair
    dist = np.minimum(c[i], c[j]) # dist[i] is the distance from i to the nearest city in the tour
    dist[i] = dist[j] = -1 # sinalize that i and j are already in the tour
    for _ in range(n-2): # add the remaining cities
        k = np.argmax(dist) # find the furthest city 
        order.append(k) # add to the tour
        dist = np.minimum(dist, c[k]) # update the distances
        dist[k] = -1 # sinalize that k is already in the tour
    return order

def or_opt(c:np.ndarray, tour:list)->bool:
    ''' search for a improving move in the tour using or-opt, returning True at the first improving move found
    c: cost matrix
    tour: current tour to be improved, will be modified in place
    return: True if an improving move is found, False otherwise
    '''
    n = len(c) # number of cities
    if __debug__: custo_ini = cost(c, tour) # initial cost for debug only
    for i in range(n): # try to move each city
        ant_i = i-1 # index of the city before i
        post_i = i+1 if i < n-1 else 0 # index of the city after i
        # calculate the cost of removing i 
        rem_delta =  c[tour[ant_i],tour[post_i]] \
                    -c[tour[ant_i],tour[i]] - c[tour[i],tour[post_i]]
        for j in range(n): # try to insert i in each position 
            if j in (i, post_i): continue # skip i, i-1 and i+1 
            ant_j = j-1 # index of the city before j
            # calculate the cost of adding i in position j
            add_delta = -c[tour[ant_j],tour[j]] \
                        +c[tour[ant_j],tour[i]] + c[tour[i],tour[j]]
            if add_delta + rem_delta < -1e-6: # if the move is improving
                if i < j:
                    # first remove i, then insert it in position j
                    tour.insert(j, tour[i])
                    tour.pop(i)
                else:
                    # first insert i in position j, then remove the original i
                    vi = tour.pop(i)
                    tour.insert(j, vi)
                if __debug__: 
                    print("OR-opt move:", tour[i], tour[j])
                    delta = cost(c, tour) - custo_ini # for debug only
                    if not np.isclose(delta, add_delta + rem_delta):
                        raise ValueError("OR-opt inconsistency")
                return True 
    return False

def two_opt(c:np.ndarray, tour:list)->bool:
    ''' search for a improving move in the tour using 2-opt, returning True at the first improving move found
    c: cost matrix
    tour: current tour to be improved, will be modified in place
    return: True if an improving move is found, False otherwise
    '''
    n = len(c) # number of cities
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
                    

def VND(c:np.ndarray, tour:list, points:list = None)->None:
    ''' perform a Variable Neighborhood Descent in the tour to improve it 
    c: cost matrix
    tour: current tour to be improved, will be modified in place
    points: coordinates of the points (for plotting only)
    '''
    # define the neighborhoods
    neighborhoods = [two_opt, or_opt]
    while True:
        for neighborhood in neighborhoods:
            if neighborhood(c, tour):
                if points: # plot the tour if points are given
                    plot_tour(points, tour)
                if __debug__: # print the cost for debug only
                    print("VND, ", neighborhood.__name__, cost(c, tour))
                break # go back to the first neighborhood
        else: # if no improving move was found in any neighborhood
            break # stop the search
        

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