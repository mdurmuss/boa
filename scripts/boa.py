#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mustafa Durmuş [mustafa.durmus@albert.health]


import numpy as np
import random
from tqdm import tqdm


PROBABILITY = 0.7 #  % probabibility switch
POWER_EXPONENT = 0.01


def sensory_modality_new(x, Ngen):
    """
    BOA algoritmasına göre sensory değişkenini günceller.
    """
    y = x + (0.025 / (x * Ngen))
    return y

def update_solution_float_to_integer(solution):
    """
    Continious değerleri discrete hale getirir.
    Ör:
        Continious = 0.1, 0.5, 0.8 , 0.2, 0.6, 0.7, 0.9
        Sorted     = 0.9, 0.8, 0.7, 0.6, 0.5, 0.3, 0.2
        Discrete   = 6    4    1     5    3    2    0
    """
    sorted_solution = sorted(solution, reverse=True)
    return [sorted_solution.index(idx) for idx in solution]


class BOA:
    def __init__(self, n_iter, lb, ub, population, wta_problem):
        self.problem = wta_problem
        self.n_iter = n_iter  # toplam iterasyon sayısı
        self.lb = lb     #lb is the lower bound
        self.ub = ub     #up is the uppper bound
        self.dim = self.problem.dimension   # boyut
        self.population = population

    def calculate_fitness(self, X):
        """
        Tüm popülasyon için objective fonksiyonunu çalıştırır ve sonucları geriye döndürür.
        """
        best_objective = 10000
        best_solution = np.zeros([1, self.dim])
        fitness = np.zeros([self.population, 1])  # ileride lazım olacak.
        for i in range(self.population):
            current_objective = self.problem.objective_function(update_solution_float_to_integer(X[i]))
            fitness[i] = current_objective
            if current_objective <= best_objective:
                best_objective = current_objective
                best_solution = X[i]
        return fitness, best_solution, best_objective

    def run(self):
        """
        BOA algoritmasını uygula ve geriye değerlendirmeleri döndür.
        """
        ALL_OBJECTIVES = []

        sensor_modality = 0.01
        # agentlar için rastgele başlangıç yerleri ata.
        X = np.random.uniform(0, 1, (self.population, self.dim)) * (self.ub - self.lb) + self.lb
        X_new = X

        # fitness fonksiyonu ile popülasyonu değerlendir.
        fitness, best_solution, best_objective = self.calculate_fitness(X)

        # başlangıçtaki rastgele çözümlerden en iyisini bulduk ve kaydettik.

        # update
        for idx in tqdm(range(self.n_iter)):

            ALL_OBJECTIVES.append(best_objective)

            for i in range(self.population):
                FP = sensor_modality * (fitness ** POWER_EXPONENT)
                if random.random() > PROBABILITY:  # rastgele durum.
                    dis = random.random() * random.random() * best_solution - X[i]
                    X_new[i] = X[i] + np.matrix(dis * FP[0, :])
                else:  # en yakın komşu kelebekleri bul.
                    # makaledeki formüle göre düzenlendi.
                    epsilon = random.random()
                    jk = np.random.permutation(self.population)
                    dis = epsilon * epsilon * X[jk[0]] - X[jk[1]]
                    X_new[i] = X[i] + dis
                # yeni X listesinden değerlendirmeyi yapalım.
                f_new = self.problem.objective_function(update_solution_float_to_integer(X_new[i]))
                if  f_new< best_objective:
                    best_objective = f_new
                    best_solution = X_new[i]

            sensor_modality = sensory_modality_new(sensor_modality, idx + 1)


        return best_objective, best_solution, ALL_OBJECTIVES
