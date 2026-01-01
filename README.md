Cyber Threat Intelligence (CTI) Platform Type: Host-Based Intrusion Detection System (HIDS) & Network Honeypot Purpose: To monitor, detect, and visualize cyber security threats in real-time on a production system. This project has evolved from a simple historical data analyzer into a live, production-ready security system that actively protects your local machine. It acts as a mini Security Operations Center (SOC).

🏗️ System Architecture (How it Works)
The system follows a classic Sensor → Storage → Dashboard pipeline:

[ SENSORS (Detection) ]       [ STORAGE (Database) ]       [ INTERFACE (Visualization) ]
1. Windows Log Monitor  ---->                        ---->  1. Web Dashboard (Streamlit)
   (Internal Health)         |                      |       (Visual Charts & Metrics)
                             | data/live_threats.csv|
2. Network Honeypot     ---->| (Central Data Feed)  |---->  2. Terminal Monitor
   (External Traps)          |                      |       (Instant Text Alerts)
                                                    |
                                                     ---->  3. PDF Reporter
                                                            (Documentation)
🧩 Module Breakdown
1. 🔍 The Detection Layer (Active Sensors)
These scripts run in the background, constantly watching for signs of attack.

scripts/ids_honeypot.py
 (The Trap):
Role: Network Intrusion Detection.
Function: Opens "Trap Ports" (8080, 8888, 9999) that mimic vulnerable services.
Behavior: If a hacker or scanner connects, it triggers a CRITICAL ALERT, logs the attacker's IP, and serves a warning HTML page ("⚠️ SECURITY ALERT") to scare them off.
scripts/monitor_windows_log.py
 (The Watchdog):
Role: System Health & Security Monitoring.
Function: Connects to the Windows Log API.
Behavior: Watches for Failed Logins (Brute Force) (requires Admin) or Application Crashes (standard mode). It serves as a health monitor for your internal system.
2. 💾 The Data Layer (Storage)
data/live_threats.csv
:
Role: Central "Source of Truth."
Function: A lightweight, real-time append-only database. All sensors write to this file simultaneously, and all dashboards read from it. It allows different parts of the system to communicate without complex servers.
3. 🖥️ The Visualization Layer (SOC Dashboard)
scripts/dashboard.py
:
Technology: Streamlit (Python Web Framework).
Role: Real-Time Situation Awareness.
Features:
Live Metrics: Counters for Total Threats and Critical Incidents.
Auto-Updating Charts: Bar charts for Severity and Donut charts for Threat Types.
Incident Feed: A scrolling table of the most recent attacks.
scripts/realtime_monitor.py
:
Role: Low-latency alerts.
Features: Displays flashes of Red/Yellow text in the command line immediately when a new line is added to the CSV.
4. 📄 The Reporting Layer
scripts/generate_pdf_report.py
:
Role: Post-Incident Documentation.
Function: Generates professional PDF reports summarizing all threats found in the CSV, useful for management reviews or forensic analysis.
🚀 Key Technologies Used
Python: The core programming language.
Streamlit: For the interactive web dashboard.
Socket Programming: For creating the custom Honeypot TCP servers.
PyWin32: For interfacing with the Windows Event Log API.
Pandas & Altair: For data processing and visualization.
