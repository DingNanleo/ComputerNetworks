# 4671340, Nan Ding, Feb,04,2025
# TELCOM 2310, Project 1: Queuing Simulation

import sys
import argparse
import random
import json
import ast

def get_args(argv):
    parser = argparse.ArgumentParser(description="Program for Event Simulator")
    parser.add_argument('-o', '--output-file', required=True, help="File to save simulation results to")
    parser.add_argument('-l', '--lambda-rate', type=int, required=True, help="Arrival rate (λ)")
    parser.add_argument('-m', '--mu-rate', type=int, required=True, help="Departure rate (μ)")
    parser.add_argument('-b', '--buffer-size', type=int, required=True, help="Queue buffer size")
    parser.add_argument('-e', '--total-events', type=int, required=True, help="Number of events to simulate")
    return parser.parse_args()
  
def main(argv):
    #lamda_rate:arrival rate; mu_rate:departure rate
    args = get_args(argv)
    
    packets_inqueue=0         #define the number of packets in the queue
    dropped_packets=0       #define the number of dropped packets
    state_queue=[]             #define the state of queue


    for i in range(args.total_events):
        if random.random()<(args.lambda_rate / (args.lambda_rate + args.mu_rate)):
            #packet is arrival event
            if packets_inqueue < args.buffer_size:
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

