import re

def clean_readme(text):
    # Remove images, links, HTML, code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'[#>*`]', '', text)

    return text.strip()


def extract_sections(text):
    lines = text.split("\n")

    overview = []
    features = []
    usage = []

    current_section = "overview"

    for line in lines:
        l = line.lower()

        if "feature" in l:
            current_section = "features"
            continue
        elif "usage" in l or "how to" in l:
            current_section = "usage"
            continue

        if len(line.strip()) < 20:
            continue

        if current_section == "overview":
            overview.append(line.strip())
        elif current_section == "features":
            features.append(line.strip())
        elif current_section == "usage":
            usage.append(line.strip())

    return overview, features, usage


def summarize_text(readme):
    if not readme or len(readme) < 50:
        return {
            "overview": "This repository does not contain enough documentation.",
            "features": ["Not enough data available"],
            "purpose": "Unknown",
            "additional": "No additional information found"
        }

    clean_text = clean_readme(readme)

    overview, features, usage = extract_sections(clean_text)

    # ---------- OVERVIEW ----------
    overview_text = " ".join(overview[:3])
    if not overview_text:
        overview_text = clean_text[:200]

    # ---------- FEATURES ----------
    if not features:
        features = re.split(r'\.', clean_text)[2:6]

    features = [f.strip() for f in features if len(f.strip()) > 20][:5]

    # ---------- PURPOSE ----------
    purpose = overview[1] if len(overview) > 1 else "This project provides useful functionality."

    # ---------- ADDITIONAL ----------
    additional = usage[0] if usage else "Refer to the repository for more details."

    return {
        "overview": overview_text,
        "features": features,
        "purpose": purpose,
        "additional": additional
    }