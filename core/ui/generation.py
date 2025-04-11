import streamlit as st
import logging
from core.llm_handler import LLMHandler
from utils.config import load_config, save_config

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

    if "history" not in st.session_state:
        st.session_state.history = []

    config = load_config()
    default_model = config.get("model", "llama3")
    default_temp = config.get("temperature", 0.7)

    st.sidebar.header("⚙️ Настройки")
    model_choice = st.sidebar.selectbox("Модель", ["llama3", "mistral"], index=[
                                        "llama3", "mistral"].index(default_model))
    temperature = st.sidebar.slider(
        "Креативность", 0.1, 1.0, float(default_temp))

    if st.sidebar.button("🔖 Сохранить настройки"):
        save_config({"model": model_choice, "temperature": temperature})
        st.sidebar.success("Настройки сохранены!")

    user_text = st.text_area("Введите ваш текст:",
                             height=300, placeholder="Начните писать здесь...")

    if st.button("✍️ Сгенерировать продолжение"):
        if user_text.strip():
            with st.spinner("ИИ думает..."):
                handler = LLMHandler(
                    model_name=f"ollama:{model_choice}",
                    temperature=temperature,
                    use_memory=True
                )

                generated_text = handler.generate_from_template(user_text)

                st.success("✅ Продолжение готово:")
                st.text_area("Ответ", value=generated_text, height=300)

                st.session_state.history.append({
                    "input": user_text,
                    "output": generated_text
                })

                log_interaction(user_text, generated_text)

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
            st.warning("Введите текст для генерации.")
