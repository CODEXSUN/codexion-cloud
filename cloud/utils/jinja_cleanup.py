import re

def postprocess_rendered(content: str) -> str:
    """
    Cleans Jinja-rendered output:
    - Converts custom {# r #} into blank lines
    - Removes all other Jinja comments
    - Normalizes blank lines
    - Trims trailing spaces per line
    """
    # Replace custom blank line marker
    content = re.sub(r"{#\s*r\s*#}", "@@B@@", content)

    # Remove all other Jinja comments
    content = re.sub(r"{#.*?#}", "", content, flags=re.DOTALL)

    # Convert placeholders to actual blank lines
    content = content.replace('@@B@@', '\n')

    # Normalize excessive blank lines (3+ → 2)
    content = re.sub(r'\n{3,}', '\n\n', content)

    # Remove trailing spaces from each line
    lines = [line.rstrip() for line in content.splitlines()]
    cleaned = "\n".join(lines)

    return cleaned.strip() + "\n"  # Ensure exactly one final newline