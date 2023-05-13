import argparse
import time
import functions

# ALTERNATIVES OF ALGORITHMS
# det_greedy: greedy determinista
# sto_greedy: greedy estocástico
# hcam: hill climbing alguna-mejora
# hcmm: hill climbing mejor-mejora
# tabu_search

algorithms = ['det_greedy', 'sto_greedy', 'hcam', 'hcmm', 'tabu_search']

def main(file, algorithm, times_number):
    if algorithm not in algorithms:
        raise Exception("Error: invalid algorithm")

    uav_times = []
    diff_times = []
    
    ##############################################################################
    ############################### GETTING PARAMS ###############################
    ##############################################################################
    uav = int(file.readline())
    count = 0
    while count < uav:
        array_uav_times = []
        array_diff_times = []

        # GET ARRIVAL TIMES
        times = file.readline().split()
        for arrival_time in times: array_uav_times.append(int(arrival_time))
        
        # GET DIFFERENCE TIMES BETWEEN UAVs
        while len(array_diff_times) != uav:
            times = file.readline().split()
            for uav_diff in times: array_diff_times.append(int(uav_diff))

        uav_times.append(array_uav_times)
        diff_times.append(array_diff_times)

        count = count + 1

    ##############################################################################
    ####################### HERE ALGORITHMS FUNCTIONS ############################
    ##############################################################################

    func = getattr(functions, algorithm)
    avg_time = 0
    avg_cost = 0

    print(times_number)
    for i in range(times_number):
        print("\033[92m" + "######################################################################" + "\033[;37m")

        start = time.time()
        arrival_plan, cost = func(uav=uav, uav_times=uav_times, diff_times=diff_times)
        end = time.time()
        # SHOW RESULTS
        print("\033[94m" + "ARRIVAL PLAN:\n" + "\033[;37m" + str(arrival_plan))
        print("\033[94m" + "TOTAL COST: " + "\033[;37m" + str(cost))
        print("\033[94m" + "TIME: " + "\033[;37m" + str(end-start))
        # CALCULATING AVERAGE
        avg_time = avg_time + (end-start)
        avg_cost = avg_cost + cost
        
        print("\033[92m" + "######################################################################" + "\033[;37m")

    # CALCULATING AVERAGE
    avg_cost = avg_cost/times_number
    avg_time = avg_time/times_number
    # SHOW AVERAGE
    print("\033[;31m" + "AVG TIME: " + "\033[;37m" + str(avg_time))
    print("\033[;31m" + "AVG COST: " + "\033[;37m" + str(avg_cost))
    


    ##############################################################################
    ##############################################################################
    ##############################################################################

if __name__ == "__main__":
    # GET PROGRAM ARGUMENTS
    parser = argparse.ArgumentParser(
        description="Arguments to use in this program",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-a", "--algorithm", help="Algorithm to solve the problem", required=True, nargs=1, type=str)
    parser.add_argument("-f", "--file", help="File with information about the problem", required=True, nargs=1, type=argparse.FileType('r'))
    parser.add_argument("-t", "--times", help="Times number of execution", default=1, nargs=1, type=int)
    args = parser.parse_args()

    main(file=args.file[0], algorithm=args.algorithm[0], times_number=args.times[0])