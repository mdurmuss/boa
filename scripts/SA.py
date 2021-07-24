# -*- coding: utf-8 -*-

import numpy as np
from tqdm import tqdm

class SimulatedAnnealing():
    def __init__(self, problem, operator, iter_max = 1000, cooling_coef = 0.9, initial_temperature = 1000, final_temperature = 0.1):
        self.problem = problem
        self.operator = operator
        self.iter_max = iter_max
        self.cooling_coef = cooling_coef
        self.initial_temperature = initial_temperature
        self.final_temperature = final_temperature
        self.best_solution = []
        self.best_objective = 0
        
    def cooling_Temperature(self, temperature):
        return temperature * self.cooling_coef
    
    def run(self):
        current_solution = np.random.permutation(self.problem.dimension)
        current_objective = self.problem.objective_function(current_solution)
        
        self.best_solution = current_solution.copy()
        self.best_objective = current_objective
        
        temperature = self.initial_temperature
        t = 0
        for t in tqdm(range(self.iter_max)):
            temperature = self.initial_temperature
            while temperature > self.final_temperature:
                candidate_solution = self.operator.genSol(current_solution)
                candidate_objective = self.problem.objective_function(candidate_solution)
                
                delta = candidate_objective - current_objective
                
                if delta < 0:
                    current_solution = candidate_solution.copy()
                    current_objective = candidate_objective
                    
                    if current_objective < self.best_objective:
                        self.best_solution = current_solution.copy()
                        self.best_objective = current_objective
                    
                else:
                    acceptance_probability = np.exp(-delta/temperature)
                    if np.random.uniform() < acceptance_probability:
                        current_solution = candidate_solution.copy()
                        current_objective = candidate_objective
                        
                                
                
                temperature = self.cooling_Temperature(temperature)

        
        return self.best_solution, self.best_objective
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
