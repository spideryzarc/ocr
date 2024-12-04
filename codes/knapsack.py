import numpy as np
import time  # Use time module instead of timeit

# Add the timed decorator


def timed(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        time_taken = time.time() - start_time
        print(f"{func.__name__} time: {time_taken} seconds")
        return result
    return wrapper


call_counter = 0


@timed
def knapsack_rec_timed(itens: list, W: int) -> tuple:
    return knapsack_rec(itens, W)


def knapsack_rec(itens: list, W: int) -> tuple:
    ''' Solve the knapsack problem using recursive approach.
    itens: list of dict with the items, where the dict has the keys 'v' and 'w'.
    W: int, the maximum weight that the knapsack can carry.
    return: tuple, (list, int) where the list contains the items that should be taken and the int is the total value.
    '''
    # count the number of calls for didactic purposes
    global call_counter
    call_counter += 1
    # anchor cases
    if W <= 0 or len(itens) == 0:
        return ([], 0)
    # recursive cases
    if itens[0]['w'] > W:  # first item is too heavy
        return knapsack_rec(itens[1:], W)
    else:  # first item can be taken or not
        # solve assuming the item is taken
        taken, value = knapsack_rec(itens[1:], W-itens[0]['w'])
        value += itens[0]['v']  # add the value of the item
        # solve assuming the item is not taken
        not_taken, value2 = knapsack_rec(itens[1:], W)
        # return the best solution
        if value > value2:
            return (taken + [itens[0]], value)
        return (not_taken, value2)


@timed
def knapsack_pd(itens: list, W: int) -> tuple:
    ''' Solve the knapsack problem using dynamic programming approach.
    itens: list of dict with the items, where the dict has the keys 'v' and 'w'.
    W: int, the maximum weight that the knapsack can carry.
    return: tuple, (list, int) where the list contains the items that should be taken and the int is the total value.
    '''
    n = len(itens)  # number of itens
    M = [[0 for _ in range(W+1)] for _ in range(n+1)]  # matrix to store the values

    # fill first row with trivial case
    w0 = itens[0]['w']
    v0 = itens[0]['v']
    for w in range(w0, W+1):
        M[0][w] = v0

    # fill the rest of the matrix using the recursive formula M[i][w] = max(M[i-1][w], M[i-1][w-wi] + vi)
    for i in range(1, n):
        wi = itens[i]['w']  # weight of the item
        vi = itens[i]['v']  # value of the item
        M[i][:wi] = M[i-1][:wi]  # best value for weight w < wi is the same as the previous row
        for w in range(wi, W+1):
            M[i][w] = max(M[i-1][w], M[i-1][w-wi] + vi)
    # build the list of itens taken
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


@timed
def knapsack_pd_numpy(itens: list, W: int) -> tuple:
    ''' Solve the knapsack problem using dynamic programming approach, using numpy vectorized operations.
    itens: list of dict with the items, where the dict has the keys 'v' and 'w'.
    W: int, the maximum weight that the knapsack can carry.
    return: tuple, (list, int) where the list contains the items that should be taken and the int is the total value.
    '''
    n = len(itens)
    M = np.zeros(W + 1, dtype=int)
    keep = np.zeros((n, W + 1), dtype=bool)
    M_shifted = np.zeros(W + 1, dtype=int)

    for i in range(n):
        wi = itens[i]['w']
        vi = itens[i]['v']

        if wi <= W:
            M_shifted[:] = 0
            # Shift the M array to the right by wi positions and add vi
            M_shifted[wi:] = M[:-wi] + vi

            # Determine whether including the current item offers a better value
            new_M = np.maximum(M, M_shifted)

            # Keep track of items included
            keep[i] = M_shifted > M
            M = new_M

    # Reconstruct the list of items taken
    w = W
    taken = []
    for i in range(n - 1, -1, -1):
        if keep[i, w]:
            taken.append(itens[i])
            w -= itens[i]['w']

    return taken, M[W]

# Example


n = 100
W = 100
max_w = 50
min_w = 5
max_v = 100
min_v = 1
itens = [{'w': np.random.randint(min_w, max_w), 'v': np.random.randint(min_v, max_v)} for _ in range(n)]

print(knapsack_pd(itens, W)[1])
print(knapsack_pd_numpy(itens, W)[1])
# print(knapsack_rec_timed(itens, W)[1])
