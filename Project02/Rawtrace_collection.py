import re
import csv
import os


# Read the traceroute text
directory= "/Users/Dina.Ding/Documents/02_Pittsburgh/Pittsburgh_Uni/Courses/2024-Spring/TELCOM2310_AppofNetworks/Project2-2/traceroute_logs/raw_traceroute/"
output_file = "google_rawtraceroute.csv"

# Prepare output data
rows = []

# Step 1: Gather matching filenames and their timestamps
files_with_timestamps = []
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        match = re.match(r"www_google_com_(\d{8}_\d{6})\.txt$", filename)
        if match:
            timestamp = match.group(1)
            files_with_timestamps.append((timestamp, filename))

# Step 2: Sort files by timestamp
files_with_timestamps.sort()

# Step 3: Process each file in order
for timestamp, filename in files_with_timestamps:
    input_file = os.path.join(directory, filename)
    last_hop = None
    
    with open(input_file, "r") as file:
        for line in file:
            # Match hop number
            #hop_match = re.match(r"^\s*(\d+)\s+(\d{1,3}(?:\.\d{1,3}){3})", line)
            hop_match = re.match(r"^\s*(\d+)\s", line)
            if hop_match:
                hop = int(hop_match.group(1))
                last_hop = hop  # Update last seen hop
            elif last_hop is not None:
                hop = last_hop  # Reuse last seen hop if current line doesn't have a hop number
            else:
                continue  # If no hop yet, skip line
            

            # Extract all IPs and RTTs
            ip_match = re.search(r"(\d{1,3}(?:\.\d{1,3}){3})", line)
            ip = ip_match.group(1) if ip_match else "NA"

            rtt_matches = re.findall(r"(\d+\.\d+)\s*ms", line)
            rtt1 = rtt_matches[0] if len(rtt_matches) > 0 else "NA"
            rtt2 = rtt_matches[1] if len(rtt_matches) > 1 else "NA"
            rtt3 = rtt_matches[2] if len(rtt_matches) > 2 else "NA"

            # Collect the row
            rows.append([timestamp, hop, ip, rtt1, rtt2, rtt3])
       

with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["timestamp", "hop", "ip", "rtt1", "rtt2", "rtt3"])
        writer.writerows(rows)
        

print("Traceroute data has been written to traceroute.csv")
