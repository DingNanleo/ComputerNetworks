# Plots results for input file of form
# event_number  queue_len   dropped_packets

import sys
import argparse
import re
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def get_args(argv):
    parser = argparse.ArgumentParser(description="Program for plotting simulator results")
    parser.add_argument('-i', '--input-file',    required=True)
    parser.add_argument('-o', '--output-file',required=True)
    parser.add_argument('-t', '--title', required=False)
    return parser.parse_args()

def main(argv):
    args = get_args(argv)

    # Read points from file
    event_seq_points = []
    queue_len_points = []
    dropped_count_points = []
    with open(args.input_file, 'r') as f:
        for line in f:
            parts = line.split()
            event_seq = int(parts[0])
            pkt_in_q = int(parts[1])
            pkt_dropped = int(parts[2])
            event_seq_points.append(event_seq)
            queue_len_points.append(pkt_in_q)
            dropped_count_points.append(pkt_dropped)

    # Create plot
    fig,ax=plt.subplots()
    ax.plot(event_seq_points, queue_len_points, label = "pkt_in_q")
    ax.plot(event_seq_points, dropped_count_points, label = "pkt_dropped")
    ax.legend()
    if args.title:
        plt.title(args.title)
        
    # Zoom function
    def on_scroll(event):
        base_scale = 1.2
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        x_range = (xlim[1] - xlim[0]) * 0.5
        y_range = (ylim[1] - ylim[0]) * 0.5
        xdata, ydata = event.xdata, event.ydata
        if event.button == 'up':
            scale_factor = 1 / base_scale
        elif event.button == 'down':
            scale_factor = base_scale
        else:
            return
        ax.set_xlim([xdata - x_range * scale_factor, xdata + x_range * scale_factor])
        ax.set_ylim([ydata - y_range * scale_factor, ydata + y_range * scale_factor])
        plt.draw()

    fig.canvas.mpl_connect('scroll_event', on_scroll)
    plt.show()
        
    plt.savefig(args.output_file)

if __name__ == "__main__":
    main(sys.argv[1:])
