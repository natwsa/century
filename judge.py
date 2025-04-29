import json
from collections import defaultdict
from langchain_openai import ChatOpenAI


judge_model = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0
)

#Second LLM that judges performance of first
def judge_extraction(note, extracted_fields, judge_model):
    judgment_prompt = f"""
    You are an expert medical information auditor.

    Given a clinical note and extracted fields, evaluate whether each extracted field faithfully reflects the content of the clinical note.

    Rules:
    - Assign 1 if the field correctly reflects the note.
    - Assign 0 if the field is hallucinated, missing, or incorrect.
    - Respond strictly in JSON format like this: {{"field1": 1, "field2": 0}}

    Clinical Note:
    {note}

    Extracted Fields:
    {json.dumps(extracted_fields)}
    """
    try:
        response = judge_model.invoke(judgment_prompt)
        return json.loads(response.content.strip())
    except Exception as e:
        print(f"Error during judging: {e}")
        return None

# High-level JSON format check
def check_entry_format(entry):
    try:
        assert isinstance(entry.get("original_note"), str)
        assert isinstance(entry.get("extracted_fields"), dict)
        assert isinstance(entry.get("suspicious_fields"), list)
        return True

    except (AssertionError):
        return False

with open('clinical_notes_extracted.json', 'r') as f:
    extracted_data = json.load(f)

field_scores_accumulator = defaultdict(list)

for entry in extracted_data:
    note_text = entry['original_note']
    extracted_fields = entry['extracted_fields']

    field_scores = judge_extraction(note_text, extracted_fields, judge_model)

    if field_scores:
        for field, score in field_scores.items():
            field_scores_accumulator[field].append(score)

#Compute average judgement scores for each field
average_field_scores = {}
for field, scores in field_scores_accumulator.items():
    average = sum(scores) / len(scores) if scores else 0
    average_field_scores[field] = round(average, 3)  # Round nicely

print("Average Field Scores:")
for field, avg in average_field_scores.items():
    print(f"{field}: {avg:.3f}")

all_good = True

for entry in extracted_data:
    if not check_entry_format(entry):
        all_good = False
        break

if all_good:
    print("Notes extracted in expected format.")
else:
    print("Notes not extracted in expected format.")
