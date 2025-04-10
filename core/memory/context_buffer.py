class ContextBuffer:
    def __init__(self, max_messages=5):
        self.max_messages = max_messages
        self.buffer = []

    def add(self, role: str, content: str):
        self.buffer.append({"role": role, "content": content})
        if len(self.buffer) > self.max_messages:
            self.buffer.pop(0)

    def get_context(self) -> str:
        return "\n".join(f"{m['role'].capitalize()}: {m['content']}" for m in self.buffer)
