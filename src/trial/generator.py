from PTO import random, random_function, solve

# no need for @random_function because this will be used as a generator itself
def randsol1(inst):
    # Create a permutation by shuffling. We provide a custom shuffle function.
    return swap_shuffle(list(range(len(inst))))

@random_function # inform PTO that this function must be traced
def swap_shuffle(perm): 
    for i in range(len(perm)):
        ri = random.choice(range(i,len(perm)))
        perm[i],perm[ri]=perm[ri],perm[i]
    return perm

# no need for @random_function because this will be used as a generator itself
def randsol2(inst):
    # Create a permutation by shuffling. We provide a custom shuffle function.
    return rev_shuffle(list(range(len(inst))))

@random_function # inform PTO that this function must be traced
def rev_shuffle(perm):
    # this is like multiple applications of 2-opt
    for i in range(len(perm)):
        ri = random.choice(range(i,len(perm)))
        perm[i:ri+1] = perm[i:ri+1][::-1] # reverse a section
    return perm
	
def randsol3(inst):
    """Take advantage of problem data in the simplest possible way"""
    n = len(inst)
    sol = []
    remaining = list(range(n))

    # the start city is a decision variable, because we'll get different results if
    # we start at different cities

    x = random.choice(list(range(n))) #(remaining) THIS WAS THE ROOT OF THE ERROR. 
    # Partial + Mutable in Local + argument of wrapped function = weird side effect... just avoid this combination!

    sol.append(x)
    remaining.remove(x)

    i = 1
    while i < n:

        # choose one of the remaining cities randomly, weighted by
        # inverse distance.
        x = choose_node(inst, x, remaining)
        sol.append(x)
        remaining.remove(x)

        i += 1

    return sol

# no need for @random_function, because choose_node makes no random calls itself
def choose_node(inst, cur, remaining):
    wts = [1.0 / inst[cur][n] for n in remaining]
    s = sum(wts)
    wts = [wt / float(s) for wt in wts] # normalise
    return roulette_wheel(remaining, wts)

@random_function # inform PTO that this function must be traced
def roulette_wheel(items, wts): # assumes wts sum to 1
    x = random.random()
    for item, wt in zip(items, wts):
        x -= wt
        if x <= 0:
            return item
    # Should not reach here
    print("Error")
    print(items)
    print(wts)
    print(r)
    raise ValueError
	
def fitness(perm, inst):
    # note negative indexing trick to include final step (return to origin)
    return -sum([inst[perm[i-1]][perm[i]] for i in range(0,len(perm))])

def randprob(n): 
    c = [[0 for x in range(n)] for x in range(n)] # initialise cost matrix
    for i in range(n):
        for j in range(n):
            if i == j:
                c[i][j] = 0 # zero diagonal
            elif i > j:
                c[i][j] = c[j][i] # symmetric matrix
            else:
                c[i][j] = random.expovariate(1) # more interesting than uniform weights
    return c

from functools import partial

inst = randprob(10) # generate a toy instance, represented by a city-city distance matrix
randsol1_inst = lambda: randsol1(inst) # specialise the generator for that instance
fitness_inst = lambda x: fitness(x, inst) # specialise the fitness for that instance

ind, fit = solve(randsol1_inst, fitness_inst, solver="HC", str_trace=True, effort=1.0)
print(ind)
print(fit)