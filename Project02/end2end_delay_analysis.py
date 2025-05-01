import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

#report_file = "google_path_stability_report.txt"
#report_file = "cmu_path_stability_report.txt"
report_file = "x_path_stability_report.txt"

# Load data
#df = pd.read_csv("google_raw_AS.csv")  # Change to your actual CSV filename
#df = pd.read_csv("cmu_raw_AS.csv")     # Change to your actual CSV filename
df = pd.read_csv("x_raw_AS.csv")         # Change to your actual CSV filename

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d_%H%M%S')
df['hour'] = df['timestamp'].dt.hour
df['month_day'] = df['timestamp'].dt.strftime('%m-%d %H')

# Convert RTT values to numeric
df[['rtt1', 'rtt2', 'rtt3']] = df[['rtt1', 'rtt2', 'rtt3']].apply(pd.to_numeric, errors='coerce')

# Step 1: Identify the Destination Hop (last hop for each timestamp)
df_last_hop = df.groupby('timestamp',group_keys=False).apply(lambda x: x.loc[x['hop'].idxmax()])


# Step 2: Calculate the average RTT for the destination hop (mean of rtt1, rtt2, rtt3)
df_last_hop['avg_rtt'] = df_last_hop[['rtt1', 'rtt2', 'rtt3']].mean(axis=1)

# Step 3: Document the end-to-end delay time (destination hop delay time)
# We now have the average RTT of each destination hop per timestamp measurement
delay_times = df_last_hop['avg_rtt'].tolist()

# Step 4: Compute Statistics for the 51 delay times
max_delay = np.max(delay_times)
min_delay = np.min(delay_times)
avg_delay = np.mean(delay_times)
std_dev_delay = np.std(delay_times)

# Step 5: Calculate Packet Loss Rate
# A packet is considered lost if the destination hop's RTTs are all NA or if any timeout occurs
lost_measurements = df_last_hop[df_last_hop[['rtt1', 'rtt2', 'rtt3']].isna().all(axis=1)].shape[0]
packet_loss_rate = (lost_measurements / len(df_last_hop)) * 100

# Step 6: Calculate Max - Min, Daytime and Nighttime Averages
delay_range = max_delay - min_delay

daytime_delays = df_last_hop[(df_last_hop['hour'] >= 8) & (df_last_hop['hour'] <= 20)]['avg_rtt'].dropna()
nighttime_delays = df_last_hop[(df_last_hop['hour'] < 8) | (df_last_hop['hour'] > 20)]['avg_rtt'].dropna()

daytime_avg_delay = daytime_delays.mean()
nighttime_avg_delay = nighttime_delays.mean()



# Write statistics to report file
with open(report_file, "a") as f:
    f.write("--------------------------------------------------------------\n")
    #f.write("For destination: www.google.com\n")
    #f.write("For destination: www.cmu.edu\n")
    f.write("For destination: www.x.com\n")
    f.write("Detailed End-to-End Delay Metrics (per measurement):\n")
    f.write("Timestamp\t\tEnd-to-End Delay (ms)\n")
    for i, row in df_last_hop.iterrows():
        #f.write(f"{row['timestamp']}\t{row['avg_rtt']:.2f}\n")
        delay = row['avg_rtt']
        delay_str = f"{delay:.2f}" if pd.notna(delay) else "NaN"
        f.write(f"{row['timestamp']}\t{delay_str}\n")
    
    f.write(f"\nSummary: \n")
    f.write(f"Maximum End-to-End Delay: {max_delay:.2f} ms\n")
    f.write(f"Minimum End-to-End Delay: {min_delay:.2f} ms\n")
    f.write(f"Max-Min(spread of delay) Delay Range: {delay_range:.2f} ms\n")
    f.write(f"Average End-to-End Delay: {avg_delay:.2f} ms\n")
    f.write(f"Standard Deviation of Delay: {std_dev_delay:.2f} ms\n")
    f.write(f"Packet Loss Rate: {packet_loss_rate:.2f} %\n\n")
    f.write(f"Daytime Average Delay (08:00–20:00): {daytime_avg_delay:.2f} ms\n")
    f.write(f"Nighttime Average Delay (20:01–07:59): {nighttime_avg_delay:.2f} ms\n\n")


# Plotting: Single plot for 51 end-to-end delay measurements
plt.figure(figsize=(12, 6))
plt.plot(df_last_hop['timestamp'], df_last_hop['avg_rtt'], marker='o', color='blue', label="End-to-End Delay")
#plt.title("www.google.com: End-to-End Delay Over Time", fontsize=14)
#plt.title("www.cmu.edu: End-to-End Delay Over Time", fontsize=14)
plt.title("www.x.com: End-to-End Delay Over Time", fontsize=14)
plt.xlabel("Time")
plt.ylabel("Delay (ms)")
plt.legend()

# Format x-axis
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H'))
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=53))
plt.xticks(rotation=270)
plt.tight_layout()
plt.show()




