import streamlit as st
from core.llm_handler import LLMHandler
from logger.log_writer import list_log_files, load_logs_from_file

LOGS_PATH = "logs"


def history_ui():
    st.title("📜 История запросов")

    log_files = list_log_files()
    if log_files:
        selected_log = st.selectbox(
            "Выберите файл лога", log_files, index=len(log_files)-1)
        logs = load_logs_from_file(selected_log)

        for entry in reversed(logs):
            with st.expander(f"{entry.get('timestamp', 'нет времени')} | {entry.get('model_name', 'модель?')}"):
                st.markdown(
                    f"**Prompt:**\n```text\n{entry.get('prompt', '')}```")
                st.markdown(
                    f"**Response:**\n```text\n{entry.get('response', '')}```")
    else:
        st.info("Файлы логов не найдены.")
