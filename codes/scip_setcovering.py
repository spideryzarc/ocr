from pyscipopt import Model 
from pyscipopt import quicksum as qsum

def setcovering(n:int,m:int,costs:list,sets:list)->tuple:
    '''
    n: int - number of rows
    m: int - number of columns
    costs: list - list of costs of each column
    sets: list - for each row, a list of columns that cover the row
    return: tuple - (min_cost, columns)
    '''
    model = Model("setcovering")
    x = [model.addVar(vtype="B") for j in range(m)]
    # add objective function
    model.setObjective(qsum(costs[j]*x[j] for j in range(m)), "minimize")
    # add constraints
    for i in range(n):
        model.addCons(qsum(x[j] for j in sets[i]) >= 1)
    # remove verbose
    model.hideOutput()
    # optimize
    model.optimize()
    min_cost = model.getObjVal()
    columns = [j for j in range(m) if model.getVal(x[j]) > 0.5]
    return min_cost, columns

if __name__ == "__main__":
    n = 4
    m = 6
    costs = [1,2,3,4,5,6]
    sets = [[0,1,2],[1,2,3],[3,4,5],[0,2,4]]
    min_cost, columns = setcovering(n,m,costs,sets)
    print("Min Cost:",min_cost)
    print("Columns:",columns)
    