import numpy as np

call_counter = 0

def knapsack_rec(itens:list, W:int)->tuple:
    ''' Solve the knapsack problem using recursive approach.
    itens: list of dict with the items, where the dict has the keys 'v' and 'w'.
    W: int, the maximum weight that the knapsack can carry.
    return: tuple, (list, int) where the list contains the items that should be taken and the int is the total value.
    '''
    global call_counter
    call_counter += 1
    # anchor cases
    if W <= 0: return ([], 0)
    if len(itens) == 1:
        if itens[0]['w'] <= W:
            return ([itens[0]], itens[0]['v'])
        return ([], 0)
<<<<<<< HEAD
    
    # solve assuming the item is taken
    taken, value = M(itens[1:], W-itens[0]['w'])
    value += itens[0]['v']
    # solve assuming the item is not taken
    not_taken, value2 = M(itens[1:], W)
    # return the best solution between the two
    if value > value2: 
        return (taken + [itens[0]], value)
    return (not_taken, value2)
=======
    if itens[0]['w'] > W:
        return knapsack_rec(itens[1:], W)
    else:
        # solve assuming the item is taken
        taken, value = knapsack_rec(itens[1:], W-itens[0]['w'])
        value += itens[0]['v']
        # solve assuming the item is not taken
        not_taken, value2 = knapsack_rec(itens[1:], W)
        if value > value2:
            return (taken + [itens[0]], value)
        return (not_taken, value2)


def knapsack_pd(itens:list, W:int)->tuple:
    ''' Solve the knapsack problem using dynamic programming approach.
    itens: list of dict with the items, where the dict has the keys 'v' and 'w'.
    W: int, the maximum weight that the knapsack can carry.
    return: tuple, (list, int) where the list contains the items that should be taken and the int is the total value.
    '''
    n = len(itens)
    M = [[0 for _ in range(W+1)] for _ in range(n+1)]
    #fill first row
    w0 = itens[0]['w']
    v0 = itens[0]['v']
    for w in range(w0, W+1):
        M[0][w] = v0
    #fill the rest of the matrix
    for i in range(1,n):
        wi = itens[i]['w']
        vi = itens[i]['v']
        M[i][:wi] = M[i-1][:wi] # remain the same until the weight of the item
        for w in range(wi, W+1):
            M[i][w] = max(M[i-1][w], M[i-1][w-wi] + vi)
    # get the items taken
    taken = []
    i = n-1
    w = W
    while i > 0:
        if M[i][w] != M[i-1][w]:
            taken.append(itens[i])
            w -= itens[i]['w']
        i -= 1
    if M[i][w] != 0:
        taken.append(itens[i])
    return taken, M[n-1][W]
>>>>>>> 1be8fe024c23d29d2379f36b3e9349303e7cc4c5
    
# Example

n = 50
W = 100
max_w = 50
min_w = 5
max_v = 100
min_v = 1
itens = [{'w': np.random.randint(min_w, max_w), 'v': np.random.randint(min_v, max_v)} for _ in range(n)]

print(itens)
print(knapsack_pd(itens, W))
print(knapsack_rec(itens, W))
print(call_counter)
