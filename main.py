import requests
import json
from memory_manager import MemoryManager

def chat_with_ollama():
    # 1. 初始化，设定你的 AI 身份
    system_text = "你生活在赛博朋克世界中，是一个代号为 'Sentinel' 的人工智能。"
    memory = MemoryManager(system_prompt=system_text)
    
    print("--- [Ollama Memory Vault 开发者模式] ---")
    print("可用指令: /clear (清空记忆), /status (查看状态), /exit (退出)")

    while True:
        user_input = input("\n你: ").strip()
        
        # --- [新增逻辑：开发者指令检查] ---
        if user_input.startswith('/'):
            cmd = user_input.lower()
            if cmd == '/exit':
                print("再见,Sentinel 离线...")
                break
            elif cmd == '/clear':
                memory.clear_history() # 调用我们新写的清空方法
                print("🧹 系统记忆已重置。")
                continue # 跳过下面的 AI 请求，回到输入框
            elif cmd == '/status':
                count = len(memory.get_messages())
                print(f"📊 当前记忆槽位: {count}/20")
                continue
            else:
                print("❓ 未知指令，请尝试 /clear 或 /exit")
                continue

        # --- [原有逻辑：正常聊天] ---
        if not user_input: continue

        # 记录用户说的话
        memory.add_message("user", user_input)

        url = "http://localhost:11434/api/chat"
        payload = {
            "model": "llama3", 
            "messages": memory.get_messages(),
            "stream": False
        }

        print("Sentinel 正在连接...", end="\r")

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            ai_content = response.json()['message']['content']
            
            print(f"AI: {ai_content}")
            # 记录 AI 说的话
            memory.add_message("assistant", ai_content)

        except Exception as e:
            print(f"\n❌ 连接中断: {e}")

if __name__ == "__main__":
    chat_with_ollama()