# -*- coding: utf-8 -*-

from Operators import Operators
from SA import SimulatedAnnealing
from wta import WTA

problem = WTA('../wta', 'wta5.txt')
operator = Operators(problem.dimension, op_name = '2opt')
SA = SimulatedAnnealing(problem, operator, iter_max = 100, cooling_coef = 0.98, initial_temperature = 1000, final_temperature = 0.1)

res = SA.run()
print(res)
