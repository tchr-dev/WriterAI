import os
from pathlib import Path
from typing import List
from core.project.project_model import Project

# Папка по умолчанию для хранения проектов
PROJECTS_DIR = Path("projects")
PROJECTS_DIR.mkdir(exist_ok=True)


def create_project(title: str) -> Project:
    """Создание нового проекта"""
    project = Project(title=title)
    save_project(project)
    return project


def get_project_path(name: str) -> Path:
    """Получить путь к файлу проекта"""
    return PROJECTS_DIR / f"{name}.json"


def list_projects() -> List[str]:
    """Список доступных проектов (по имени файла без .json)"""
    return [f.stem for f in PROJECTS_DIR.glob("*.json")]


def load_project(name: str) -> Project:
    """Загрузка проекта по имени"""
    path = get_project_path(name)
    if not path.exists():
        raise FileNotFoundError(f"Проект '{name}' не найден")
    return Project.load(path)


def save_project(project: Project):
    """Сохранение проекта"""
    path = get_project_path(project.title)
    project.save(path)


def delete_project(name: str):
    """Удаление проекта по имени"""
    path = get_project_path(name)
    if path.exists():
        path.unlink()
