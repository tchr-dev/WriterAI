import json
from pathlib import Path
from typing import Optional

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.language_models.chat_models import BaseChatModel
# Новые импорты:
from logger.log_writer import log_interaction
from core.memory.context_buffer import ContextBuffer


class LLMHandler:
    def __init__(
        self,
        model_name: str = "ollama:llama3",
        temperature: float = 0.7,
        template_path: str = "core/prompts/base.json"
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.template_path = Path(template_path)
        self.llm: BaseChatModel = self._get_llm()

        # Контекст
        self.context = ContextBuffer(max_messages=5)

    def _get_llm(self) -> BaseChatModel:
        if self.model_name.startswith("ollama:"):
            model_id = self.model_name.split(":", 1)[1]
            return ChatOllama(model=model_id, temperature=self.temperature)
        raise ValueError(f"Unsupported model: {self.model_name}")

    def _load_prompt_template(self) -> dict:
        if not self.template_path.exists():
            return {}
        try:
            return json.loads(self.template_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        # Собираем сообщения с учётом контекста
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))

        for m in self.context.buffer:
            if m["role"] == "user":
                messages.append(HumanMessage(content=m["content"]))
            elif m["role"] == "assistant":
                messages.append(AIMessage(content=m["content"]))

        messages.append(HumanMessage(content=prompt))

        # Генерация
        response = self.llm.invoke(messages)

        # Обновляем контекст
        self.context.add("user", prompt)
        self.context.add("assistant", response.content)

        # Логируем
        log_interaction(prompt="\n".join([m.content for m in messages]), response=response.content)

        return response.content

    def generate_from_template(self, user_prompt: str) -> str:
        template = self._load_prompt_template()
        messages = []

        if "system" in template:
            messages.append(SystemMessage(content=template["system"]))

        for ex in template.get("examples", []):
            messages.append(HumanMessage(content=ex.get("user", "")))
            messages.append(AIMessage(content=ex.get("assistant", "")))

        # Контекст из предыдущих сообщений
        for m in self.context.buffer:
            if m["role"] == "user":
                messages.append(HumanMessage(content=m["content"]))
            elif m["role"] == "assistant":
                messages.append(AIMessage(content=m["content"]))

        messages.append(HumanMessage(content=user_prompt))

        # Генерация
        response = self.llm.invoke(messages)

        # Обновляем контекст
        self.context.add("user", user_prompt)
        self.context.add("assistant", response.content)

        # Логируем
        log_interaction(prompt="\n".join([m.content for m in messages]), response=response.content)

        return response.content
