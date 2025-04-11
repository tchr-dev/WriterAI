import yaml
from pathlib import Path

CHARACTER_FILE = Path("data/characters.yaml")


def load_characters():
    if CHARACTER_FILE.exists():
        with open(CHARACTER_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


def save_characters(characters):
    with open(CHARACTER_FILE, "w", encoding="utf-8") as f:
        yaml.dump(characters, f, allow_unicode=True)


def get_character(name):
    characters = load_characters()
    return characters.get(name)


def add_or_update_character(name, data):
    characters = load_characters()
    characters[name] = data
    save_characters(characters)


def delete_character(name):
    characters = load_characters()
    if name in characters:
        del characters[name]
        save_characters(characters)


def list_characters():
    return list(load_characters().keys())
