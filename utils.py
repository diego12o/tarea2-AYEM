import random

def calculate_cost(arrival_plan, uav_times):
    total_cost = 0
    for i in range(len(arrival_plan)):
        cost = arrival_plan[i]-uav_times[i][1]
        if cost < 0: cost=cost*-1
        total_cost = total_cost + cost
    return total_cost

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

def time_corrector(arrival_plan, uav_times, pos_changed, diff_times):
    feasible = True
    # order = order_by_conflicts(arrival_plan, diff_times)
    for i in range(len(arrival_plan)):
        # i = order[pos][1]
        l_time = uav_times[i][2]
        e_time = uav_times[i][0]
        sum = 1
        
        if i in pos_changed: continue
        if l_time == e_time:
            pos_changed.append(i)
            continue
        pos_changed.append(i)

        taked_e_time = False
        taked_l_time = False
        initial_value = uav_times[i][1]
        arrival_plan[i] = uav_times[i][1]
        
        while True:
            if arrival_plan[i] == e_time: taked_e_time = True
            if arrival_plan[i] == l_time: taked_l_time = True

            if not taked_e_time and not taked_l_time:
                arrival_plan[i] = initial_value + sum
                sum = sum*-1
            elif taked_e_time and not taked_l_time: arrival_plan[i] = arrival_plan[i] + 1
            elif taked_l_time and not taked_e_time: arrival_plan[i] = arrival_plan[i] - 1
            elif taked_e_time and taked_l_time:
                return arrival_plan, False
            
            if not get_conflict(arrival_plan, diff_times, i):
                if time_corrector(arrival_plan, uav_times, pos_changed, diff_times): return arrival_plan, feasible
            
            if sum > 0: sum = sum + 1
    
    return arrival_plan, feasible


def miope(arrival_plan, e_time, l_time, p_time, diff_times, pos):
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
            
            # print("[" + str(min_range_value) + ", " + str(max_range_value) + "] ----> " + str(solution_test))
            # VERIFY IF THE SOLUTION TAKED IS IN THE RANGE
            if arrival_time > solution_test:
                min_range_value = solution_test
                max_range_value = solution_test + diff_times[pos][i]
                if arrival_time < max_range_value and arrival_time > min_range_value:
                    factible_solution = False
                    break
            elif arrival_time < solution_test:
                min_range_value = arrival_time
                max_range_value = arrival_time + diff_times[i][pos]
                if solution_test > min_range_value and solution_test < max_range_value:
                    factible_solution = False
                    break
            else:
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
                var_solution = var_solution + 1

    #print("----------------------------------------------------------------")

    # RETURN SOLUTION AND COST
    return solution_test

def miope_sto(arrival_plan, e_time, l_time, p_time, diff_times, pos):
    factible_solution = False
    taked_e_time = False
    taked_l_time = False
    var_solution = 1

    # SET SOLUTION WITH LOWER COST
    solution_test = p_time

    
    while not factible_solution and (not taked_l_time or not taked_e_time):
        if e_time == solution_test: taked_e_time = True
        if l_time == solution_test: taked_l_time = True

        take_solution = random.randint(1, 10) >= 7
        if take_solution:
            factible_solution = True
            for i in range(len(arrival_plan)):
                arrival_time = arrival_plan[i]
                # GET RANGE OF VALUES THAT CANT TAKE THE SOLUTION
                
                # print("[" + str(min_range_value) + ", " + str(max_range_value) + "] ----> " + str(solution_test))
                # VERIFY IF THE SOLUTION TAKED IS IN THE RANGE
                if arrival_time > solution_test:
                    min_range_value = solution_test
                    max_range_value = solution_test + diff_times[pos][i]
                    if arrival_time < max_range_value and arrival_time > min_range_value:
                        factible_solution = False
                        break
                elif arrival_time < solution_test:
                    min_range_value = arrival_time
                    max_range_value = arrival_time + diff_times[i][pos]
                    if solution_test > min_range_value and solution_test < max_range_value:
                        factible_solution = False
                        break
                else:
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
                var_solution = var_solution + 1

    #print("----------------------------------------------------------------")

    # RETURN SOLUTION AND COST
    return solution_test


def get_conflict(arrival_plan, diff_times, i):
    for j in range(len(arrival_plan)):
        if i == j: continue
        
        arrival_time_i = arrival_plan[i]
        arrival_time_j = arrival_plan[j]
        
        if arrival_time_j > arrival_time_i:
            min_range_value = arrival_time_i
            max_range_value = arrival_time_i + diff_times[i][j]
            if arrival_time_j < max_range_value and arrival_time_j > min_range_value: return True
        elif arrival_time_j < arrival_time_i:
            min_range_value = arrival_time_j
            max_range_value = arrival_time_j + diff_times[j][i]
            if arrival_time_i > min_range_value and arrival_time_i < max_range_value: return True
        else: return True
    return False

def conflict(arrival_plan, diff_times):
    for i in range(len(arrival_plan)):
        for j in range(len(arrival_plan)):
            if i == j: continue
            
            arrival_time_i = arrival_plan[i]
            arrival_time_j = arrival_plan[j]
            
            if arrival_time_j > arrival_time_i:
                min_range_value = arrival_time_i
                max_range_value = arrival_time_i + diff_times[i][j]
                if arrival_time_j < max_range_value and arrival_time_j > min_range_value: return True
            elif arrival_time_j < arrival_time_i:
                min_range_value = arrival_time_j
                max_range_value = arrival_time_j + diff_times[j][i]
                if arrival_time_i > min_range_value and arrival_time_i < max_range_value: return True
            else: return True
    return False

def order_by_conflicts(arrival_plan, diff_times):
    list = []
    for i in range(len(arrival_plan)):
        conflicts = 0
        for j in range(len(arrival_plan)):
            if i == j: continue
            if arrival_plan[i] + diff_times[i][j] >= arrival_plan[j] and arrival_plan[i] - diff_times[i][j] <= arrival_plan[j]: conflicts = conflicts + 1
        pair = (conflicts, i)
        list.append(pair)
    list.sort()
    return list