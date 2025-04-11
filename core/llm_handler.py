import json
from pathlib import Path
from typing import Optional

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from core.prompts.prompt_editor import load_prompt

from logger.log_writer import log_interaction
from core.memory.context_buffer import ContextBuffer
from core.memory.memory_manager import MemoryManager


class LLMHandler:
    def __init__(
        self,
        model_name: str = "ollama:llama3",
        temperature: float = 0.7,
        template_path: str = "core/prompts/base.json",
        use_memory: bool = False
    ):
        """
        :param model_name: Модель, например "ollama:llama3"
        :param temperature: Креативность модели
        :param template_path: Путь к JSON-файлу с prompt-шаблоном
        :param use_memory: Включить ли LangChain-память через MemoryManager
        """
        self.model_name = model_name
        self.temperature = temperature
        self.template_path = Path(template_path)
        self.use_memory = use_memory

        self.llm: BaseChatModel = self._get_llm()
        self.context = ContextBuffer(max_messages=5)

        self.memory_manager: Optional[MemoryManager] = None
        self.conversation_chain: Optional[ConversationChain] = None

        if self.use_memory:
            self.memory_manager = MemoryManager(self.llm)
            memory = self.memory_manager.get_combined_memory()

            custom_prompt = PromptTemplate(
                input_variables=["input", "summary", "entities", "lore"],
                template="""
Ты помощник писателя. Вот текущий контекст:

📘 Сводка сюжета:
{summary}

👤 Персонажи:
{entities}

🌍 Правила мира:
{lore}

Теперь продолжи историю на основе следующего запроса:
{input}
""".strip()
            )

            self.conversation_chain = ConversationChain(
                llm=self.llm,
                memory=memory,
                prompt=custom_prompt
            )

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
        """
        Генерация ответа, используя либо LangChain memory, либо локальный буфер.
        """
        if self.use_memory and self.conversation_chain:
            response = self.conversation_chain.predict(input=prompt)
            log_interaction(prompt=prompt, response=response)
            return response

        # Без памяти — обычная генерация с буфером
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))

        for m in self.context.buffer:
            if m["role"] == "user":
                messages.append(HumanMessage(content=m["content"]))
            elif m["role"] == "assistant":
                messages.append(AIMessage(content=m["content"]))

        messages.append(HumanMessage(content=prompt))

        response = self.llm.invoke(messages)

        self.context.add("user", prompt)
        self.context.add("assistant", response.content)

        log_interaction(prompt="\n".join(
            [m.content for m in messages]), response=response.content)

        return response.content

    def generate_from_template(self, user_prompt: str) -> str:
        """
        Генерация ответа с использованием prompt-шаблона (если он задан).
        """
        if self.use_memory and self.conversation_chain:
            response = self.conversation_chain.predict(input=user_prompt)
            log_interaction(prompt=user_prompt, response=response)
            return response

        template = json.loads(load_prompt(str(self.template_path)))
        messages = []

        if "system" in template:
            messages.append(SystemMessage(content=template["system"]))

        for ex in template.get("examples", []):
            messages.append(HumanMessage(content=ex.get("user", "")))
            messages.append(AIMessage(content=ex.get("assistant", "")))

        for m in self.context.buffer:
            if m["role"] == "user":
                messages.append(HumanMessage(content=m["content"]))
            elif m["role"] == "assistant":
                messages.append(AIMessage(content=m["content"]))

        messages.append(HumanMessage(content=user_prompt))

        response = self.llm.invoke(messages)

        self.context.add("user", user_prompt)
        self.context.add("assistant", response.content)

        log_interaction(prompt="\n".join(
            [m.content for m in messages]), response=response.content)

        return response.content

    def get_context_data(self) -> dict:
        """
        Возвращает текущий контекст памяти, если память включена.
        :return: dict c ключами summary, characters, lore
        """
        if self.use_memory and self.memory_manager:
            return self.memory_manager.get_memory_summary()
        else:
            return {
                "summary": "Память отключена.",
                "characters": {},
                "lore": []
            }
