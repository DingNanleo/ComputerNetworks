import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

#report_file = "google_path_stability_report.txt"
#report_file = "cmu_path_stability_report.txt"
report_file = "x_path_stability_report.txt"

# Load the data
#df = pd.read_csv("google_raw_AS.csv")  # Change to your actual CSV filename
#df = pd.read_csv("cmu_raw_AS.csv")  # Change to your actual CSV filename
df = pd.read_csv("x_raw_AS.csv")  # Change to your actual CSV filename


# Fill missing values with a placeholder for grouping
df[['ip', 'AS']] = df[['ip', 'AS']].fillna('NA')

# Step 1: Group by timestamp and construct full router and AS paths
router_paths = df.groupby('timestamp')['ip'].apply(lambda x: tuple(x)).tolist()
as_paths = df.groupby('timestamp')['AS'].apply(lambda x: tuple(x)).tolist()

# Step 2: Count frequencies (histogram) of each unique path
router_path_counts = Counter(router_paths)
as_path_counts = Counter(as_paths)

# Step 3: Most common path (mode)
most_common_router_path, router_count = router_path_counts.most_common(1)[0]
most_common_as_path, as_count = as_path_counts.most_common(1)[0]

with open(report_file, "w") as f:
    #f.write("For destination: www.google.com\n")
    #f.write("For destination: www.cmu.edu\n")
    f.write("For destination: www.x.com\n")
    
    f.write("Most common router path (appeared {} times):\n".format(router_count))
    f.write(f"{most_common_router_path}\n\n")

    f.write("Most common AS path (appeared {} times):\n".format(as_count))
    f.write(f"{most_common_as_path}\n\n")

    f.write("Top 5 Router Paths:\n")
    for path, count in router_path_counts.most_common(5):
        f.write(f"{count} times: {path}\n")

    f.write("\nTop 5 AS Paths:\n")
    for path, count in as_path_counts.most_common(5):
        f.write(f"{count} times: {path}\n")

print(f"Report written to {report_file}")

# Plot histograms
def plot_histogram(path_counts, title):
    top_paths = path_counts.most_common(5)
    labels = [str(p[0]) for p in top_paths]
    values = [p[1] for p in top_paths]

    plt.figure(figsize=(10, 5))
    plt.barh(range(len(labels)), values, color='skyblue')
    plt.yticks(range(len(labels)), labels, fontsize=8)
    plt.xlabel("Frequency")
    plt.title(title)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

plot_histogram(router_path_counts, "Top 5 Most Common Router Paths")
plot_histogram(as_path_counts, "Top 5 Most Common AS Paths")
