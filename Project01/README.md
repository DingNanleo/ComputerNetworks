# Project-1: Queuing Simulation #

This README file explains how to run the codes in the project 1 file.The folder of project 1 includes  files of codes: Simulator.py, Simulator_Variable.py and plot_results.py. This readme file is help you to know how to run these python codes.

## Required Tools

The tools needed:
*  Python 3
*  Libraries: `argparse`, `random`, 'sys','json','ast'and `matplotlib`

To install the libraries:
```bash
pip install matplotlib
```

## Files
1: Simulator.py :  simulate events with constant input rate. This script simulates a queuing system with a buffer limit. Packets arrive and depart based on a given arrival rate () and departure rate (). If the queue is full, incoming packets are dropped.


2: Simulator_Variable.py：  simulate events with variable input rate. This script simulates a queuing system with a buffer limit. Packets arrive and depart based on a fixed departure rate (fixed at 120), buffer size (fixed at 100), total events(fixed at 1000000), but variable input rate (although this is variable, but it has several case (70,200,130,120,70) according to different percentage of events. If the queue is full, incoming packets are dropped.


3: plot_results.py:  plot the result of simulation.This script reads the output file from the queuing simulation and generates a plot of queue length and dropped packets over time.


## Introduction of the parameters

* **Arrival Rate (lambda, `--lambda_rate`)**: The rate at which packets arrive.

* **Departure Rate (mu, `--mu_rate`)**: The rate at which packets leave the queue.

* **Buffer Size (n, `--buffer_size`)**: The maximum number of packets that can be stored in the queue.

* **Number of Events (`--events`)**: The total number of events to simulate.


## Notes before running the files:
1: Make sure Simulator.py, Simulator_Variable.py and plot_results.py. are in the same file directory.

2: Make sure to use terminal tool with the address(path) the same as the python files.

3: Maker sure the generated plot files and data files are also in the same directory as the Python scripts.


## How to Run the Files

1: Simulator.py 
Instruction
Run the script with the required arguments:
python Simulator.py -o output.txt -l <lambda_rate> -m <mu_rate> -b <buffer_size> -e <total_events>
 
Arguments
-o, --output-file (str): File to save simulation results.
-l, --lambda-rate (int): Arrival rate ().
-m, --mu-rate (int): Departure rate ().
-b, --buffer-size (int): Queue buffer size.
-e, --total-events (int): Number of events to simulate.
 
Commands example:
```bash
xxxxxx$ python3 Simulator.py -o=result.txt -l=10 -m=4 -b=10 -e=40
```

Output Format
The results are saved in a file in the format:
1 1 0
2 2 0
3 1 0
4 0 0
...
Each row represents:
[event_number] [queue_length] [dropped_packets]



2: Simulator_Variable.py
Instruction
Run the script with the required arguments:
python Simulator_variable.py -o=output.txt 
 
Arguments
-o, --output-file (str): File to save simulation results.
 
Commands example:
```bash
xxxxxx$ python3 Simulator_variable.py -o=result_variable.txt 
```
 
Output Format
The results are saved in a file in the format:
1 1 0
2 2 0
3 1 0
4 0 0
...
 
Each row represents:
[event_number] [queue_length] [dropped_packets]


3: plot_results.py
Usage
Run the script with:
python plot_results.py -i output.txt -o plot.png -t "Queue Simulation Results"
 
Arguments
-i, --input-file (str): Input file containing the simulation results.
-o, --output-file (str): Output image file for the plot.
-t, --title (str, optional): Title of the plot.
 
Commands example:
```bash
xxxx$ python3 plot_results.py -i=result.txt -o=plotresult.jpg -t="plot of queue simulation"
 ```
 
Output
A line plot showing:
Queue length over time (pkt_in_q)
Dropped packets over time (pkt_dropped)
 
 
The plot is saved as an image file.


