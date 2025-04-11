import streamlit as st
from core.llm_handler import LLMHandler


def lore_editor_ui():
    st.title("🌍 Редактор Лора")

    handler = LLMHandler(use_memory=True)
    memory = handler.memory_manager  # доступ к MemoryManager

    # Получаем текущий лор
    lore_list = memory.get_memory_summary()["lore"]
    joined_text = "\n".join(lore_list)

    st.markdown("Отредактируйте правила мира (каждая строка — отдельный пункт):")
    edited = st.text_area("Правила мира", value=joined_text, height=300)

    if st.button("💾 Сохранить изменения"):
        new_lore = [line.strip()
                    for line in edited.splitlines() if line.strip()]
        memory.update_lore(new_lore)
        st.success("Лор обновлён и сохранён!")
