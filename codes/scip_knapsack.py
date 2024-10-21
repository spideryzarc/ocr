from pyscipopt import Model 
from pyscipopt import quicksum as qsum

def knapsack(C:int,profits:list,weights:list)->tuple:
    '''
    C: int - capacity of the knapsack
    profits: list - list of profits of each item
    weights: list - list of weights of each item
    return: tuple - (max_profit, items)
    '''
    n = len(profits)
    model = Model("knapsack")
    x = [model.addVar(vtype="B") for i in range(n)]
    # add objective function
    model.setObjective(qsum(profits[i]*x[i] for i in range(n)), "maximize")
    # add constraints
    model.addCons(qsum(weights[i]*x[i] for i in range(n)) <= C)
    # remove verbose
    model.hideOutput()
    # optimize
    model.optimize()
    max_profit = model.getObjVal()
    items = [i for i in range(n) if model.getVal(x[i]) > 0.5]
    return max_profit, items

if __name__ == "__main__":
    C = 10
    profits = [10,13,18,20,25,30]
    weights = [5,6,8,9,12,15]
    max_profit, items = knapsack(C,profits,weights)
    print("Max Profit:",max_profit)
    print("Items:",items)
    