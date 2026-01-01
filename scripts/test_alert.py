import csv
import time
from datetime import datetime

DATA_FILE = "data/live_threats.csv"

def inject_test():
    print("🔫 INJECTING TEST THREAT...")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [
        timestamp,
        "TEST_ATTACK",
        "192.168.1.100",
        "Server_01",
        "Critical",
        "🚨 THIS IS A MANUAL TEST ALERT to verify dashboard connectivity"
    ]
    
    with open(DATA_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row)
        
    print(f"✅ Threat Injected: {row}")
    print("👀 Check your Dashboard now!")

if __name__ == "__main__":
    inject_test()
