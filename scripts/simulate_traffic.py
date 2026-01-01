import time
import csv
import random
from datetime import datetime
import os

# File to simulate real-time feed
DATA_FILE = "data/live_threats.csv"

# Threat definitions
THREAT_TYPES = ["Malware", "Phishing", "DDoS", "Brute Force", "Ransomware"]
SEVERITIES = ["Low", "Medium", "High", "Critical"]
DESCRIPTIONS = {
    "Malware": ["Trojan detected", "Spyware activity", "Worm propagation", "Rootkit found"],
    "Phishing": ["Suspicious email", "Fake login page", "Credential harvesting", "Spear phishing attempt"],
    "DDoS": ["SYN flood", "UDP flood", "Traffic spike detected", "HTTP flood"],
    "Brute Force": ["Multiple login failures", "SSH dictionary attack", "FTP unauthorized access", "RDP brute force"],
    "Ransomware": ["File encryption started", "Ransom note detected", "Shadow copy deletion", "Encrypted backup attempt"]
}

def generate_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def start_simulation():
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Initialize file with header if it doesn't exist
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Threat_Type", "Source_IP", "Destination_IP", "Severity", "Description"])
    
    print(f"🚀 Traffic simulation started.")
    print(f"Generated events will be written to: {os.path.abspath(DATA_FILE)}")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            threat_type = random.choice(THREAT_TYPES)
            
            # Weight severity: Ransomware is usually Critical
            if threat_type == "Ransomware":
                severity = "Critical"
            else:
                # 10% Critical, 20% High, 30% Medium, 40% Low
                rand_val = random.random()
                if rand_val < 0.1:
                    severity = "Critical"
                elif rand_val < 0.3:
                    severity = "High"
                elif rand_val < 0.6:
                    severity = "Medium"
                else:
                    severity = "Low"
                
            row = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                threat_type,
                generate_ip(),
                generate_ip(),
                severity,
                random.choice(DESCRIPTIONS[threat_type])
            ]
            
            with open(DATA_FILE, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(row)
                
            # Visual feedback in generator console too
            status_icon = "🔴" if severity == "Critical" else "🟡" if severity == "High" else "🟢"
            print(f"{status_icon} [{row[0]}] Generated: {threat_type} ({severity})")
            
            # Random delay between 1 and 4 seconds
            time.sleep(random.uniform(1, 4))
            
    except KeyboardInterrupt:
        print("\n🛑 Simulation stopped.")

if __name__ == "__main__":
    start_simulation()
