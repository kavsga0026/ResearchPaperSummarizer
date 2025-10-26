import re

# contains common headings of research papers 
HEADERS = {
    "abstract": r"\babstract\b",
    "introduction": r"\bintroduction\b|\bbackground\b",
    "methodology": r"\bmethodology\b|\bmethods\b|\bmaterials and methods\b",
    "results": r"\bresults\b|\bfindings\b",
    "discussion": r"\bdiscussion\b|\bresults and discussion\b",
    "conclusion": r"\bconclusion\b|\bconclusions\b|\bsummary\b",
    "references": r"\breferences\b|\bbibliography\b"
}

def extract_sections(text: str) -> dict:
    # converting the entire text to lower 
    low = text.lower()
    spans = []
    for name, pat in HEADERS.items():
        for m in re.finditer(pat, low):
            spans.append((m.start(), name))
    spans.sort(key=lambda x: x[0])

    # If no headers are found,we return 
    if not spans:
        return {}

    sections = {}
    for i, (start_idx, name) in enumerate(spans):
        end_idx = spans[i+1][0] if i + 1 < len(spans) else len(text)
        content = text[start_idx:end_idx].strip()
        sections[name] = content

    picked = {}

    def pick_first_of(keys):
        for k in keys:
            if k in sections and len(sections[k].split()) > 30:
                return sections[k]
        return None

    abstract = pick_first_of(["abstract", "introduction"])
    methodology = pick_first_of(["methodology", "methods"])
    conclusion = pick_first_of(["conclusion", "discussion", "results"])

    if abstract: picked["abstract"] = abstract
    if methodology: picked["methodology"] = methodology
    if conclusion: picked["conclusion"] = conclusion

    return picked
