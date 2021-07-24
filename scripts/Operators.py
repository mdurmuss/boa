# -*- coding: utf-8 -*-

import numpy as np

class Operators:
    def __init__(self, dimension, op_name='swap'):
        self.D = dimension
        self.op_name = op_name
        
    def genSol(self,solution):
        if self.op_name=='swap':        
            r1 = np.random.randint(self.D)
            r2 = np.random.randint(self.D)
            while r1 == r2:
                r2 = np.random.randint(self.D)
            
            temp = solution[r1]
            solution[r1] = solution[r2]
            solution[r2] = temp
            
        elif self.op_name =='insert':  
            r1 = np.random.randint(self.D)
            r2 = np.random.randint(self.D)
            while r1 == r2:
                r2 = np.random.randint(self.D)
                
            if r1>r2:
                solution = np.hstack((solution[0:r2],solution[r1],solution[r2:r1],solution[(r1+1):]))                
            else:
                solution = np.hstack((solution[0:r1],solution[(r1+1):r2],solution[r1],solution[r2:]))
                
                
        elif self.op_name =='2opt':  
            r1 = np.random.randint(self.D)
            r2 = np.random.randint(self.D)
            while r1 == r2:
                r2 = np.random.randint(self.D)
                
            if r1>r2:
                solution = np.hstack((solution[0:r2],np.flip(solution[r2:r1]),solution[r1:]))                
            else:
                solution = np.hstack((solution[0:r1],np.flip(solution[r1:r2]),solution[r2:]))
                
                
         
                
        return solution