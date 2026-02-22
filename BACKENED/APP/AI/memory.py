# memory.py

from typing import List
from ..SCHEMAS.ai_schema import AIMemoryEntry


class AIMemoryStore:

    def __init__(self):
        self.memory: List[AIMemoryEntry] = []

    def add_entry(self, entry: AIMemoryEntry):
        self.memory.append(entry)

    def get_session_memory(self, session_id: str):
        return [m for m in self.memory if m.session_id == session_id]