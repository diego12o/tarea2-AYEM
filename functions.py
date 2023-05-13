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

    # SET SOLUTION WITH LOWER COST
    solution_test = p_time

    while not factible_solution and (not taked_l_time or not taked_e_time):
        if e_time == solution_test:
            taked_e_time = True
            solution_test = p_time
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
            if not taked_e_time: solution_test = solution_test - 1
            elif not taked_l_time: solution_test = solution_test + 1
    #print("----------------------------------------------------------------")

    cost = solution_test - p_time
    if cost < 0: cost = cost*-1

    # RETURN SOLUTION AND COST
    return solution_test, cost

############################### STOCHASTIC GREEDY ################################
##################################################################################




################################ HILL CLIMBING MM ################################
##################################################################################




################################ HILL CLIMBING AM ################################
##################################################################################




################################## TABU SEARCH ###################################
##################################################################################