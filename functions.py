def search_greater_cost(arrival_plan, uav_times):
    pos_greater_cost = 0
    greater_cost = 0
    
    for i in range(len(arrival_plan)):
        # print("TIME: " + str(arrival_plan[i]) + " P_TIME: " + str(uav_times[i][1]))
        cost = arrival_plan[i] - uav_times[i][1]
        # print("COST: " + str(cost) + " POS: " + str(i))
        if cost < 0: cost=cost*-1
        if cost >= greater_cost:
            greater_cost = cost
            pos_greater_cost = i
        
    # print("GREATER: " + str(greater_cost) + " POS: " + str(pos_greater_cost))
    return pos_greater_cost

def time_corrector(arrival_plan, uav_times, pos_changed, diff_times, sum = -1):
    feasible = True
    total_cost_variation = 0
    
    for i in range(len(arrival_plan)):
        if i == pos_changed: continue

        arrival_time = arrival_plan[i]
        p_time = uav_times[i][1]
        l_time = uav_times[i][2]
        e_time = uav_times[i][0]
        
        impossible_values = []
        
        for j in range(len(arrival_plan)):
            if i == j: continue
            # time.sleep(0.5)
            # GET CONFLICT PARAMS
            conflict_time = arrival_plan[j]
            diff_time = diff_times[i][j]
            # INITIAL VARIABLES
            aux_arrival_time = arrival_time
            control = 0
            # VERIFY IF THERE IS CONFLICT
            while(aux_arrival_time <= conflict_time + diff_time and aux_arrival_time >= conflict_time - diff_time):
                can_take = True
                if aux_arrival_time in impossible_values: can_take = False
                
                impossible_values.append(aux_arrival_time)
                aux_arrival_time = aux_arrival_time + sum
                if not (aux_arrival_time <= conflict_time + diff_time and aux_arrival_time >= conflict_time - diff_time and can_take):
                    # NEW COST
                    new_cost = p_time - aux_arrival_time
                    if new_cost < 0: new_cost = new_cost*-1
                    # OLD COST
                    old_cost = p_time - arrival_time
                    if old_cost < 0: old_cost = old_cost*-1
                    
                    # IF NEW COST IS BIGGER THAN OLD COST, THEN TOTAL COST UP
                    total_cost_variation = total_cost_variation + new_cost - old_cost
                    
                    arrival_plan[i] = aux_arrival_time
                    break
                if e_time == aux_arrival_time or l_time == aux_arrival_time:
                    aux_arrival_time = arrival_time
                    sum = sum*-1
                    control = control + 1
                    if control == 2:
                        feasible = False
                        return 0, feasible
                    
    
    return arrival_plan, total_cost_variation, feasible
        

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

def miope(arrival_plan, e_time, l_time, p_time, diff_times):
    factible_solution = False
    taked_e_time = False
    taked_l_time = False
    var_solution = 1

    # SET SOLUTION WITH LOWER COST
    solution_test = p_time
    
    while not factible_solution and (not taked_l_time or not taked_e_time):
        if e_time == solution_test: taked_e_time = True
        if l_time == solution_test: taked_l_time = True

        factible_solution = True

        for i in range(len(arrival_plan)):
            arrival_time = arrival_plan[i]
            # GET RANGE OF VALUES THAT CANT TAKE THE SOLUTION
            min_range_value = arrival_time - diff_times[i]
            max_range_value = arrival_time + diff_times[i]
            # print("[" + str(min_range_value) + ", " + str(max_range_value) + "] ----> " + str(solution_test))
            # VERIFY IF THE SOLUTION TAKED IS IN THE RANGE
            if not (solution_test < min_range_value or solution_test > max_range_value):
                factible_solution = False
                break
        # SET NEW LOWER SOLUTION IF THE ACTUAL IS NOT FACTIBLE
        if not factible_solution:
            if not taked_e_time and solution_test >= p_time: solution_test = p_time - var_solution
            elif not taked_l_time and solution_test < p_time:
                solution_test = p_time + var_solution
                var_solution = var_solution + 1
            elif taked_e_time and solution_test >= p_time:
                solution_test = p_time + var_solution
                var_solution = var_solution + 1
            elif taked_l_time and solution_test < p_time:
                solution_test = p_time - var_solution
                var_solution = var_solution - 1

    #print("----------------------------------------------------------------")

    cost = solution_test - p_time
    if cost < 0: cost = cost*-1

    # RETURN SOLUTION AND COST
    return solution_test, cost

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
    pos_greater = search_greater_cost(initial_arrival_plan, uav_times)
    
    initial_arrival_plan[pos_greater] = initial_arrival_plan[pos_greater] - 1
    # time_corrector(arrival_plan=initial_arrival_plan, uav_times=uav_times, pos_changed=pos_greater, diff_times=diff_times)
    
    #########
    lower_cost = initial_cost
    lower_result = initial_arrival_plan
        
    while(initial_arrival_plan[pos_greater] != uav_times[pos_greater][1]):
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
    
    initial_arrival_plan[pos_greater] = initial_arrival_plan[pos_greater] - 1
    # time_corrector(arrival_plan=initial_arrival_plan, uav_times=uav_times, pos_changed=pos_greater, diff_times=diff_times)
    
    #########
    lower_cost = initial_cost
    lower_result = initial_arrival_plan

    while(lower_cost == initial_cost):
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
        
    #     print("NEW COST: {} INITIAL COST: {}".format(new_cost, initial_cost))
    #     print("FINAL: {}".format(arrival_plan))
    # print("----------------------------------------------------------")
    # print("COST: {} \n RESULT: \n{}".format(lower_cost, lower_result))
    return lower_result, lower_cost

################################## TABU SEARCH ###################################
##################################################################################
def tabu_search(uav, uav_times, diff_times):
    print("Hola")