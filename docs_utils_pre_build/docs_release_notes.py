import re
import requests
from datetime import datetime
from pathlib import Path
import shutil

release_notes_api_url = "https://api.github.com/repos/mauro-andre/pyodmongo/releases"
release_notes = requests.get(url=release_notes_api_url).json()

en_file_path = Path().absolute() / ".docs_tmp" / "en" / "release_notes.md"
pt_file_path = Path().absolute() / ".docs_tmp" / "pt-BR" / "release_notes.md"


def convert_text(input_text):
    pattern = r"(@[\w-]+) in (\S+)"

    def replace_link(match):
        name = match.group(1)
        url = match.group(2)
        return f'<a href="{url}" target="_blank">{name}</a>'

    converted_text = re.sub(pattern, replace_link, input_text)
    return converted_text


with open(en_file_path, "w") as file:
    file.write("# <center>Release notes</center> #\n\n")
    for release_note in release_notes:
        name = release_note.get("name")
        published_at = datetime.fromisoformat(
            release_note.get("published_at")
        ).strftime("%Y-%m-%d")
        body: str = release_note.get("body")
        body = convert_text(body)
        body = body.replace("\n", "\n\n")
        file.write("---\n")
        file.write(f"## {name} - {published_at}\n")
        file.write(f"{body}\n\n")

shutil.copy(en_file_path, pt_file_path)
