import numpy as np

call_counter = 0

def M(itens:list, W:int)->tuple:
    ''' Solve the knapsack problem using recursive approach.
    itens: list of dict with the items, where the dict has the keys 'v' and 'w'.
    W: int, the maximum weight that the knapsack can carry.
    return: tuple, (list, int) where the list contains the items that should be taken and the int is the total value.
    '''
    global call_counter
    call_counter += 1
    
    if len(itens) == 1:
        if itens[0]['w'] <= W:
            return ([itens[0]], itens[0]['v'])
        return ([], 0)
    if itens[0]['w'] > W:
        return M(itens[1:], W)
    else:
        # solve assuming the item is taken
        taken, value = M(itens[1:], W-itens[0]['w'])
        value += itens[0]['v']
        # solve assuming the item is not taken
        not_taken, value2 = M(itens[1:], W)
        if value > value2:
            return (taken + [itens[0]], value)
        return (not_taken, value2)
    
# Example

n = 30
W = 100
max_w = 50
min_w = 5
max_v = 100
min_v = 1
itens = [{'w': np.random.randint(min_w, max_w), 'v': np.random.randint(min_v, max_v)} for _ in range(n)]

print(itens)
print(M(itens, W))
print(call_counter)
