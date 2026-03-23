import re

def clean_text(text):
    # Remove code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)

    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)

    # Remove markdown symbols
    text = re.sub(r'[#>*`]', '', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def summarize_text(text):
    text = clean_text(text)

    sentences = re.split(r'(?<=[.!?]) +', text)

    clean_sentences = []

    for s in sentences:
        s = s.strip()

        # Remove garbage lines
        if len(s) < 40:
            continue

        if any(x in s.lower() for x in [
            "install", "clone", "npm", "pip", "config",
            "json", "license", "copyright"
        ]):
            continue

        clean_sentences.append(s)

    # Fallback if too much removed
    if len(clean_sentences) < 3:
        clean_sentences = sentences[:6]

    # Pick top sentences
    selected = clean_sentences[:6]

    # 🧠 STRUCTURED OUTPUT
    summary = f"""
Overview:
{selected[0] if len(selected) > 0 else ""}

Key Features:
- {selected[1] if len(selected) > 1 else ""}
- {selected[2] if len(selected) > 2 else ""}

Purpose:
{selected[3] if len(selected) > 3 else ""}

Additional Info:
{selected[4] if len(selected) > 4 else ""}
"""

    return summary.strip()