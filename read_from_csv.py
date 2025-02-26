from fpdf import FPDF
import pandas as pd

# Function to read data from a file
def read_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Function to generate a PDF report
def generate_pdf(data, output_path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "Automated Data Report", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    for column in data.columns:
        pdf.cell(50, 10, column, border=1)
    pdf.ln()
    
    for index, row in data.iterrows():
        for value in row:
            pdf.cell(50, 10, str(value), border=1)
        pdf.ln()
    
    pdf.output(output_path)
    print(f"Report generated: {output_path}")

if __name__ == "__main__":
    file_path = r"C:\Users\Administrator\Downloads\sample_data.csv"  # Replace with your data file
    output_path = "generated_report.pdf"
    data = read_data(file_path)
    if data is not None:
        generate_pdf(data, output_path)
