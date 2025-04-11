import os
import json
import yaml

from langchain.memory import (
    ConversationSummaryBufferMemory,
    ConversationEntityMemory,
    VectorStoreRetrieverMemory,
    CombinedMemory
)
from langchain.vectorstores import FAISS
from langchain.embeddings import OllamaEmbeddings
from langchain.llms.base import BaseLLM
from langchain_core.memory import BaseMemory
from pydantic import Field


class FlattenedMemory(BaseMemory):
    memory: CombinedMemory = Field(exclude=True)

    def __init__(self, memory: CombinedMemory):
        super().__init__(memory=memory)

    def load_memory_variables(self, inputs: dict) -> dict:
        raw = self.memory.load_memory_variables(inputs)
        flat = {}
        for key, value in raw.items():
            if isinstance(value, dict):
                flat[key] = "\n".join(str(v) for v in value.values())
            elif isinstance(value, list):
                flat[key] = "\n".join(str(v) for v in value)
            else:
                flat[key] = str(value)
        return flat

    def save_context(self, inputs: dict, outputs: dict) -> None:
        return self.memory.save_context(inputs, outputs)

    def clear(self) -> None:
        return self.memory.clear()

    @property
    def memory_variables(self) -> list:
        return ["summary", "entities", "lore"]


class MemoryManager:
    """
    Менеджер памяти для WriterAI, объединяющий:
    - Сводку сюжета (summary)
    - Память о персонажах (entities)
    - Знания о мире (лоре) на основе векторного поиска

    Поддерживает загрузку и обновление лора из JSON/YAML файлов.
    """

    def __init__(self, llm: BaseLLM, embedding_model=None, lore_path: str = None):
        self.llm = llm
        self.embedding_model = embedding_model or OllamaEmbeddings(
            model="nomic-embed-text")
        self.lore_path = lore_path or "data/lore.yaml"

        # Инициализация компонентов памяти
        self.summary_memory = self._init_summary_memory()
        self.character_memory = self._init_entity_memory()
        self.lore_texts = self._load_lore_texts()
        self.lore_memory = self._init_lore_memory(self.lore_texts)

        # Объединённая память
        self.combined_memory = CombinedMemory(
            memories=[
                self.summary_memory,
                self.character_memory,
                self.lore_memory
            ],
            exclude_input_keys=["history"]
        )

    def _init_summary_memory(self):
        return ConversationSummaryBufferMemory(
            llm=self.llm,
            memory_key="summary",
            input_key="input",
            return_messages=True
        )

    def _init_entity_memory(self):
        return ConversationEntityMemory(
            llm=self.llm,
            memory_key="entities",
            input_key="input",
            return_messages=True
        )

    def _init_lore_memory(self, texts):
        vectorstore = FAISS.from_texts(texts, embedding=self.embedding_model)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        return VectorStoreRetrieverMemory(
            retriever=retriever,
            memory_key="lore"
        )

    def _load_lore_texts(self):
        if not os.path.exists(self.lore_path):
            return []

        with open(self.lore_path, "r", encoding="utf-8") as f:
            if self.lore_path.endswith(".json"):
                data = json.load(f)
            elif self.lore_path.endswith((".yaml", ".yml")):
                data = yaml.safe_load(f)
            else:
                raise ValueError("Unsupported lore file format")

        if isinstance(data, list):
            return [item["text"] if isinstance(item, dict) and "text" in item else str(item) for item in data]
        else:
            return [str(data)]

    def update_lore(self, new_lore: list):
        self.lore_texts = new_lore
        self.lore_memory = self._init_lore_memory(self.lore_texts)

        if self.lore_path.endswith(".json"):
            with open(self.lore_path, "w", encoding="utf-8") as f:
                json.dump(new_lore, f, ensure_ascii=False, indent=2)
        elif self.lore_path.endswith((".yaml", ".yml")):
            with open(self.lore_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(new_lore, f, allow_unicode=True)

    def get_combined_memory(self):
        return FlattenedMemory(self.combined_memory)

    def get_memory_summary(self):
        dummy_input = {"input": ""}
        return {
            "summary": self.summary_memory.load_memory_variables(dummy_input),
            "characters": self.character_memory.load_memory_variables(dummy_input),
            "lore": self.lore_texts
        }
