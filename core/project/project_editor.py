import streamlit as st
from pathlib import Path
from core.project.project_model import Project, Chapter, Scene

PROJECTS_DIR = Path("projects")
PROJECTS_DIR.mkdir(exist_ok=True)


def project_editor_ui():
    # Выбор проекта
    project_files = list(PROJECTS_DIR.glob("*.json"))
    project_names = [f.stem for f in project_files]
    selected_project_name = st.sidebar.selectbox(
        "Выберите проект", project_names)

    if selected_project_name:
        project_path = PROJECTS_DIR / f"{selected_project_name}.json"
        project = Project.load(project_path)

        st.title(f"Проект: {project.title}")

        chapter_titles = [ch.title for ch in project.chapters]
        selected_chapter = st.selectbox("Глава", chapter_titles)

        if selected_chapter:
            chapter = next(
                ch for ch in project.chapters if ch.title == selected_chapter)
            scene_titles = [sc.title for sc in chapter.scenes]
            selected_scene = st.selectbox("Сцена", scene_titles)

            if selected_scene:
                scene = next(
                    sc for sc in chapter.scenes if sc.title == selected_scene)
                scene_title = st.text_input(
                    "Название сцены", value=scene.title)
                scene_content = st.text_area(
                    "Текст сцены", value=scene.content, height=300)

                if st.button("Сохранить сцену"):
                    scene.title = scene_title
                    scene.content = scene_content
                    project.save(project_path)
                    st.success("Сцена сохранена")
