import win32evtlog
import win32con
import win32evtlogutil
import time
import csv
import os
import re
import socket
from datetime import datetime

# Central file where all threats are logged
DATA_FILE = "data/live_threats.csv"

# Security Event ID for "Audit Failure" (Failed Login)
FAILED_LOGIN_ID = 4625

def watch_logs():
    server = 'localhost'
    log_type = 'Security'
    fallback_mode = False
    
    print("🛡️  WINDOWS LOG MONITOR STARTED")
    
    # Try to open Security Log
    try:
        hand = win32evtlog.OpenEventLog(server, log_type)
        print(f"📡 Watching {log_type} log for Failed Logins (Event ID 4625)...")
    except Exception as e:
        if "privilege" in str(e).lower() or "access is denied" in str(e).lower():
            print(f"⚠️  Access Denied to 'Security' Log (Run as Admin to scan logins).")
            print(f"🔄 Fallback: Switching to 'Application' Log to scan for System Errors...")
            log_type = 'Application'
            fallback_mode = True
            hand = win32evtlog.OpenEventLog(server, log_type)
        else:
            raise e

    print("Press Ctrl+C to stop.\n")
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    
    try:
        while True:
            events = win32evtlog.ReadEventLog(hand, flags, 0)
            if events:
                for event in events:
                    # MODE A: Security Log (Failed Logins)
                    if not fallback_mode and event.EventID == FAILED_LOGIN_ID:
                        process_security_event(event)

                    # MODE B: Application Log (Errors/Warnings)
                    elif fallback_mode and event.EventType == win32con.EVENTLOG_ERROR_TYPE:
                        process_application_event(event)
                        
            time.sleep(1) # Poll every second
            
    except KeyboardInterrupt:
        print("\n🛑 Monitor stopped.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def process_security_event(event):
    msg = win32evtlogutil.SafeFormatMessage(event, 'Security')
    timestamp_fmt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Regex for IP
    ip_match = re.search(r"Source Network Address:\s+([0-9.]+)", msg)
    source_ip = ip_match.group(1) if ip_match else "Unknown"
    
    log_threat(timestamp_fmt, "Brute Force", source_ip, "High", "Windows Logon Failed")
    print(f"⚠️  [SECURITY] Failed Login from {source_ip}")

def process_application_event(event):
    # Only capture recent events (last 5 seconds) to avoid spamming old logs
    # Note: Real implementation would check event.TimeGenerated, but for demo we just process
    # what we read. To avoid flooding from backlog, we could check timestamps.
    # For now, let's just log it.
    
    # Ignore if event is too old (e.g. older than 1 minute)
    delta = datetime.now() - event.TimeGenerated
    if delta.total_seconds() > 60:
        return

    try:
        msg = win32evtlogutil.SafeFormatMessage(event, 'Application')
        # Clean message
        msg = msg.split('\r')[0] if msg else "Unknown Application Error"
    except:
        msg = "Unknown Application Error"
        
    timestamp_fmt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Map Event ID to a "Threat Type" for fun
    log_threat(timestamp_fmt, "System Error", "Localhost", "Medium", f"App Crash: {event.SourceName}")
    print(f"🔸 [SYSTEM] Application Error detected: {event.SourceName}")

def log_threat(timestamp, t_type, source, severity, desc):
    row = [timestamp, t_type, source, "Localhost", severity, desc]
    with open(DATA_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row)

if __name__ == "__main__":
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', newline='') as f:
            csv.writer(f).writerow(["Timestamp", "Threat_Type", "Source_IP", "Destination_IP", "Severity", "Description"])

    watch_logs()
