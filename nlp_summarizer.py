import re

def clean_readme(text):
    if not text:
        return ""

    # Remove code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)

    # Remove markdown links/images
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)

    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # Remove special junk
    text = re.sub(r'[#>*_`]', '', text)

    # Remove file extensions & configs
    text = re.sub(r'\S+\.(png|jpg|svg|json|md)', '', text)

    # Clean spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def summarize_text(text):
    if not text:
        return "No description available."

    sentences = text.split('.')

    clean_sentences = []

    for s in sentences:
        s = s.strip()

        # ❌ Remove garbage sentences
        if len(s) < 40:
            continue
        if any(x in s.lower() for x in ["install", "clone", "npm", "pip", "config", "json"]):
            continue

        clean_sentences.append(s)

    if not clean_sentences:
        clean_sentences = sentences[:6]

    summary = ". ".join(clean_sentences[:5])

    return summary.strip() + "."