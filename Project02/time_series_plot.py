import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load your dataset (replace with your actual file path)
#df = pd.read_csv("google_raw_AS.csv")  # Change to your actual CSV filename
df = pd.read_csv("cmu_raw_AS.csv")  # Change to your actual CSV filename
#df = pd.read_csv("x_raw_AS.csv")  # Change to your actual CSV filename

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d_%H%M%S')

# Step 1: Group by timestamp and extract paths as strings
router_paths = df.groupby("timestamp")["ip"].apply(lambda x: ' -> '.join(x.dropna().astype(str)))
as_paths = df.groupby("timestamp")["AS"].apply(lambda x: ' -> '.join(x.dropna().astype(str)))

# Step 2: Assign a unique integer ID to each unique path (categorical encoding)
router_path_codes = router_paths.astype("category").cat.codes
as_path_codes = as_paths.astype("category").cat.codes

# Step 3: Create the plot
fig, ax = plt.subplots(figsize=(14, 6))

# Plot router paths using numeric ID as y-value
ax.plot(router_paths.index, router_path_codes, label="Router Path", marker="o", linestyle='-', color="blue")

# Plot AS paths using numeric ID as y-value
ax.plot(as_paths.index, as_path_codes, label="AS Path", marker="x", linestyle='--', color="orange")

# Step 4: Set x-ticks to be the actual timestamps from the dataframe
ax.set_xticks(router_paths.index)  # Use the index of the grouped data as x-ticks
ax.set_xticklabels(router_paths.index.strftime('%m%d-%H'), rotation=45)  # Format the x-ticks as mmdd-hh

# Adding labels and title
ax.set_xlabel("Timestamp (mmdd-hh)")
ax.set_ylabel("Path Group ID")
#ax.set_title("wwww:google.com: Time-Series Plot of Path Changes")
ax.set_title("wwww:cmu.edu: Time-Series Plot of Path Changes")
#ax.set_title("wwww:x.com: Time-Series Plot of Path Changes")
ax.legend()

# Layout adjustment
plt.tight_layout()
plt.grid(True)
plt.show()
