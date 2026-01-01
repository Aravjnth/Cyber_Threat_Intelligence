from fpdf import FPDF
import pandas as pd
import os

# Path to CSV file
data_path = "data/historical_threats.csv"
pdf_file = "reports/threat_report.pdf"

# Check if CSV exists
if not os.path.exists(data_path):
    print(f"❌ CSV file not found: {data_path}")
    exit()

# Load dataset
df = pd.read_csv(data_path)

# Create reports folder if not exists
os.makedirs("reports", exist_ok=True)

# Prepare analysis
total_threats = len(df)
threat_type_counts = df["Threat_Type"].value_counts()
severity_counts = df["Severity"].value_counts()
critical_threats = df[df["Severity"].str.lower() == "critical"]

# Create PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Header
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "CYBER THREAT INTELLIGENCE REPORT", ln=True, align="C")
pdf.ln(10)

# Total threats
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 8, f"Total Threat Records: {total_threats}", ln=True)
pdf.ln(5)

# Threats by type
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 8, "Threats by Type:", ln=True)
pdf.set_font("Arial", "", 12)
for t, count in threat_type_counts.items():
    pdf.cell(0, 8, f"{t}: {count}", ln=True)
pdf.ln(5)

# Severity distribution with colors
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 8, "Severity Distribution:", ln=True)
pdf.ln(2)
pdf.set_font("Arial", "", 12)
for sev, count in severity_counts.items():
    if sev.lower() == "critical":
        pdf.set_text_color(255, 0, 0)  # Red
    elif sev.lower() == "high":
        pdf.set_text_color(255, 140, 0)  # Orange
    else:
        pdf.set_text_color(0, 0, 0)  # Black
    pdf.cell(0, 8, f"{sev}: {count}", ln=True)

pdf.set_text_color(0, 0, 0)  # Reset to black
pdf.ln(5)

# Critical threats
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 8, f"Total Critical Threats: {len(critical_threats)}", ln=True)

# Save PDF
pdf.output(pdf_file)
print(f"✅ PDF report generated at {pdf_file}")
