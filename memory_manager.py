import json
import os

class MemoryManager:
    def __init__(self, filename="history.json",system_prompt="你生活在赛博朋克世界中，是一个代号为 'Sentinel' 的人工智能，交流时带有黑客电影的氛围感。"):
        self.filename = filename
        self.system_prompt=system_prompt
        self.history = self._load_history()

    def _load_history(self):
        history = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                history = json.load(f)
        new_system_msg = {"role": "system", "content": self.system_prompt}
        
        if not history:
            history.append(new_system_msg)
        else:
            if history[0].get("role") == "system":
                history[0] = new_system_msg
            else:
                history.insert(0, new_system_msg)
                
        return history
    
    def clear_history(self):
        # 恢复到只有系统提示词的初始状态
        self.history = [{"role": "system", "content": self.system_prompt}]
        self._save()
        print("🧹 记忆已清空,AI 已重置。")

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