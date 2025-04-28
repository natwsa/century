from openai import OpenAI
import os
import json

# Set your OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extractor(note):
    prompt = f"""
    You are an expert clinical data extractor.
    Extract the following fields from the clinical note below into JSON format. Strictly return only valid JSON, with no explanation, no extra text.

    Fields:
    - patient_name
    - age
    - gender
    - reason for visit
    - allergies (as a list)
    - medications (as a list)
    - lab_results (as a list)
    - next steps

    If a field is missing, use an empty list `[]` or `null`.

    Clinical Note:
    {note}

    Strictly output JSON, and nothing else.
    """


    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You extract structured fields from clinical notes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        # Extract the JSON part
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"Error: {e}")
        return None

