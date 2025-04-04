import json
from pathlib import Path
from typing import Optional

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.language_models.chat_models import BaseChatModel


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
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=prompt))

        response = self.llm.invoke(messages)
        return response.content

    def generate_from_template(self, user_prompt: str) -> str:
        template = self._load_prompt_template()
        messages = []

        if "system" in template:
            messages.append(SystemMessage(content=template["system"]))

        for ex in template.get("examples", []):
            messages.append(HumanMessage(content=ex.get("user", "")))
            messages.append(AIMessage(content=ex.get("assistant", "")))

        messages.append(HumanMessage(content=user_prompt))

        response = self.llm.invoke(messages)
        return response.content
