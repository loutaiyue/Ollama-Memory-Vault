import json
import os

class MemoryManager:
    def __init__(self, filename="history.json"):
        self.filename = filename
        self.history = self._load_history()

    def _load_history(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})
        # 限制长度，防止上下文爆炸
        if len(self.history) > 20:
            self.history = self.history[-20:]
        self._save()

    def _save(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def get_messages(self):
        return self.history