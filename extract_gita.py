import PyPDF2
import pandas as pd
import re

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    text = []
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text.append(page.extract_text())
    return text

# Function to process and structure the slokas
def process_gita_text(text):
    chapter_num = None
    sloka_num = None
    sloka = ""
    explanation = ""
    data = []

    for line in text.splitlines():
        line = line.strip()

        # Detect chapter
        chapter_match = re.match(r'Chapter\s(\d+)', line, re.IGNORECASE)
        if chapter_match:
            chapter_num = int(chapter_match.group(1))
            continue

        # Detect sloka number
        sloka_match = re.match(r'Verse\s(\d+)', line, re.IGNORECASE)
        if sloka_match:
            if sloka:  # Save previous sloka
                data.append([chapter_num, sloka_num, sloka.strip(), explanation.strip()])
                sloka = ""
                explanation = ""
            sloka_num = int(sloka_match.group(1))
            continue

        # Accumulate sloka text
        if sloka_num and not line.startswith("Verse"):
            if line.isupper():
                explanation += line + " "
            else:
                sloka += line + " "

    # Append the last sloka
    if sloka:
        data.append([chapter_num, sloka_num, sloka.strip(), explanation.strip()])

    return data

# Main process
def pdf_to_csv(pdf_path, csv_path):
    raw_text = extract_text_from_pdf(pdf_path)
    all_data = []

    for page in raw_text:
        structured_data = process_gita_text(page)
        all_data.extend(structured_data)

    # Save to CSV
    df = pd.DataFrame(all_data, columns=["Chapter", "Sloka Number", "Sloka", "Explanation"])
    df.to_csv(csv_path, index=False)
    print(f"Data saved to {csv_path}")

# Input PDF file and output CSV file
pdf_file = "/Users/ritik/Downloads/English-Bhagavad-gita-His-Divine-Grace-AC-Bhaktivedanta-Swami-Prabhupada.pdf"
csv_file = "/Users/ritik/Desktop/SlokaSamadhan/output_gita.csv"

pdf_to_csv(pdf_file, csv_file)
