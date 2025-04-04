import pytest
import json
from unittest.mock import patch, MagicMock
from core.llm_handler import LLMHandler


@patch("core.llm_handler.ChatOllama")
def test_generate_basic(mock_chat_ollama):
    mock_response = MagicMock()
    mock_response.content = "Ответ от LLM"

    mock_instance = MagicMock()
    mock_instance.invoke.return_value = mock_response
    mock_chat_ollama.return_value = mock_instance

    handler = LLMHandler(model_name="ollama:llama3")
    result = handler.generate("Привет!")

    assert result == "Ответ от LLM"


@patch("core.llm_handler.ChatOllama")
def test_generate_with_system_prompt(mock_chat_ollama):
    mock_response = MagicMock()
    mock_response.content = "Ответ с системным промптом"

    mock_instance = MagicMock()
    mock_instance.invoke.return_value = mock_response
    mock_chat_ollama.return_value = mock_instance

    handler = LLMHandler()
    result = handler.generate("Что ты умеешь?", system_prompt="Ты — литературный помощник.")

    assert result == "Ответ с системным промптом"


@patch("core.llm_handler.ChatOllama")
def test_generate_from_template(mock_chat_ollama, tmp_path):
    # Подготовка временного шаблона
    template = {
        "system": "Ты пишешь сказки.",
        "examples": [
            {"user": "Кто главный герой?", "assistant": "Принцесса Луна"}
        ]
    }
    template_path = tmp_path / "prompt.json"
    template_path.write_text(json.dumps(template, ensure_ascii=False))

    # Мокаем модель
    mock_response = MagicMock()
    mock_response.content = "Сказочное продолжение..."

    mock_instance = MagicMock()
    mock_instance.invoke.return_value = mock_response
    mock_chat_ollama.return_value = mock_instance

    handler = LLMHandler(template_path=str(template_path))
    result = handler.generate_from_template("Что произошло дальше?")

    assert result == "Сказочное продолжение..."
    mock_instance.invoke.assert_called_once()


@patch("core.llm_handler.ChatOllama")
def test_generate_from_template_file_not_found(mock_chat_ollama):
    mock_response = MagicMock()
    mock_response.content = "Ответ без шаблона"
    
    mock_instance = MagicMock()
    mock_instance.invoke.return_value = mock_response
    mock_chat_ollama.return_value = mock_instance

    handler = LLMHandler(template_path="non_existent_file.json")
    result = handler.generate_from_template("Просто продолжи текст.")
    
    assert result == "Ответ без шаблона"

@patch("core.llm_handler.ChatOllama")
def test_generate_from_template_invalid_json(mock_chat_ollama, tmp_path):
    broken_template_path = tmp_path / "invalid_prompt.json"
    broken_template_path.write_text("{ this is not: valid json")

    mock_response = MagicMock()
    mock_response.content = "Ответ даже при ошибке в шаблоне"
    
    mock_instance = MagicMock()
    mock_instance.invoke.return_value = mock_response
    mock_chat_ollama.return_value = mock_instance

    handler = LLMHandler(template_path=str(broken_template_path))
    result = handler.generate_from_template("Что происходит?")
    
    assert result == "Ответ даже при ошибке в шаблоне"
