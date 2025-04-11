import json
from pathlib import Path
from typing import List, Dict, Optional


class Scene:
    def __init__(self, title: str, content: str = ""):
        self.title = title
        self.content = content

    def to_dict(self):
        return {"title": self.title, "content": self.content}

    @staticmethod
    def from_dict(data):
        return Scene(title=data["title"], content=data.get("content", ""))


class Chapter:
    def __init__(self, title: str, scenes: Optional[List[Scene]] = None):
        self.title = title
        self.scenes = scenes or []

    def to_dict(self):
        return {
            "title": self.title,
            "scenes": [scene.to_dict() for scene in self.scenes]
        }

    @staticmethod
    def from_dict(data):
        scenes = [Scene.from_dict(s) for s in data.get("scenes", [])]
        return Chapter(title=data["title"], scenes=scenes)


class Character:
    def __init__(self, name: str, description: str = "", traits: Optional[List[str]] = None):
        self.name = name
        self.description = description
        self.traits = traits or []

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "traits": self.traits
        }

    @staticmethod
    def from_dict(data):
        return Character(
            name=data["name"],
            description=data.get("description", ""),
            traits=data.get("traits", [])
        )


class Project:
    def __init__(self, title: str, chapters: Optional[List[Chapter]] = None, characters: Optional[List[Character]] = None):
        self.title = title
        self.chapters = chapters or []
        self.characters = characters or []

    def to_dict(self):
        return {
            "title": self.title,
            "chapters": [chapter.to_dict() for chapter in self.chapters],
            "characters": [character.to_dict() for character in self.characters]
        }

    @staticmethod
    def from_dict(data):
        chapters = [Chapter.from_dict(c) for c in data.get("chapters", [])]
        characters = [Character.from_dict(c)
                      for c in data.get("characters", [])]
        return Project(title=data["title"], chapters=chapters, characters=characters)

    def save(self, path: Path):
        path.write_text(json.dumps(self.to_dict(), indent=2), encoding='utf-8')

    @staticmethod
    def load(path: Path):
        data = json.loads(path.read_text(encoding='utf-8'))
        return Project.from_dict(data)
