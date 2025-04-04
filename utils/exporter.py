def export_to_md(text: str, path: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
