import time
import random
from utils import search_greater_cost, time_corrector, miope, calculate_cost, conflict, miope_sto
        
############################## DETERMINISTIC GREEDY ##############################
##################################################################################
def det_greedy(uav, uav_times, diff_times):
    arrival_plan = []

    for i in range(0, uav):
        value = miope(
            arrival_plan=arrival_plan,
            e_time=uav_times[i][0],
            p_time=uav_times[i][1],
            l_time=uav_times[i][2],
            diff_times=diff_times,
            pos= i
        )
        arrival_plan.append(value)
        
    total_cost = calculate_cost(arrival_plan, uav_times)
    return arrival_plan, total_cost


############################### STOCHASTIC GREEDY ################################
##################################################################################
def sto_greedy(uav, uav_times, diff_times):
    arrival_plan = []

    for i in range(0, uav):
        value = miope_sto(
            arrival_plan=arrival_plan,
            e_time=uav_times[i][0],
            p_time=uav_times[i][1],
            l_time=uav_times[i][2],
            diff_times=diff_times,
            pos= i
        )
        arrival_plan.append(value)
        
    total_cost = calculate_cost(arrival_plan, uav_times)
    return arrival_plan, total_cost



################################ HILL CLIMBING MM ################################
##################################################################################

def hcmm(uav, uav_times, diff_times):
    # GET SOLUTION WITH GREEDY
    initial_arrival_plan, initial_cost = det_greedy(uav, uav_times, diff_times)
    # SEARCH POSITION WITH GREATER COST
    # pos_greater = search_greater_cost(initial_arrival_plan, uav_times)
    
    #########
    lower_cost = initial_cost
    lower_result = initial_arrival_plan.copy()
    iterations = 10
    
    diff_sum = 1
        
    for iteration in range(iterations):
        print(iteration)
        solution = True
        initial_arrival_plan = lower_result.copy()
        
        for i in range(len(initial_arrival_plan)):
            # print(i)
            if uav_times[i][0] == uav_times[i][2]: continue
            
            aux_initial_arrival_plan = initial_arrival_plan.copy()
            for j in range(2):
                if j == 0 and initial_arrival_plan[i]-diff_sum>=uav_times[i][0]: aux_initial_arrival_plan[i] = initial_arrival_plan[i] - diff_sum
                elif j == 1 and initial_arrival_plan[i]+diff_sum<=uav_times[i][2]: aux_initial_arrival_plan[i] = initial_arrival_plan[i] + diff_sum
                
                arrival_plan, feasible = time_corrector(arrival_plan=aux_initial_arrival_plan[:], uav_times=uav_times, pos_changed=[i], diff_times=diff_times)
                if feasible:
                    new_cost = calculate_cost(arrival_plan=arrival_plan, uav_times=uav_times)
                    if new_cost < lower_cost:
                        # print(str(arrival_plan))
                        # print(conflict(arrival_plan, diff_times))
                        solution = False
                        lower_cost = new_cost
                        lower_result = arrival_plan
        
        if solution: diff_sum = diff_sum + 1
        else: diff_sum = 1
        
    return lower_result, lower_cost


################################ HILL CLIMBING AM ################################
##################################################################################
def hcam(uav, uav_times, diff_times):
    # GET SOLUTION WITH GREEDY
    initial_arrival_plan, initial_cost = det_greedy(uav, uav_times, diff_times)
    # SEARCH POSITION WITH GREATER COST
    # pos_greater = search_greater_cost(initial_arrival_plan, uav_times)
    
    #########
    lower_cost = initial_cost
    lower_result = initial_arrival_plan.copy()
    iterations = 500
    
    diff_sum = 1
        
    for iteration in range(iterations):
        print(iteration)
        solution = False
        initial_arrival_plan = lower_result.copy()
        
        for i in range(len(initial_arrival_plan)):
            # print(i)
            if uav_times[i][0] == uav_times[i][2]: continue
            
            aux_initial_arrival_plan = initial_arrival_plan.copy()
            for j in range(2):
                if j == 0 and initial_arrival_plan[i]-diff_sum>=uav_times[i][0]: aux_initial_arrival_plan[i] = initial_arrival_plan[i] - diff_sum
                elif j == 1 and initial_arrival_plan[i]+diff_sum<=uav_times[i][2]: aux_initial_arrival_plan[i] = initial_arrival_plan[i] + diff_sum
                
                arrival_plan, feasible = time_corrector(arrival_plan=aux_initial_arrival_plan[:], uav_times=uav_times, pos_changed=[i], diff_times=diff_times)
                if feasible:
                    new_cost = calculate_cost(arrival_plan=arrival_plan, uav_times=uav_times)
                    if new_cost < lower_cost:
                        # print(str(arrival_plan))
                        # print(conflict(arrival_plan, diff_times))
                        solution = True
                        lower_cost = new_cost
                        lower_result = arrival_plan
                        break
            # IF THERE IS A NEW BEST SOLUTION, CONTINUE TO THAT PLACE
            if solution: break
            
        if not solution: diff_sum = diff_sum + 1
        else: diff_sum = 1
        
    return lower_result, lower_cost


################################## TABU SEARCH ###################################
##################################################################################
def tabu_search(uav, uav_times, diff_times):
    # GET SOLUTION WITH GREEDY
    initial_arrival_plan, initial_cost = det_greedy(uav, uav_times, diff_times)
    # SEARCH POSITION WITH GREATER COST
    # pos_greater = search_greater_cost(initial_arrival_plan, uav_times)
    
    # TABU LIST
    tabu_list = []
    max_len_tabu_list = 50
    #########
    lower_cost = initial_cost
    lower_result = initial_arrival_plan.copy()
    tabu_solution = lower_result.copy()
    iterations = 100
    
    diff_sum = 1
        
    for iteration in range(iterations):
        print(iteration)
        solution = True
        initial_arrival_plan = tabu_solution.copy()
        
        for i in range(len(initial_arrival_plan)):
            # print(i)
            if uav_times[i][0] == uav_times[i][2]: continue
            
            aux_initial_arrival_plan = initial_arrival_plan.copy()
            for j in range(2):
                if j == 0 and initial_arrival_plan[i]-diff_sum>=uav_times[i][0]: aux_initial_arrival_plan[i] = initial_arrival_plan[i] - diff_sum
                elif j == 1 and initial_arrival_plan[i]+diff_sum<=uav_times[i][2]: aux_initial_arrival_plan[i] = initial_arrival_plan[i] + diff_sum
                
                arrival_plan, feasible = time_corrector(arrival_plan=aux_initial_arrival_plan[:], uav_times=uav_times, pos_changed=[i], diff_times=diff_times)
                if feasible and not arrival_plan in tabu_list:
                    # COST CALCULATE
                    new_cost = calculate_cost(arrival_plan=arrival_plan, uav_times=uav_times)
                    # ADD SOLUTION TO TABU_LIST
                    tabu_list.append(arrival_plan)
                    # SIZE CONTROL
                    if len(tabu_list) > max_len_tabu_list: tabu_list.pop(0)
                    if new_cost < lower_cost:
                        # print(str(arrival_plan))
                        # print(conflict(arrival_plan, diff_times))
                        solution = False
                        lower_cost = new_cost
                        lower_result = arrival_plan.copy()
                    if random.randint(1 ,10) >= 6:
                        tabu_solution = arrival_plan.copy()
        
        if solution: diff_sum = diff_sum + 1
        else: diff_sum = 1
        
    return lower_result, lower_cost