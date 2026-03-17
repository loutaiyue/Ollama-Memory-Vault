import requests
import json
from memory_manager import MemoryManager

def chat_with_ollama():
    # 1. 初始化记忆管理器
    memory = MemoryManager()
    
    # 2. 获取之前的对话历史作为上下文
    history = memory.get_messages()
    
    print(f"--- 系统：已加载 {len(history)} 条记忆。输入 'exit' 退出 ---")
    
    while True:
        user_input = input("\n你: ")
        if user_input.lower() in ['exit', 'quit', '退出']:
            break

        # 将用户输入存入记忆
        memory.add_message("user", user_input)

        # 3. 准备发送给 Ollama 的数据
        url = "http://localhost:11434/api/chat"
        payload = {
            "model": "llama3",  # 确保你本地有这个模型，没有的话换成你有的
            "messages": memory.get_messages(),
            "stream": False
        }

        print("AI 正在思考...", end="\r")

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            # 获取 AI 的回复内容
            ai_content = response.json()['message']['content']
            print(f"AI: {ai_content}")

            # 4. 将 AI 的回复存入记忆
            memory.add_message("assistant", ai_content)

        except Exception as e:
            print(f"\n❌ 出错了: {e}")

if __name__ == "__main__":
    chat_with_ollama()