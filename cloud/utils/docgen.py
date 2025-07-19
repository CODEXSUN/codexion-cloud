from pathlib import Path
import datetime

SUPPORTED_EXTENSIONS = ['.py', '.js', '.ts', '.jsx', '.tsx', '.php']

def get_comment_syntax(file_ext: str):
    if file_ext == '.py':
        return "#", ""
    elif file_ext in ['.js', '.ts', '.jsx', '.tsx']:
        return "/*", "*/"
    elif file_ext == '.php':
        return "/**", "*/"
    else:
        return "#", ""  # Fallback

def generate_header(file_path: Path, author: str, version: str = None) -> str:
    ext = file_path.suffix
    comment_start, comment_end = get_comment_syntax(ext)

    header_lines = []

    if comment_end:
        header_lines.append(f"{comment_start}")
    else:
        header_lines.append(f"{comment_start} File: {file_path.name}")

    if not comment_end:
        header_lines.append(f"{comment_start} Author: {author}")
        header_lines.append(f"{comment_start} Created: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        header_lines.append(f"{comment_start} Version: {version}")
    else:
        header_lines.append(f" File: {file_path.name}")
        header_lines.append(f" Author: {author}")
        header_lines.append(f" Created: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        header_lines.append(f" Version: {version}")
        header_lines.append(f"{comment_end}")

    header_lines.append("")  # Newline after header
    return '\n'.join(header_lines)

def add_header_to_file(file_path: Path, header: str):
    original_content = file_path.read_text(encoding="utf-8")
    if header.strip() in original_content:
        print(f"⚠️  Header already exists in: {file_path}")
        return
    updated_content = header + original_content
    file_path.write_text(updated_content, encoding="utf-8")
    print(f"✅ Header added to: {file_path}")

def main(target_dir: Path, author: str = "Sundar", version: str = "1.0.0"):
    for file_path in target_dir.rglob("*"):
        if file_path.suffix in SUPPORTED_EXTENSIONS and file_path.is_file():
            header = generate_header(file_path, author, version)
            add_header_to_file(file_path, header)

if __name__ == "__main__":
    import sys
    directory = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    main(directory)
