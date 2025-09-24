import spacy
import re

nlp = spacy.load("en_core_web_sm")

# Small condition dictionary
CONDITIONS = {
    "diabetes": ["diabetes", "diabetic"],
    "hypertension": ["hypertension", "high blood pressure"],
    "asthma": ["asthma"],
    "insulin": ["insulin"],
}

def extract_condition(text: str):
    text_l = text.lower()
    for cond, variants in CONDITIONS.items():
        for v in variants:
            if v in text_l:
                return cond
    return None

def extract_age(text: str):
    # Match "over 50" / "under 40"
    if m := re.search(r'over (\d+)', text.lower()):
        return ("gt", int(m.group(1)))
    if m := re.search(r'under (\d+)', text.lower()):
        return ("lt", int(m.group(1)))
    # detect any number as age
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "CARDINAL" and ent.text.isdigit():
            return (None, int(ent.text))
    return (None, None)

def parse_query(text: str):
    condition = extract_condition(text)
    op, age = extract_age(text)

    parts = []
    if condition: parts.append(f"condition={condition}")
    if age: 
        if op == "gt": parts.append(f"age=gt{age}")
        elif op == "lt": parts.append(f"age=lt{age}")
        else: parts.append(f"age={age}")
    fhir_request = "GET /Patient?" + "&".join(parts) if parts else "GET /Patient"
    return {"condition": condition, "age_op": op, "age": age, "fhir_request": fhir_request}

def simulate_patients(parsed):
    data = [
        {"name": "Ali Rahman", "age": 62, "condition": "diabetes"},
        {"name": "Sadia Akter", "age": 54, "condition": "diabetes"},
        {"name": "Raihan Khan", "age": 45, "condition": "hypertension"},
        {"name": "Mina Akther", "age": 34, "condition": "asthma"},
    ]
    cond = parsed["condition"]
    op = parsed["age_op"]
    age = parsed["age"]
    results = []
    for p in data:
        cond_ok = cond is None or p["condition"] == cond
        age_ok = True
        if age:
            if op == "gt": age_ok = p["age"] > age
            elif op == "lt": age_ok = p["age"] < age
            else: age_ok = p["age"] == age
        if cond_ok and age_ok:
            results.append(p)
    return results
