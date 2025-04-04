import streamlit as st
import logging
from core.llm_handler import LLMHandler
from core.prompts.prompt_editor import prompt_editor_ui
from utils.config import load_config, save_config

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
    model_choice = st.sidebar.selectbox("Модель", ["llama3", "mistral"], index=["llama3", "mistral"].index(default_model))
    temperature = st.sidebar.slider("Креативность", 0.1, 1.0, float(default_temp))

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
                    temperature=temperature
                )

                generated_text = handler.generate_from_template(user_text)

                st.success("✅ Продолжение готово:")
                st.text_area("Ответ", value=generated_text, height=300)

                st.session_state.history.append({
                    "input": user_text,
                    "output": generated_text
                })

                log_interaction(user_text, generated_text)
        else:
            st.warning("Введите текст перед генерацией!")

    if st.checkbox("🕘 Показать историю"):
        for i, item in enumerate(reversed(st.session_state.history), 1):
            st.markdown(f"**#{i} Запрос:** {item['input']}")
            st.markdown(f"**Ответ:** {item['output']}")
            st.markdown("---")

def main():
    # Навигация
    page = st.sidebar.selectbox("📚 Навигация", [
        "Генерация текста", "🧠 Prompt Editor"
    ])

    if page == "Генерация текста":
        generation_ui()
    elif page == "🧠 Prompt Editor":
        prompt_editor_ui()

if __name__ == "__main__":
    main()
