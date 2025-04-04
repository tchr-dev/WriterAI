import os
import tempfile
from utils.exporter import export_to_md

def test_export_to_md_creates_file_with_correct_content():
    sample_text = "# Заголовок\nЭто тестовый текст."

    # Создаем временный файл (безопасно удалится после теста)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as tmp_file:
        tmp_path = tmp_file.name

    try:
        export_to_md(sample_text, tmp_path)

        # Проверяем, что файл существует и содержит нужный текст
        with open(tmp_path, "r", encoding="utf-8") as f:
            content = f.read()

        assert content == sample_text
    finally:
        os.remove(tmp_path)  # Чистим файл после теста
