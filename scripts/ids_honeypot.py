import socket
import csv
import time
import threading
from datetime import datetime
import os

# Configuration
DATA_FILE = "data/live_threats.csv"
HONEY_PORTS = [8080, 8888, 9999]  # Trap ports. If anyone touches these, it's a threat.

def start_honeyport(port):
    """
    Listens on a specific port. If a connection occurs, it's treated as a CRITICAL threat.
    """
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', port))
        server.listen(5)
        print(f"🕸️  Honeyport active on port {port}...")
        
        while True:
            client_socket, addr = server.accept()
            ip = addr[0]
            
            # 🚨 INTRUSION DETECTED
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"🚨 [ALERT] Unauthorized connection to Honeyport {port} from {ip}!")
            
            # Log to CSV
            row = [
                timestamp,
                "Intrusion Attempt",
                ip,
                f"Trap_Port_{port}",
                "Critical",
                f"Unauthorized connection detected on Honeypot Port {port}"
            ]
            
            with open(DATA_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(row)
            
            # Send a fake warning response to the attacker (or user) so the browser shows something
            # Enhanced with UTF-8 charset and meaningful styling
            html_body = f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ background-color: #1a0000; color: #ff3333; font-family: 'Courier New', monospace; text-align: center; padding-top: 50px; }}
                    .alert-box {{ border: 4px solid #ff0000; display: inline-block; padding: 40px; background-color: #000; box-shadow: 0 0 20px #ff0000; }}
                    h1 {{ font-size: 48px; margin: 0; }}
                    p {{ font-size: 18px; color: #ffffff; }}
                    .ip {{ color: #ffff00; font-weight: bold; font-size: 24px; margin-top: 20px;}}
                </style>
            </head>
            <body>
                <div class="alert-box">
                    <h1>⚠️ SECURITY ALERT ⚠️</h1>
                    <p>UNAUTHORIZED ACCESS DETECTED</p>
                    <p>This is a restricted honeypot trap.</p>
                    <div class="ip">YOUR IP HAS BEEN LOGGED: {ip}</div>
                    <p>System Administrator has been notified.</p>
                </div>
            </body>
            </html>
            """
            
            # Construct HTTP response
            # Note: We must encode body to get correct length for Content-Length
            encoded_body = html_body.encode('utf-8')
            response_header = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Content-Length: {len(encoded_body)}\r\n"
                "\r\n"
            )
            
            client_socket.sendall(response_header.encode('utf-8') + encoded_body)
            time.sleep(0.5) # Allow browser to receive full payload
            
            # Close connection
            client_socket.close()
            
    except Exception as e:
        print(f"❌ Error on port {port}: {e}")

def main():
    print("🛡️  INTERNAL REAL-TIME INTRUSION DETECTION SYSTEM (IDS)")
    print("======================================================")
    print("mode: PRODUCTIVE (Honeypot Strategy)")
    print(f"scope: Monitoring local ports {HONEY_PORTS} for unauthorized scans.\n")
    
    threads = []
    for port in HONEY_PORTS:
        t = threading.Thread(target=start_honeyport, args=(port,))
        t.daemon = True
        t.start()
        threads.append(t)
        
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 IDS stopped.")

if __name__ == "__main__":
    # Ensure data file exists
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', newline='') as f:
            csv.writer(f).writerow(["Timestamp", "Threat_Type", "Source_IP", "Destination_IP", "Severity", "Description"])
            
    main()
