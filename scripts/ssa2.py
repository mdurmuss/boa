# Required Libraries
import numpy  as np
import math
import random
import os

"""
swarm_size = Popülasyon boyutu. Varsayılan Değer 5'tir.

min_values ​​= Bir listedeki değişken(ler)in sahip olabileceği minimum değer. Varsayılan değer -5'tir.

max_values ​​= Bir listedeki değişken(ler)in sahip olabileceği maksimum değer. Varsayılan değer 5'tir.

(generations)nesiller = Toplam yineleme sayısı. Varsayılan Değer 50'dir.

target_function = Küçültülecek işlev.

"""
from tqdm import tqdm
import matplotlib.pyplot as plt


# Function
def target_function():
    return

# Function: Initialize Variables
def initial_position(swarm_size = 5, min_values = [-5,-5], max_values = [5,5], target_function = target_function):
    position = np.zeros((swarm_size, len(min_values)))
    for i in range(0, swarm_size):
        for j in range(0, len(min_values)):
             position[i,j] = random.uniform(min_values[j], max_values[j])
        position[i,-1] = target_function(position[i,0:position.shape[1]-1])
    return position

# Function: Initialize Food Position
def food_position(dimension = 2, target_function = target_function):
    food = np.zeros((1, dimension+1))
    for j in range(0, dimension):
        food[0,j] = 0.0
    food[0,-1] = target_function(food[0,0:food.shape[1]-1])
    return food

# Function: Updtade Food Position by Fitness
def update_food(position, food):
    for i in range(0, position.shape[0]):
        if (food[0,-1] > position[i,-1]):
            for j in range(0, position.shape[1]):
                food[0,j] = position[i,j]
    return food

# Function: Updtade Position
def update_position(position, food, c1 = 1, min_values = [-5,-5], max_values = [5,5], target_function = target_function):
    for i in range(0, position.shape[0]):
        if (i <= position.shape[0]/2):
            for j in range (0, len(min_values)):
                c2 = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
                c3 = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
                if (c3 >= 0.5): #c3 < 0.5
                    position[i,j] = np.clip((food[0,j] + c1*((max_values[j] - min_values[j])*c2 + min_values[j])), min_values[j],max_values[j])
                else:
                    position[i,j] = np.clip((food[0,j] - c1*((max_values[j] - min_values[j])*c2 + min_values[j])), min_values[j],max_values[j])                       
        elif (i > position.shape[0]/2 and i < position.shape[0] + 1):
            for j in range (0, len(min_values)):
                position[i,j] = np.clip(((position[i - 1,j] + position[i,j])/2), min_values[j],max_values[j])             
        position[i,-1] = target_function(position[i,0:position.shape[1]-1])         
    return position


def six_hump_camel_back(variables_values = [0, 0]):
        func_value = 4*variables_values[0]**2 - 2.1*variables_values[0]**4 + (1/3)*variables_values[0]**6 + variables_values[0]*variables_values[1] - 4*variables_values[1]**2 + 4*variables_values[1]**4
        return func_value


    # Function to be Minimized (Rosenbrocks Valley). Solution ->  f(x) = 0; xi = 1
def rosenbrocks_valley(variables_values = [0,0]):
        func_value = 0
        last_x = variables_values[0]
        for i in range(1, len(variables_values)):
            func_value = func_value + (100 * math.pow((variables_values[i] - math.pow(last_x, 2)), 2)) + math.pow(1 - last_x, 2)
        return func_value

# SSA Function
def salp_swarm_algorithm(problem, swarm_size = 5, min_values = [-5,-5], max_values = [5,5], iterations = 50, target_function = target_function):
    count    = 0
    position = initial_position(swarm_size = swarm_size, min_values = min_values, max_values = max_values, target_function = target_function)

    # ilk aşamada rastgele üretilen 50 pozisyon içerisindeki en iyi cost ve pozisyonu bulalım.
    best_cost = 10000
    best_solution_pos = np.zeros(50)
    for pos in position:
        new_position = continious_2_discrete(pos)
        cost = problem.objective_function(new_position)
        # eğer yeni pozisyonun cost'u en iyiden daha azsa, artık en iyi yeni cost olur.
        if cost < best_cost:
            best_cost = cost
            best_solution_pos = new_position

    # pozisyon güncellemesi
    food     = food_position(dimension = len(min_values), target_function = target_function)

    for count in tqdm(range(iterations)):
#        print("Iteration = ", count, " f(x) = ", food[0,-1])
        c1       = 2*math.exp(-(4*(count/iterations))**2)
        food     = update_food(position, food)
        position = update_position(position, food,
                                   c1 = c1,
                                   min_values = min_values,
                                   max_values = max_values,
                                   target_function = target_function)

        # pozisyonlar yukarıda güncellendi. Tekrar en iyi çözüm için arama yapılsın.
        for pos in position:
            new_position = continious_2_discrete(pos)
            cost = problem.objective_function(new_position)
            # eğer yeni pozisyonun cost'u en iyiden daha azsa, artık en iyi yeni cost olur.
            if cost < best_cost:
                best_cost = cost
                best_solution_pos = new_position
    return best_cost, best_solution_pos


def continious_2_discrete(solution):
    sorted_solution = sorted(solution, reverse=True)
    return [sorted_solution.index(idx) for idx in solution]



def visualize_wta(vis_result):
    """
    WTA problemlerine göre en iyi sonuçları görselleştirir.
    """
    names = [f'WTA{i+1}' for i in range(len(vis_result))]
    plt.plot(names, vis_result, 'r', label='En iyi Değer')
    plt.title('WTA ya göre En İyi Değerler')
    plt.xlabel('Problem')
    plt.ylabel('Objective')
    plt.legend()
    plt.show()


if __name__ == '__main__':

    from wta import WTA
    all_results = []
    for i in [5,10,20,30,40,50]:
        file_name = f'wta{i}.txt'
        problem = WTA('../wta', file_name)

        min_values = np.ones(i) * -5
        max_values = np.ones(i) * 5
        best_cost, best_pos = salp_swarm_algorithm(swarm_size = 5, min_values = min_values,
                                                   max_values = max_values, iterations = 100,
                                                   target_function = six_hump_camel_back, problem=problem)


        all_results.append(best_cost)

    visualize_wta(all_results)
