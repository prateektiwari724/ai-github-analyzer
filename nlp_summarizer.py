def detect_tech_stack(readme, language):

    stack = set()
    text = readme.lower()

    # Tech keywords
    mapping = {
        "react": "React",
        "vue": "Vue",
        "angular": "Angular",
        "node": "Node.js",
        "express": "Express",
        "django": "Django",
        "flask": "Flask",
        "fastapi": "FastAPI",
        "spring": "Spring",
        "tensorflow": "TensorFlow",
        "pytorch": "PyTorch",
        "flutter": "Flutter",
        "vscode": "VS Code Extension",
    }

    for key, value in mapping.items():
        if key in text:
            stack.add(value)

    # Language fallback
    if language:
        stack.add(language)

    return list(stack)


def detect_project_type(readme):

    text = readme.lower()

    if "extension" in text and "vscode" in text:
        return "Developer Tool"

    if "flutter" in text or "mobile app" in text:
        return "Mobile App"

    if "website" in text or "documentation" in text or "docs" in text:
        return "Web Platform"

    if "api" in text or "backend" in text:
        return "Backend API"

    if "machine learning" in text or "artificial intelligence" in text:
        return "AI System"

    return "Software Project"


def detect_architecture(project_type):

    mapping = {
        "Mobile App": "Mobile Architecture",
        "Web Platform": "Frontend Web Architecture",
        "Backend API": "Backend / API Architecture",
        "AI System": "ML / AI Architecture",
        "Developer Tool": "Tooling / Extension Architecture",
        "Software Project": "General Architecture"
    }

    return mapping.get(project_type, "General Architecture")


def generate_summary(repo, project_type, language, tech_stack, readme):

    tech = ", ".join(tech_stack)

    # Extract first meaningful line from README
    lines = readme.split("\n")
    description = ""

    for line in lines:
        if len(line.strip()) > 30:
            description = line.strip()
            break

    return f"""{repo} is a {project_type} developed using {language}.

{description}

Tech Stack: {tech}

This project is designed to solve practical problems and enhance developer productivity.
"""