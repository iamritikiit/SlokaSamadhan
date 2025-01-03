import PyPDF2
import pandas as pd

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    text = []
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text.append(page.extract_text())
    return text

# Function to clean the extracted text
def clean_text(text):
    cleaned_lines = []
    for line in text.splitlines():
        line = line.strip()  # Remove extra spaces
        if line and not line.isdigit():  # Ignore empty lines and page numbers
            cleaned_lines.append(line)
    return cleaned_lines

# Main process
def pdf_to_csv(pdf_path, csv_path):
    raw_text = extract_text_from_pdf(pdf_path)
    all_cleaned_data = []

    for page in raw_text:
        cleaned_data = clean_text(page)
        all_cleaned_data.extend(cleaned_data)

    # Save to CSV
    df = pd.DataFrame(all_cleaned_data, columns=["Verse"])
    df.to_csv(csv_path, index=False)
    print(f"Data saved to {csv_path}")

# Input PDF file and output CSV file
pdf_file = "path_to_bhagavad_gita.pdf"
csv_file = "output_bhagavad_gita.csv"

pdf_to_csv(pdf_file, csv_file)

