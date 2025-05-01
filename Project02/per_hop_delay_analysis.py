import pandas as pd
import numpy as np

# Load data
#df = pd.read_csv("google_raw_AS.csv")
#df = pd.read_csv("cmu_raw_AS.csv")
df = pd.read_csv("x_raw_AS.csv")

df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d_%H%M%S')
df['hour'] = df['timestamp'].dt.hour

# Convert RTTs to numeric
df[['rtt1', 'rtt2', 'rtt3']] = df[['rtt1', 'rtt2', 'rtt3']].apply(pd.to_numeric, errors='coerce')

# Get average RTT per row (i.e., per hop per timestamp)
df['avg_rtt'] = df[['rtt1', 'rtt2', 'rtt3']].mean(axis=1)

# ---- STEP 1: Identify Stable Hops (Consistent IPs) ----
hop_ip_counts = df.groupby('hop')['ip'].nunique().reset_index()
stable_hops = hop_ip_counts[hop_ip_counts['ip'] == 1]['hop'].tolist()

# ---- STEP 2: Calculate Per-Hop Statistics ----
results = []
# First get end-to-end delay from destination hop (per timestamp)
dest_hop_df = df.groupby('timestamp', group_keys=False).apply(lambda x: x.loc[x['hop'].idxmax()])
dest_hop_df['end_to_end_rtt'] = dest_hop_df[['rtt1', 'rtt2', 'rtt3']].mean(axis=1)
end_to_end_delay_map = dest_hop_df.set_index('timestamp')['end_to_end_rtt'].to_dict()

for hop in stable_hops:
    hop_data = df[df['hop'] == hop].copy()
    hop_data = hop_data[hop_data['avg_rtt'].notna()]  # Exclude timeouts
    
    # Day/Night Split
    daytime = hop_data[(hop_data['hour'] >= 8) & (hop_data['hour'] < 20)]
    nighttime = hop_data[(hop_data['hour'] < 8) | (hop_data['hour'] >= 20)]

    # Delay stats
    mean_delay = hop_data['avg_rtt'].mean()
    min_delay = hop_data['avg_rtt'].min()
    max_delay = hop_data['avg_rtt'].max()
    std_delay = hop_data['avg_rtt'].std()
    range_delay = max_delay - min_delay
    day_avg = daytime['avg_rtt'].mean()
    night_avg = nighttime['avg_rtt'].mean()

    # Bottleneck detection: Compare to end-to-end delay
    bottleneck_ratio = []
    for i, row in hop_data.iterrows():
        ts = row['timestamp']
        if ts in end_to_end_delay_map:
            hop_rtt = row['avg_rtt']
            end_rtt = end_to_end_delay_map[ts]
            if pd.notna(hop_rtt) and pd.notna(end_rtt) and end_rtt > 0:
                ratio = hop_rtt / end_rtt
                bottleneck_ratio.append(ratio)
    avg_ratio = np.mean(bottleneck_ratio)
    
    results.append({
        'hop': hop,
        'ip': hop_data['ip'].iloc[0],
        'mean_delay': mean_delay,
        'min_delay': min_delay,
        'max_delay': max_delay,
        'max_minus_min': range_delay,
        'std_delay': std_delay,
        'day_avg': day_avg,
        'night_avg': night_avg,
        'bottleneck_ratio': avg_ratio
    })

# ---- STEP 3: Save results to a report file ----
#report_file = "google_path_stability_report.txt"
#report_file = "cmu_path_stability_report.txt"
report_file = "x_path_stability_report.txt"

with open(report_file, 'a') as f:
    f.write("--------------------------------------------------------------\n")

    #f.write("www.google.com: Per-Hop Delay Stability Analysis (Only Stable Hops): \n")
    #f.write("www.cmu.edu: Per-Hop Delay Stability Analysis (Only Stable Hops): \n")
    f.write("www.x.com: Per-Hop Delay Stability Analysis (Only Stable Hops): \n")

    f.write("\n")
    for row in results:
        f.write(f"Hop: {row['hop']}, IP: {row['ip']}\n")
        f.write(f"  Mean Delay: {row['mean_delay']:.2f} ms\n")
        f.write(f"  Min Delay: {row['min_delay']:.2f} ms\n")
        f.write(f"  Max Delay: {row['max_delay']:.2f} ms\n")
        f.write(f"  Max - Min: {row['max_minus_min']:.2f} ms\n")
        f.write(f"  Std Deviation: {row['std_delay']:.2f} ms\n")
        f.write(f"  Daytime Avg Delay: {row['day_avg']:.2f} ms\n")
        f.write(f"  Nighttime Avg Delay: {row['night_avg']:.2f} ms\n")
        f.write(f"  Bottleneck Ratio (Hop/End-to-End): {row['bottleneck_ratio']:.2%}\n\n")


