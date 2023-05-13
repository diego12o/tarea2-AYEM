# HOW TO RUN
Use the following command:
```
python main.py -a [algorithm_to_use] -f [file_to_use] -t [number_of_executions]
```
Alternatives of algorithms:
- `det_greedy`: deterministic greedy
- `sto_greedy`: stochastic greedy
- `hcam`: hill climbing AM
- `hcmm`: hill climbing MM
- `tabu_search`: tabu search

Example:

```
python main.py -a det_greedy -f te_Titan.txt -t 5
```