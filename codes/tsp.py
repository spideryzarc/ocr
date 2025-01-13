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
    

if __name__ == "__main__":
    points, c = make_random_instance(100)
   
    nn_tour = nearest_neighbor(c)
    print ("NN Tour Cost:", cost(c, nn_tour))
    plot_tour(points, nn_tour)
    
    order  = furthest_order(c)
    futher_tour = best_insertion(c, order, points)
    print("Furthest Order Cost:", cost(c, futher_tour))
    plot_tour(points, futher_tour)
    
    best = cost(c, nn_tour)
    for _ in range(100):
        np.random.shuffle(order)
        bi_tour = best_insertion(c, order, points)
        a = cost(c, bi_tour)
        if a < best:
            best = a
            print("BI Tour Cost:", a)
            plot_tour(points, bi_tour)
            
    
    opt_cost, opt_tour = tsp_adhoc_subtours(c, plot=False, points=points)
    print("Optimal Cost:", opt_cost)
    plot_tour(points, opt_tour)