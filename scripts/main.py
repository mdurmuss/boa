#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mustafa Durmuş [mustafa.durmus@albert.health]

import numpy as np
from boa import BOA
from wta import WTA
import matplotlib.pyplot as plt



def visualize_accuracy(epoch_no, result):
    """
    Epoch sayısına göre en iyi sonuçları görselleştirir.
    """
    plt.plot(range(epoch_no), result, 'g', label='Objective')
    plt.title('Iterasyon ve Objective Değeri')
    plt.xlabel('Iterasyon')
    plt.ylabel('Objective')
    plt.legend()
    plt.show()

def visualize_best_and_worst(result):
    """
    WTA problemlerine göre en iyi sonuçları görselleştirir.
    """
    best_result = [i[0] for i in result]
    worst_result = [i[2] for i in result]

    names = [f'WTA{i+1}' for i in range(len(result))]

    plt.plot(names, best_result, 'r', label='En iyi Değer')
    plt.plot(names, worst_result, 'g', label='En Kötü Değer')
    plt.title('WTA ya göre En İyi Değer ve En Kötü Değer Kıyaslaması')
    plt.xlabel('Problem')
    plt.ylabel('Objective')
    plt.legend()
    plt.show()

def visualize_wta(result):
    """
    WTA problemlerine göre en iyi sonuçları görselleştirir.
    """
    vis_result = [i[0] for i in result]
    names = [f'WTA{i+1}' for i in range(len(result))]
    plt.plot(names, vis_result, 'r', label='En iyi Değer')
    plt.title('WTA ya göre En İyi Değerler')
    plt.xlabel('Problem')
    plt.ylabel('Objective')
    plt.legend()
    plt.show()


def analyze_all(metric_type="best", is_visualize=True):
    """
    Tüm wta problemleri için BOA algoritmasını çalıştırır.
    """
    metric_results = []
    for i in [5,10,20,30,40,50,60,70,80,90,100,200]:
        file_name = f'wta{str(i)}.txt'
        problem = WTA(folderName='../wta', fileName=file_name)
        EPOCH = 1000
        butterfly = BOA(n_iter=EPOCH, lb=-100, ub=100, population=50, wta_problem=problem)
        best_objective, best_solution, all_results = butterfly.run()

        # metrikleri bulalım.
        best_result = round(np.min(all_results), 3)
        mean = round(np.mean(all_results),3)
        worst_result = round(np.max(all_results), 3)
        median = round(np.median(all_results), 3)
        standard_dev = round(np.std(all_results), 3)

        # diziye kayıt edelim.
        metric_results.append([best_result, mean, worst_result, median, standard_dev])

    if is_visualize:
        visualize_wta(metric_results)
        visualize_best_and_worst(metric_results)

    if metric_type == "best":
        return [i[0] for i in metric_results]
    elif metric_type == "std":
        return [i[4] for i in metric_results]

def analyze_wta50():
    """
    WTA50 problemi için BOA algoritmasını çalıştırır. populasyon=50
    """
    problem = WTA(folderName='../wta', fileName='wta50.txt')
    butterfly = BOA(n_iter=500, lb=0, ub=1, population=50, wta_problem=problem)
    best_objective, best_solution, all_results = butterfly.run()
    visualize_accuracy(500, all_results)



def visualize_boa_and_sa_result(boa_r, sa_r):
    """
    BOA ve SA sonuçlarını görselleştirir.
    """

    names = [f'WTA{i+1}' for i in range(len(boa_r))]

    plt.plot(names, boa_r, 'r', label='BOA Standard Sapma')
    plt.plot(names, sa_r, 'b', label='SA Standard Sapma')
    plt.title('WTA ya göre SA ve BOA Kıyaslaması')
    plt.xlabel('Problem')
    plt.ylabel('Objective')
    plt.legend()
    plt.show()


def visualize_boa_and_sa_result_with_std(boa_r):
    """
    BOA ve SA sonuçlarını standard sapma ile görselleştirir.
    """

    # makaleden alınmıştır.
    SA_STD_VALUES = [0, 0, 0, 0, 0, 0.14, 0.21, 0.30, 0.57, 0.72, 0.75, 0.86]

    names = [f'WTA{i+1}' for i in range(len(boa_r))]

    plt.plot(names, boa_r, 'r', label='Butterfly Algorithm Best')
    plt.plot(names, SA_STD_VALUES, 'g', label='Simulated Annealing Best')
    plt.title('WTA ya göre SA ve BOA Kıyaslaması Standard Sapma')
    plt.xlabel('Problem')
    plt.ylabel('Standard Deviation')
    plt.legend()
    plt.show()



def analyze_boa_sa(metric_type="best"):
    """
    BOA ve SA algoritmalarını tüm WTA popülasyonu için çalıştırır ve sonuçları görselleştirir.
    """
    boa_all_result = analyze_all(metric_type=metric_type,is_visualize=False)

    # FOR SIMULATED ANNEALING
    from Operators import Operators
    from SA import SimulatedAnnealing

    if not metric_type == "std":
        sa_all_results = []
        for i in [5,10,20,30,40,50,60,70,80,90,100,200]:
            file_name = f'wta{str(i)}.txt'
            problem = WTA(folderName='../wta', fileName=file_name)
            operator = Operators(problem.dimension, op_name='2opt')

            SA = SimulatedAnnealing(problem, operator, iter_max=100, cooling_coef=0.98, initial_temperature=1000,
                                    final_temperature=0.1)

            res = SA.run()
            sa_all_results.append(res[1])

        visualize_boa_and_sa_result(boa_all_result, sa_all_results)

    elif metric_type == "std":
        visualize_boa_and_sa_result_with_std(boa_all_result)

if __name__ == '__main__':

    # run for only wta50
    analyze_wta50()
    # run for all wta problem's
#    analyze_all()
     # sa ve boa algoritmalarını kıyasla.
#    analyze_boa_sa()
     # sa ve boa algoritmalarını standard sapma ile kıyasla.
#    analyze_boa_sa(metric_type="std")
