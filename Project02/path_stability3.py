import pandas as pd

#report_file = "google_path_stability_report.txt"
#report_file = "cmu_path_stability_report.txt"
report_file = "x_path_stability_report.txt"


# Load data
#df = pd.read_csv("google_raw_AS.csv")  # Change to your actual CSV filename
#df = pd.read_csv("cmu_raw_AS.csv")  # Change to your actual CSV filename
df = pd.read_csv("x_raw_AS.csv")  # Change to your actual CSV filename


# Sort and group to ensure unique (timestamp, hop) combinations
df.sort_values(by=["timestamp", "hop"], inplace=True)
df_unique = df.groupby(["timestamp", "hop"], as_index=False).first()

# Pivot to wide format
ip_pivot = df_unique.pivot(index="timestamp", columns="hop", values="ip")
as_pivot = df_unique.pivot(index="timestamp", columns="hop", values="AS")


# Function to calculate volatility
#def compute_volatility(pivot_df):
#    changes = pivot_df.ne(pivot_df.shift()).sum()
#    total = pivot_df.shape[0] - 1
#   return (changes / total * 100).round(2)

def compute_volatility(pivot_df):
    # Shift values down to compare current and previous
    shifted = pivot_df.shift()
    
    # Only count changes where BOTH current and previous are not NaN
    valid = pivot_df.notna() & shifted.notna()
    changes = (pivot_df != shifted) & valid
    
    # Count total valid comparisons per column
    total_valid = valid.sum()
    change_count = changes.sum()
    
    return (change_count / total_valid * 100).round(2)



# Compute volatility
ip_volatility = compute_volatility(ip_pivot)
as_volatility = compute_volatility(as_pivot)

# Sort for top 5
most_volatile_ips = ip_volatility.sort_values(ascending=False)
most_volatile_ases = as_volatility.sort_values(ascending=False)

# Write to report
with open(report_file, "a") as f:
    f.write("--------------------------------------------------------------\n")
    #f.write("For destination: www.google.com\n")
    #f.write("For destination: www.cmu.edu\n")
    f.write("For destination: www.x.com\n")
    
    f.write("\nMost Volatile Hops:\n")
    f.write("Top 5 Most Volatile Router Hops (by IP change %):\n")
    for hop, vol in most_volatile_ips.head(5).items():
        f.write(f"Hop {hop}: {vol:.2f}%\n")

    f.write("\nTop 5 Most Volatile AS Hops (by AS change %):\n")
    for hop, vol in most_volatile_ases.head(5).items():
        f.write(f"Hop {hop}: {vol:.2f}%\n")

