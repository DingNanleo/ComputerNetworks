import csv
import re
import os

# Paths
csv_file = 'x_rawtraceroute.csv'  # The input CSV file containing traceroute data
as_dir = ("/Users/Dina.Ding/Documents"
    "/02_Pittsburgh/Pittsburgh_Uni/Courses/"
    "2024-Spring/TELCOM2310_AppofNetworks/"
    "Project2-2/traceroute_logs/as_tables/")
output_csv = 'x_raw_AS.csv'  # Output CSV file with appended AS info


# Step 1: Read the AS data and create a mapping for each IP to its AS information
def read_as_data(as_file):
    ip_to_as_info = {}
    with open(as_file, 'r') as file:
        for line in file:
            if '|' not in line or line.startswith('AS |'):  # skip headers or dividers
                continue
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 7:
                ip = parts[1]
                ip_to_as_info[ip] = parts[:7]  # all fields: AS, IP, Prefix, CC, Registry, Allocated, Name
    return ip_to_as_info

# Step 2: Process the CSV file to append AS information
def process_csv_with_as_info(csv_file, as_dir, output_csv):
    # Read the original CSV
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # Define new field names for AS info
    as_fields = ['AS', 'AS IP', 'BGP Prefix', 'CC', 'Registry', 'Allocated', 'AS Name']
    fieldnames = reader.fieldnames + as_fields


    # Write the output CSV with added header
    with open(output_csv, mode='w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Step 3: Process each row and append the AS information
        for row in rows:
            timestamp = row['timestamp']
            ip = row['ip']
            as_file = os.path.join(as_dir, f"www_cmu_edu_{timestamp}_as.txt")


            # Default AS info (all NA)
            as_info = ['NA'] * 7
            
            if os.path.exists(as_file):
                ip_to_as_info = read_as_data(as_file)
                if ip in ip_to_as_info:
                    as_info = ip_to_as_info[ip]

            # Add AS fields to the row
            for key, value in zip(as_fields, as_info):
                row[key] = value

            # Step 4: Write row to the output CSV
            writer.writerow(row)

    print(f"Output written to {output_csv}")

# Run the function
process_csv_with_as_info(csv_file, as_dir, output_csv)
