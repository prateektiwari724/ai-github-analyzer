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
    if not text or len(text.strip()) == 0:
        return generate_default_summary()

    text = clean_text(text)

    # Split sentences
    sentences = re.split(r'(?<=[.!?]) +', text)

    # Light filtering (NOT aggressive)
    clean_sentences = []
    for s in sentences:
        s = s.strip()

        if len(s) < 25:
            continue

        # Only remove extreme garbage
        if any(x in s.lower() for x in ["license", "copyright"]):
            continue

        clean_sentences.append(s)

    # 🔥 FALLBACK SYSTEM (IMPORTANT FIX)
    if len(clean_sentences) < 3:
        clean_sentences = sentences[:8]

    if len(clean_sentences) == 0:
        return generate_default_summary()

    # Pick top sentences
    selected = clean_sentences[:6]

    return format_summary(selected)


def format_summary(sentences):
    # Safe extraction
    s0 = sentences[0] if len(sentences) > 0 else ""
    s1 = sentences[1] if len(sentences) > 1 else ""
    s2 = sentences[2] if len(sentences) > 2 else ""
    s3 = sentences[3] if len(sentences) > 3 else ""
    s4 = sentences[4] if len(sentences) > 4 else ""

    summary = f"""
Overview:
{s0}

Key Features:
- {s1}
- {s2}

Purpose:
{s3}

Additional Info:
{s4}
"""

    return summary.strip()


def generate_default_summary():
    return """
Overview:
This repository contains a software project hosted on GitHub.

Key Features:
- Provides core functionality based on its implementation.
- Designed to solve a specific problem or use case.

Purpose:
The project demonstrates development practices and technical implementation.

Additional Info:
Refer to the repository documentation for more details.
""".strip()