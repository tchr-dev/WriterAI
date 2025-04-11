import streamlit as st
from core.lore.character_editor import (
    get_character,
    add_or_update_character,
    delete_character,
    list_characters
)


def character_editor_ui():
    """
    UI для редактирования персонажей
    """
    # Заголовок
    st.title("📖 Редактор Персонажей")

    # Выбор персонажа
    characters = list_characters()
    selected = st.selectbox("Выберите персонажа", [
                            "<Новый персонаж>"] + characters)

    # Параметры персонажа
    if selected != "<Новый персонаж>":
        data = get_character(selected) or {}
    else:
        data = {}

    name = st.text_input("Имя", value=selected if selected !=
                         "<Новый персонаж>" else "")
    role = st.text_input("Роль", value=data.get("role", ""))
    description = st.text_area("Описание", value=data.get("description", ""))
    traits = st.text_area("Черты характера", value=data.get("traits", ""))
    motivation = st.text_area("Мотивация", value=data.get("motivation", ""))

    # Сохранение
    if st.button("Сохранить"):
        if name:
            add_or_update_character(name, {
                "role": role,
                "description": description,
                "traits": traits,
                "motivation": motivation
            })
            st.success(f"Персонаж '{name}' сохранен.")

    # Удаление
    if selected != "<Новый персонаж>" and st.button("Удалить"):
        delete_character(selected)
        st.warning(f"Персонаж '{selected}' удален.")
