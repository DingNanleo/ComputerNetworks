# 4671340, Nan Ding, Feb,04,2025
# TELCOM 2310, Project 1: Queuing Simulation

import sys
import argparse
import random
import json
import ast

def get_args(argv):
    parser = argparse.ArgumentParser(description="Program for Event Simulator with Variable Input Rate")
    parser.add_argument('-o', '--output-file', required=True, help="File to save simulation results to")
    #parser.add_argument('-e', '--total-events', type=int, required=True, help="Number of events to simulate (min 1,000,000)")
    return parser.parse_args()

def get_lambda(event_index, total_events):
    # Determine lambda based on the percentage of total events completed.
    percentage = (event_index / total_events) * 100

    if percentage <= 10:
        return 70
    elif percentage <= 70:
        return 200
    elif percentage <= 80:
        return 130
    elif percentage <= 90:
        return 120
    else:
        return 70
  
def main(argv):
    #lamda_rate:arrival rate; mu_rate:departure rate
    args = get_args(argv)

    total_events = 1000000 # fixed at 1,000,000 events
    mu_rate = 120           # Departure rate: fixed as 120
    buffer_size = 100       # Buffer size: fixed as 100
    
    packets_inqueue=0       #define the number of packets in the queue
    dropped_packets=0       #define the number of dropped packets
    state_queue=[]          #define the state of queue


    for i in range(total_events):
        lambda_rate = get_lambda(i,total_events)  # get lambda based on event progress
        
        if random.random()<(lambda_rate / (lambda_rate + mu_rate)):
            #packet is arrival event
            if packets_inqueue < buffer_size:
                #still have a seat, packet can be in the queue
                packets_inqueue += 1
            else:
                #no seat, drop the packet
                dropped_packets += 1
        else:
            #packet is departural event
            if packets_inqueue > 0:
                packets_inqueue -= 1
                
        state_queue.append(f"{i+1} {packets_inqueue} {dropped_packets}")
        
    with open(args.output_file,"w") as fp:
        fp.write("\n".join(state_queue))
    
    print(f"Simulation results saved to {args.output_file}")

    
if __name__ == "__main__":
    main(sys.argv[1:])

