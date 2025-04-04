import streamlit as st
import json
from pathlib import Path

PROMPT_FILE = Path("core/prompts/base.json")

def prompt_editor_ui():
    st.header("🧠 Prompt Editor")

    # Загрузка текущего шаблона
    if PROMPT_FILE.exists():
        prompt_data = PROMPT_FILE.read_text()
    else:
        prompt_data = "{}"

    # UI-редактор
    editor = st.text_area("Prompt JSON", prompt_data, height=400)

    # Сохранение
    if st.button("💾 Сохранить"):
        try:
            parsed = json.loads(editor)  # Валидация
            PROMPT_FILE.write_text(json.dumps(parsed, indent=2, ensure_ascii=False))
            st.success("✅ Шаблон сохранён!")
        except json.JSONDecodeError as e:
            st.error(f"❌ Ошибка в JSON: {str(e)}")
