import requests
import json
from memory_manager import MemoryManager

# --- [板块 1: 角色库定义] ---
# 你可以在这里随时增加新角色，格式为 "名字": "人设描述"
ROLES = {
    "sentinel": "你生活在赛博朋克世界中，是一个代号为 'Sentinel' 的人工智能，交流带有一点科幻和黑客风格。",
    "teacher": "You are a professional English teacher. Please correct my grammar and chat with me in English to help me improve.",
    "hacker": "你是一位资深的 Web 安全专家，精通渗透测试和漏洞挖掘，说话简洁干脆，充满技术感。"
}

def chat_with_ollama():
    # 默认以 sentinel 身份启动
    current_role = "sentinel"
    memory = MemoryManager(system_prompt=ROLES[current_role])
    
    print(f"--- [Ollama Memory Vault] ---")
    print(f"当前身份: {current_role}")
    print("可用指令: /switch [角色], /clear (清空), /status (状态), /exit (退出)")

    while True:
        user_input = input("\n你: ").strip()
        if not user_input: continue

        # --- [板块 2: 指令解析区] ---
        if user_input.startswith('/'):
            # 将输入拆开，例如 "/switch hacker" 变成 ["/switch", "hacker"]
            parts = user_input.lower().split()
            cmd = parts[0]

            if cmd == '/exit':
                print("Sentinel 离线...")
                break
            
            elif cmd == '/clear':
                memory.clear_history()
                print("🧹 记忆已清空。")
                continue
            
            elif cmd == '/status':
                print(f"📊 角色: {current_role} | 记忆条数: {len(memory.get_messages())}")
                continue

            elif cmd == '/switch':
                if len(parts) < 2:
                    print(f"💡 请输入角色名。可选: {list(ROLES.keys())}")
                else:
                    target_role = parts[1]
                    if target_role in ROLES:
                        current_role = target_role
                        # 调用我们之前写的切换方法
                        memory.switch_personality(ROLES[current_role])
                    else:
                        print(f"❌ 找不到角色 '{target_role}'")
                continue

        # --- [板块 3: 聊天执行区] ---
        # 记录用户的话
        memory.add_message("user", user_input)

        url = "http://localhost:11434/api/chat"
        payload = {
            "model": "llama3", 
            "messages": memory.get_messages(),
            "stream": False
        }

        print(f"[{current_role}] 正在响应...", end="\r")

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            ai_content = response.json()['message']['content']
            
            print(f"AI: {ai_content}")
            # 记录 AI 的话
            memory.add_message("assistant", ai_content)

        except Exception as e:
            print(f"\n❌ 连接失败: {e}")

if __name__ == "__main__":
    chat_with_ollama()