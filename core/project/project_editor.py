import streamlit as st
from core.project.project_model import Chapter, Scene
from core.project.project_manager import (
    list_projects,
    create_project,
    load_project,
    save_project,
    delete_project,
)


def project_editor_ui():
    st.sidebar.header("Проекты")

    # Список доступных проектов
    projects = list_projects()
    selected_project_name = st.sidebar.selectbox("Выберите проект", projects)

    # Создание нового проекта
    with st.sidebar.expander("➕ Новый проект"):
        new_project_name = st.text_input("Название проекта")
        if st.button("Создать проект") and new_project_name:
            create_project(new_project_name)
            st.rerun()

    # Удаление проекта с подтверждением
    if selected_project_name:
        with st.sidebar.expander("🗑️ Удалить проект"):
            st.warning(f"Проект: {selected_project_name}")
            confirm_delete = st.checkbox("Подтвердить удаление")
            if st.button("Удалить проект") and confirm_delete:
                delete_project(selected_project_name)
                st.rerun()

    if selected_project_name:
        project = load_project(selected_project_name)
        st.sidebar.markdown("---")

        st.title(f"Проект: {project.title}")
        st.markdown("## 📚 Структура и редактирование")

        for ch in project.chapters:
            st.markdown(f"### 📖 {ch.title}")
            new_ch_title = st.text_input(
                f"Название главы", value=ch.title, key=f"ch_title_{ch.title}")
            if new_ch_title != ch.title:
                ch.title = new_ch_title
                save_project(project)

            if st.button(f"❌ Удалить главу '{ch.title}'", key=f"del_ch_{ch.title}"):
                project.chapters = [c for c in project.chapters if c != ch]
                save_project(project)
                st.rerun()

            new_scene_title = st.text_input(
                "Название новой сцены", key=f"new_scene_{ch.title}")
            if st.button("Добавить сцену", key=f"add_scene_{ch.title}") and new_scene_title:
                ch.scenes.append(Scene(title=new_scene_title, content=""))
                save_project(project)
                st.rerun()

            for sc in ch.scenes:
                st.markdown(f"#### ✏️ Сцена: {sc.title}")
                sc_title = st.text_input(
                    "Название сцены", value=sc.title, key=f"sc_title_{ch.title}_{sc.title}")
                sc_content = st.text_area(
                    "Текст сцены", value=sc.content, height=300, key=f"sc_text_{ch.title}_{sc.title}")

                if st.button("Сохранить сцену", key=f"save_scene_{ch.title}_{sc.title}"):
                    sc.title = sc_title
                    sc.content = sc_content
                    save_project(project)
                    st.success("Сцена сохранена")

                if st.button("❌ Удалить сцену", key=f"del_scene_{ch.title}_{sc.title}"):
                    ch.scenes = [s for s in ch.scenes if s != sc]
                    save_project(project)
                    st.rerun()

        # Добавление новой главы
        st.markdown("---")
        st.subheader("➕ Добавить главу")
        new_chapter_title = st.text_input(
            "Название новой главы", key="new_chapter")
        if st.button("Добавить главу") and new_chapter_title:
            project.chapters.append(Chapter(title=new_chapter_title))
            save_project(project)
            st.rerun()
