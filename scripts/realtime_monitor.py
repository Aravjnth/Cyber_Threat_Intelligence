import time
import os
import sys

DATA_FILE = "data/live_threats.csv"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def monitor_threats():
    clear_screen()
    print("🛡️  INITIALIZING REAL-TIME THREAT MONITOR SYSTEM")
    print("================================================")
    print(f"📡  Listening to feed: {DATA_FILE}")
    print("⏳  Waiting for live data stream...\n")

    # Wait for file to actuly exist
    while not os.path.exists(DATA_FILE):
        time.sleep(1)

    # Open the file
    with open(DATA_FILE, "r") as f:
        # Move pointer to the end of the file to ignore old data
        f.seek(0, os.SEEK_END)

        try:
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.5) # Wait for new data
                    continue

                # Process new line
                parts = line.strip().split(",")
                # Ensure we have enough columns (handling potential empty lines or malformed data)
                if len(parts) < 6:
                    continue
                
                timestamp, threat_type, src_ip, dst_ip, severity, desc = parts
                
                # skip header if it appears
                if timestamp == "Timestamp":
                    continue

                # Formatted Output based on Severity
                if severity.lower() == "critical":
                    print("\n" + "!" * 60)
                    print(f"🚨🚨 CRITICAL SECURITY ALERT DETECTED 🚨🚨")
                    print(f"⏰  Time       : {timestamp}")
                    print(f"🦠  Threat     : {threat_type.upper()}")
                    print(f"🔥  Severity   : CRITICAL")
                    print(f"📝  Details    : {desc}")
                    print(f"🌐  Source IP  : {src_ip}")
                    print(f"🎯  Target IP  : {dst_ip}")
                    print("!" * 60 + "\n")
                    
                    # Optional: Simulate a sound beep
                    print('\a') 
                    
                elif severity.lower() == "high":
                    print(f"⚠️   [HIGH] {timestamp} | {threat_type}: {desc} (Src: {src_ip})")
                    
                elif severity.lower() == "medium":
                    print(f"🔸  [MED ] {timestamp} | {threat_type}: {desc}")
                    
                else:
                    print(f"🔹  [LOW ] {timestamp} | {threat_type} detected.")

        except KeyboardInterrupt:
            print("\n🛑 Monitor system shutdown.")

if __name__ == "__main__":
    monitor_threats()
