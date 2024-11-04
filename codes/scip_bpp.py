from pyscipopt import Model 
from pyscipopt import quicksum as qsum

def bpp(n:int,m:int,w:list,W:list)->tuple:
    '''
    n: int - number of items
    m: int - number of bins
    w: list - list of weights of each item
    W: list - capacity of each bin
    return: tuple - (min_bins, bin_assignment)
    '''
    model = Model("bpp")
    x = {(i,j):model.addVar(vtype="B") for i in range(n) for j in range(m)}
    y = [model.addVar(vtype="B") for j in range(m)]
    # add objective function
    model.setObjective(qsum(y), "minimize")
    # add constraints
    for i in range(n):
        model.addCons(qsum(x[i,j] for j in range(m)) == 1)
    for j in range(m):
        model.addCons(qsum(w[i]*x[i,j] for i in range(n)) <= W[j]*y[j])
    # remove verbose
    model.hideOutput()
    # optimize
    model.optimize()
    min_bins = model.getObjVal()
    bin_assignment = [next(j for j in range(m) if model.getVal(x[i,j]) > 0.5) for i in range(n)]
    return min_bins, bin_assignment

if __name__ == "__main__":
    n = 7
    m = 7
    w = [5,3,7,5,2,2,5]
    W = [8]*m
    min_bins, bin_assignment = bpp(n,m,w,W)
    print("Min Bins:",min_bins)
    print("Bin Assignment:",bin_assignment)
    