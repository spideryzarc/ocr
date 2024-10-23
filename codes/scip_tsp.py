from pyscipopt import Model 
from pyscipopt import quicksum as qsum
import numpy as np
import matplotlib.pyplot as plt

def tsp_mtz(c:np.array)->tuple:
    '''
    c: np.array - cost matrix
    return: tuple - (min_cost, tour)
    '''
    n = c.shape[0]
    model = Model("tsp")
    x = {(i,j):model.addVar(vtype="B") for i in range(n) for j in range(n)}
    u = [model.addVar(vtype="C") for i in range(n)]
    # add objective function
    model.setObjective(qsum(c[i,j]*x[i,j] for i in range(n) for j in range(n)), "minimize")
    # add constraints
    for i in range(n):
        model.addCons(qsum(x[i,j] for j in range(n) if i!=j ) == 1)
        model.addCons(qsum(x[j,i] for j in range(n) if i!=j ) == 1)
    for i in range(n):
        for j in range(1,n):
            if i != j:
                model.addCons(u[i] - u[j] + n*x[i,j] <= n-1)
    # remove verbose
    # model.hideOutput()
    # optimize
    model.optimize()
    min_cost = model.getObjVal()
    u_val = [model.getVal(u[i]) for i in range(n)]
    print(u_val)
    tour = np.argsort(u_val)
    return min_cost, tour

if __name__ == "__main__":
    n = 30
    # list of random points
    points = np.random.rand(n,2)
    # cost matrix
    c = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            c[i,j] = np.linalg.norm(points[i] - points[j])
    min_cost, tour = tsp_mtz(c) 
    print("Min Cost:",min_cost)
    
    # plot tour
    fig, ax = plt.subplots()
    ax.plot(points[:,0],points[:,1],'o')
    for i in range(n):
        ax.text(points[i,0],points[i,1],str(i))
    for i in range(n):
        ax.plot([points[tour[i],0],points[tour[(i+1)%n],0]],[points[tour[i],1],points[tour[(i+1)%n],1]],'r')
    plt.show()

    
    