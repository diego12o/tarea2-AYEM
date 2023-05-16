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