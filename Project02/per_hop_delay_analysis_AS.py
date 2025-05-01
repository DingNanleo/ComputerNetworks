import pandas as pd
import numpy as np

# Load data
#df = pd.read_csv("google_raw_AS.csv")
df = pd.read_csv("cmu_raw_AS.csv")
#df = pd.read_csv("x_raw_AS.csv")

df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d_%H%M%S')
df['hour'] = df['timestamp'].dt.hour


# Fill missing ASN
df['asn'] = df['AS Name'].fillna("NA")

# Compute average RTT per row
df['avg_rtt'] = df[['rtt1', 'rtt2', 'rtt3']].mean(axis=1)

# Build AS paths per timestamp
as_paths = df.groupby('timestamp')['asn'].apply(list)

# Find stable AS positions
stable_as_positions = {}
for i in range(max(len(p) for p in as_paths)):
    as_at_pos = as_paths.map(lambda x: x[i] if i < len(x) else "NA")
    unique_asn = as_at_pos.unique()
    if len(unique_asn) == 1 and unique_asn[0] != "NA":
        stable_as_positions[i] = unique_asn[0]

# Filter only stable AS hops
df_stable_as = df[df['AS Name'].isin(stable_as_positions.values())]

# Build end-to-end delay mapping from final hop of each timestamp group
end_to_end_delay_map = df.groupby('timestamp').apply(
    lambda g: g[g['hop'] == g['hop'].max()]['avg_rtt'].values[0]
).to_dict()

# Analyze delay stats for each consistent ASN
results = []
for asn, group in df_stable_as.groupby('AS Name'):
    daytime = group[(group['hour'] >= 8) & (group['hour'] < 20)]
    nighttime = group[(group['hour'] < 8) | (group['hour'] >= 20)]
    
    mean_delay = group['avg_rtt'].mean()
    min_delay = group['avg_rtt'].min()
    max_delay = group['avg_rtt'].max()
    std_delay = group['avg_rtt'].std()
    range_delay = max_delay - min_delay
    day_avg = daytime['avg_rtt'].mean()
    night_avg = nighttime['avg_rtt'].mean()
    
    # Bottleneck ratio vs end-to-end delay
    bottleneck_ratios = []
    for _, row in group.iterrows():
        ts = row['timestamp']
        if ts in end_to_end_delay_map:
            hop_rtt = row['avg_rtt']
            end_rtt = end_to_end_delay_map[ts]
            if pd.notna(hop_rtt) and pd.notna(end_rtt) and end_rtt > 0:
                ratio = hop_rtt / end_rtt
                bottleneck_ratios.append(ratio)
    avg_ratio = np.mean(bottleneck_ratios) if bottleneck_ratios else np.nan

    results.append({
        'AS Name': asn,
        'mean_delay': mean_delay,
        'min_delay': min_delay,
        'max_delay': max_delay,
        'max-min': range_delay,
        'standard_deviation': std_delay,
        'daytime_average_delay(8AM-8PM)': day_avg,
        'nighttime_avg_delay(other time)': night_avg,
        'bottleneck_ratio': avg_ratio
    })

# Optional: Convert to DataFrame for inspection
results_df = pd.DataFrame(results)
print(results_df)

# ---- STEP 3: Save results to a report file ----
#report_file = "google_path_stability_report.txt"
report_file = "cmu_path_stability_report.txt"
#report_file = "x_path_stability_report.txt"

with open(report_file, 'a') as f:
    f.write("--------------------------------------------------------------\n")

    #f.write("www.google.com: Per-Hop Delay Stability Analysis (Only Stable Hops): \n")
    f.write("www.cmu.edu: Per-Hop Delay Stability Analysis (Only Stable Hops): \n")
    #f.write("www.x.com: Per-Hop Delay Stability Analysis (Only Stable Hops): \n")

    for index, row in results_df.iterrows():
        f.write(f"{row.to_string()}\n")
