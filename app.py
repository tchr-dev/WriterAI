import streamlit as st
import logging
from core.llm_handler import LLMHandler
from core.prompts.prompt_editor import prompt_editor_ui
from core.lore.lore_editor import lore_editor_ui
from utils.config import load_config, save_config
from logger.log_writer import list_log_files, load_logs_from_file

st.set_page_config(page_title="NovelCraft MVP", layout="wide")

# Настройка логирования
logging.basicConfig(
    filename="logs/llm.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def log_interaction(prompt: str, response: str):
    logging.info("Prompt: %s", prompt)
    logging.info("Response: %s", response)


def generation_ui():
    st.title("🕋️ NovelCraft: Генерация текста")

    # Инициализация истории
    if "history" not in st.session_state:
        st.session_state.history = []

    # Загрузка конфигурации
    config = load_config()
    default_model = config.get("model", "llama3")
    default_temp = config.get("temperature", 0.7)

    # Боковая панель с настройками
    st.sidebar.header("⚙️ Настройки")
    model_choice = st.sidebar.selectbox("Модель", ["llama3", "mistral"], index=[
                                        "llama3", "mistral"].index(default_model))
    temperature = st.sidebar.slider(
        "Креативность", 0.1, 1.0, float(default_temp))

    if st.sidebar.button("🔖 Сохранить настройки"):
        save_config({"model": model_choice, "temperature": temperature})
        st.sidebar.success("Настройки сохранены!")

    # Ввод текста
    user_text = st.text_area("Введите ваш текст:", height=300,
                             placeholder="Начните писать здесь...")

    if st.button("✍️ Сгенерировать продолжение"):
        if user_text.strip():
            with st.spinner("ИИ думает..."):
                handler = LLMHandler(
                    model_name=f"ollama:{model_choice}",
                    temperature=temperature,
                    use_memory=True  # Включаем контекстную память
                )

                generated_text = handler.generate_from_template(user_text)

                st.success("✅ Продолжение готово:")
                st.text_area("Ответ", value=generated_text, height=300)

                st.session_state.history.append({
                    "input": user_text,
                    "output": generated_text
                })

                log_interaction(user_text, generated_text)

                # Отображаем память
                with st.expander("🧠 Контекст памяти"):
                    memory = handler.get_context_data()

                    st.subheader("📘 Сводка сюжета")
                    st.json(memory["summary"])

                    st.subheader("👤 Персонажи")
                    st.json(memory["characters"])

                    st.subheader("🌍 Лор / Магические правила")
                    for item in memory["lore"]:
                        st.markdown(f"- {item}")
        else:
            st.warning("Введите текст перед генерацией!")

    if st.checkbox("🕘 Показать историю"):
        for i, item in enumerate(reversed(st.session_state.history), 1):
            st.markdown(f"**#{i} Запрос:** {item['input']}")
            st.markdown(f"**Ответ:** {item['output']}")
            st.markdown("---")


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


def main():
    # Навигация
    page = st.sidebar.selectbox("📚 Навигация", [
        "Генерация текста", "🧠 Prompt Editor", "📜 История", "🌍 Редактор Лора"
    ])

    if page == "Генерация текста":
        generation_ui()
    elif page == "🧠 Prompt Editor":
        prompt_editor_ui()
    elif page == "📜 История":
        history_ui()
    elif page == "🌍 Редактор Лора":
        lore_editor_ui()


if __name__ == "__main__":
    main()
