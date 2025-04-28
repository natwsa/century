import pandas as pd
from openai import OpenAI
import os
import json
import time
from extraction import extractor
from hallucinations import validator

# Load the Excel file
file_path = 'your_filepath'
df = pd.read_excel(file_path)

# Set your OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

extracted_data = []

#Extract key fields for each note
for idx, row in df.iterrows():
    note_text = row['note']
    extracted_fields = extractor(note_text)

    if extracted_fields:
        extracted_data.append({
            "original_note": note_text,
            "extracted_fields": extracted_fields
        })
    time.sleep(1)  # Avoid API rate limits

# Save results to JSON file
output_path = 'clinical_notes_extracted.json'
with open(output_path, 'w') as f:
    json.dump(extracted_data, f, indent=2)

#Search for hallucinations
for entry in extracted_data:
    note_text = entry['original_note']
    fields = entry['extracted_fields']

    suspicious = validator(note_text, fields)
    entry['suspicious_fields'] = suspicious

output_path = 'clinical_notes_extracted.json'
with open(output_path, 'w') as f:
    json.dump(extracted_data, f, indent=2)

print(f"Extraction and validation complete! Saved to {output_path}")
