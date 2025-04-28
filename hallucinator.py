def validator(note_text, extracted_fields):
    note_lower = note_text.lower()
    suspicious_fields = []

    #Search for hallucinated words
    for key, value in extracted_fields.items():
        if isinstance(value, str) and value.lower() not in note_lower:
            suspicious_fields.append(key)
        elif isinstance(value, list):
            for item in value:
                if item.lower() not in note_lower:
                    suspicious_fields.append(key)
                    break

    return suspicious_fields
