import streamlit as st
import logging
from core.llm_handler import LLMHandler
from core.prompts.prompt_editor import prompt_editor_ui
from core.lore.lore_editor import lore_editor_ui
from core.project.project_editor import project_editor_ui
from utils.config import load_config, save_config
from logger.log_writer import list_log_files, load_logs_from_file
from logger.utils import setup_logging, log_interaction
from core.ui.generation import generation_ui
from core.ui.history import history_ui


st.set_page_config(page_title="NovelCraft MVP", layout="wide")

# перед основной логикой
setup_logging()


def main():
    # Навигация
    page = st.sidebar.selectbox("📚 Навигация", [
        "Генерация текста", "🧠 Prompt Editor", "📜 История", "🌍 Редактор Лора", "🔹 Проектный режим"
    ])

    if page == "Генерация текста":
        generation_ui()
    elif page == "🧠 Prompt Editor":
        prompt_editor_ui()
    elif page == "📜 История":
        history_ui()
    elif page == "🌍 Редактор Лора":
        lore_editor_ui()
    elif page == "🔹 Проектный режим":
        # Вызов редактора проекта
        project_editor_ui()


if __name__ == "__main__":
    main()
