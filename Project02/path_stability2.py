import pandas as pd

report_file = "google_path_stability_report.txt"
#report_file = "cmu_path_stability_report.txt"
#report_file = "x_path_stability_report.txt"

# Load your CSV
df = pd.read_csv("google_raw_AS.csv")  # Change to your actual CSV filename
#df = pd.read_csv("cmu_raw_AS.csv")  # Change to your actual CSV filename
#df = pd.read_csv("x_raw_AS.csv")  # Change to your actual CSV filename


# Ensure proper ordering by timestamp and hop
df = df.sort_values(by=["timestamp", "hop"])

# Group by timestamp to get individual paths
router_paths = df.groupby("timestamp")["ip"].apply(lambda x: tuple(x.dropna()))
as_paths = df.groupby("timestamp")["AS"].apply(lambda x: tuple(x.dropna()))

# Function to compute path change frequency
def calculate_path_change_frequency(paths):
    changes = 0
    total = len(paths) - 1
    previous_path = None
    for path in paths:
        if previous_path is not None and path != previous_path:
            changes += 1
        previous_path = path
        #print(previous_path)
    return (changes / total) * 100 if total > 0 else 0

# Calculate change frequencies
router_change_freq = calculate_path_change_frequency(router_paths.tolist())
as_change_freq = calculate_path_change_frequency(as_paths.tolist())

# Print results
print("Path Change Frequency Report:")
print(f"Router Path Change Frequency: {router_change_freq:.2f}%")
print(f"AS Path Change Frequency: {as_change_freq:.2f}%")

with open(report_file, "a") as f:  # Use "a" for append mode
    f.write("--------------------------------------------------------------\n")
    f.write("For destination: www.google.com\n")
    #f.write("For destination: www.cmu.edu\n")
    #f.write("For destination: www.x.com\n")
    
    f.write("Path Change Frequency Report:\n")
    f.write(f"Router Path Change Frequency: {router_change_freq:.2f}%\n")
    f.write(f"AS Path Change Frequency: {as_change_freq:.2f}%\n")
