#!/bin/bash

# Configuration
LOG_DIR="/Users/Dina.Ding/Documents/02_Pittsburgh/Pittsburgh_Uni/Courses/2024-Spring/TELCOM2310_AppofNetworks/Project2-2/traceroute_logs"
mkdir -p "$LOG_DIR" || { echo "Failed to create log directory"; exit 1; }

DESTS=("www.google.com" "www.cmu.edu" "www.x.com")
MEASUREMENTS_PER_DAY=6   # measure 6 times per day
DAYS_TO_RUN=8            # measure 8 days

# Create output directories
mkdir -p "$LOG_DIR/raw_traceroute" || { echo "Failed to create raw_traceroute directory"; exit 1; }
mkdir -p "$LOG_DIR/as_tables" || { echo "Failed to create as_tables directory"; exit 1; }

# Function to get AS information (now handles all IPs including 0.0.0.0)
get_as_info() {
    local ip=$1
    if [[ "$ip" == "0.0.0.0" ]]; then
        printf "NA | 0.0.0.0 | NA | NA | NA | NA | Invalid/Unknown IP\n"
    else
        whois -h whois.cymru.com " -v $ip" 2>/dev/null | awk -F'|' '{
            gsub(/^[ \t]+|[ \t]+$/, "", $1);
            gsub(/^[ \t]+|[ \t]+$/, "", $2);
            gsub(/^[ \t]+|[ \t]+$/, "", $3);
            gsub(/^[ \t]+|[ \t]+$/, "", $4);
            gsub(/^[ \t]+|[ \t]+$/, "", $5);
            gsub(/^[ \t]+|[ \t]+$/, "", $6);
            gsub(/^[ \t]+|[ \t]+$/, "", $7);
            printf "%s | %s | %s | %s | %s | %s | %s\n", $1, $2, $3, $4, $5, $6, $7
        }' || printf "NA | $ip | NA | NA | NA | NA | Lookup Failed\n"
    fi
}

# Main measurement loop
for ((day=1; day<=$DAYS_TO_RUN; day++)); do
    for ((measurement=1; measurement<=$MEASUREMENTS_PER_DAY; measurement++)); do
        TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
        echo "Day $day, Measurement $measurement - $TIMESTAMP"
        
        for DEST in "${DESTS[@]}"; do
            # Create safe filename
            BASE_NAME=$(echo "$DEST" | sed 's/[^a-zA-Z0-9]/_/g')
            RAW_FILE="$LOG_DIR/raw_traceroute/${BASE_NAME}_${TIMESTAMP}.txt"
            AS_TABLE_FILE="$LOG_DIR/as_tables/${BASE_NAME}_${TIMESTAMP}_AS.txt"
            
            # Run traceroute (with increased hop limit)
            echo "Tracing route to $DEST..."
            echo "---------------------------------------------------------------------"
            traceroute -n -m 30 "$DEST" > "$RAW_FILE" 2>&1
            
            # Generate AS table with header
            {
                echo "AS table of $DEST..."
                echo "---------------------------------------------------------------------"
               # Extract IPs in hop order (skip first line containing destination)
                grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' "$RAW_FILE" | tail -n +2 | while read -r IP; do
                        get_as_info "$IP"
                done
            } > "$AS_TABLE_FILE"
            
            echo "Saved complete records for $DEST:"
            echo " - Raw traceroute: $RAW_FILE"
            echo " - AS table: $AS_TABLE_FILE"
        done
        
        # Space measurements 6 hours apart
        if [ $measurement -lt $MEASUREMENTS_PER_DAY ]; then
            echo "Waiting 4 hours until next measurement..."
            #sleep 21600 # 6 hours 4 times
            sleep 14400  #4 hours 6 times
        fi
    done
    
    # Wait until same time next day
    if [ $day -lt $DAYS_TO_RUN ]; then
        echo "Waiting until tomorrow..."
        sleep 86400
    fi
done

echo "All measurements completed!"
