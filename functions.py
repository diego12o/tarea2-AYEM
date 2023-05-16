import time
from utils import search_greater_cost, time_corrector, miope
        
############################## DETERMINISTIC GREEDY ##############################
##################################################################################
def det_greedy(uav, uav_times, diff_times):
    arrival_plan = []
    total_cost = 0

    for i in range(0, uav):
        value, cost = miope(
            arrival_plan=arrival_plan,
            e_time=uav_times[i][0],
            p_time=uav_times[i][1],
            l_time=uav_times[i][2],
            diff_times=diff_times[i]
        )
        arrival_plan.append(value)
        # print(cost)
        total_cost = total_cost + cost
    return arrival_plan, total_cost


############################### STOCHASTIC GREEDY ################################
##################################################################################
def sto_greedy(uav, uav_times, diff_times):
    print("Hola")



################################ HILL CLIMBING MM ################################
##################################################################################
def hcmm(uav, uav_times, diff_times):
    # GET SOLUTION WITH GREEDY
    initial_arrival_plan, initial_cost = det_greedy(uav, uav_times, diff_times)
    # SEARCH POSITION WITH GREATER COST
    # pos_greater = search_greater_cost(initial_arrival_plan, uav_times)
    
    #########
    lower_cost = initial_cost
    lower_result = initial_arrival_plan
        
    for i in range(len(initial_arrival_plan)):
        aux_initial_arrival_plan = initial_arrival_plan[:]
        while(aux_initial_arrival_plan[i] != uav_times[i][1]):
            # print("-----------------------------------------------------")
            # print("INICIO: " + str(initial_arrival_plan))
            # SUBSTRACT 1 WHEN TIME IS GREATER THAN P_TIME
            # ADD 1 WHEN TIME IS LOWER THAN P_TIME
            if aux_initial_arrival_plan[i] > uav_times[i][1]:
                aux_initial_arrival_plan[i] = aux_initial_arrival_plan[i] - 1
                sum = -1
            elif aux_initial_arrival_plan[i] < uav_times[i][1]:
                aux_initial_arrival_plan[i] = aux_initial_arrival_plan[i] + 1
                sum = 1
            
            arrival_plan, total_cost_variation, feasible = time_corrector(arrival_plan=aux_initial_arrival_plan[:], uav_times=uav_times, pos_changed=i, diff_times=diff_times, sum=sum)
            
            if feasible:
                new_cost = initial_cost + total_cost_variation
                if new_cost < lower_cost:
                    lower_cost = new_cost
                    lower_result = arrival_plan
        
    #     print("NEW COST: {} INITIAL COST: {}".format(new_cost, initial_cost))
    #     print("FINAL: {}".format(arrival_plan))
    # print("----------------------------------------------------------")
    # print("COST: {} \n RESULT: \n{}".format(lower_cost, lower_result))
    return lower_result, lower_cost
        


################################ HILL CLIMBING AM ################################
##################################################################################
def hcam(uav, uav_times, diff_times):
    # GET SOLUTION WITH GREEDY
    initial_arrival_plan, initial_cost = det_greedy(uav, uav_times, diff_times)
    # SEARCH POSITION WITH GREATER COST
    pos_greater = search_greater_cost(initial_arrival_plan, uav_times)
    
    #########
    lower_cost = initial_cost
    lower_result = initial_arrival_plan
    
    start = time.time()
    end = time.time()

    while(lower_cost == initial_cost and end-start < 10):
        # print("-----------------------------------------------------")
        # print("INICIO: " + str(initial_arrival_plan))
        # SUBSTRACT 1 WHEN TIME IS GREATER THAN P_TIME
        # ADD 1 WHEN TIME IS LOWER THAN P_TIME
        if initial_arrival_plan[pos_greater] > uav_times[pos_greater][1]:
            initial_arrival_plan[pos_greater] = initial_arrival_plan[pos_greater] - 1
            sum = -1
        elif initial_arrival_plan[pos_greater] < uav_times[pos_greater][1]:
            initial_arrival_plan[pos_greater] = initial_arrival_plan[pos_greater] + 1
            sum = 1
        
        arrival_plan, total_cost_variation, feasible = time_corrector(arrival_plan=initial_arrival_plan[:], uav_times=uav_times, pos_changed=pos_greater, diff_times=diff_times, sum=sum)
        
        if feasible:
            new_cost = initial_cost + total_cost_variation
            if new_cost < lower_cost:
                lower_cost = new_cost
                lower_result = arrival_plan
        
        end = time.time()
        
    #     print("NEW COST: {} INITIAL COST: {}".format(new_cost, initial_cost))
    #     print("FINAL: {}".format(arrival_plan))
    # print("----------------------------------------------------------")
    # print("COST: {} \n RESULT: \n{}".format(lower_cost, lower_result))
    return lower_result, lower_cost


################################## TABU SEARCH ###################################
##################################################################################
def tabu_search(uav, uav_times, diff_times):
    print("Hola")