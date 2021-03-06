import sys
sys.path.append('../solverS')
sys.path.append('../tracer')
sys.path.append('../analysis')

#import random
from solver import solve
from traceable_random import random
from wrapper_patch import random_function #overload module random and use random_function as address decorator
from compare import compare_methods, plot_scalability, compare_all, stat_summary, make_table, plot_runs
