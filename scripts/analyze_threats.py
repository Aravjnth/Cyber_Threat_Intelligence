import pandas as pd
import os

# Path to CSV file
data_path = "data/historical_threats.csv"

# Check if CSV exists
if not os.path.exists(data_path):
    print(f"❌ ERROR: File not found at {data_path}")
    exit()

# Load dataset
df = pd.read_csv(data_path)

print("\n📊 CYBER THREAT INTELLIGENCE REPORT")
print("-" * 50)

# Total threat records
total_threats = len(df)
print(f"Total Threat Records: {total_threats}\n")

# Threat count by type
print("Threats by Type:")
threat_type_counts = df["Threat_Type"].value_counts()
for t, count in threat_type_counts.items():
    print(f"{t}: {count}")

# Severity distribution
print("\nSeverity Distribution:")
severity_counts = df["Severity"].value_counts()
for sev, count in severity_counts.items():
    print(f"{sev}: {count}")

# Critical threats only
critical_threats = df[df["Severity"].str.lower() == "critical"]
print(f"\n🚨 Total Critical Threats: {len(critical_threats)}")

# Save the report to logs folder
os.makedirs("logs", exist_ok=True)
log_file = "logs/threat_analysis.log"
with open(log_file, "w") as f:
    f.write("CYBER THREAT INTELLIGENCE REPORT\n")
    f.write("-" * 50 + "\n")
    f.write(f"Total Threat Records: {total_threats}\n\n")
    f.write("Threats by Type:\n")
    for t, count in threat_type_counts.items():
        f.write(f"{t}: {count}\n")
    f.write("\nSeverity Distribution:\n")
    for sev, count in severity_counts.items():
        f.write(f"{sev}: {count}\n")
    f.write(f"\nTotal Critical Threats: {len(critical_threats)}\n")

print(f"\n✅ Analysis complete. Report saved to {log_file}")
