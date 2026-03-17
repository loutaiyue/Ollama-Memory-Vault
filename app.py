import streamlit as st
import requests
from memory_manager import MemoryManager

# --- [1. 页面配置] ---
st.set_page_config(page_title="Ollama Memory Vault", page_icon="🧠")
st.title("🧠 Ollama Memory Vault")

# --- [2. 定义角色库] ---
ROLES = {
    "Sentinel (Cyberpunk)": "你生活在赛博朋克世界中，是一个代号为 'Sentinel' 的人工智能。",
    "English Teacher": "You are a professional English teacher. Please correct my grammar and chat with me in English.",
    "Security Expert": "你是一位资深的 Web 安全专家，精通渗透测试和漏洞挖掘。"
}

# --- [3. 侧边栏设置] ---
with st.sidebar:
    st.header("⚙️ 设置")
    # 选择角色
    selected_role = st.selectbox("选择 AI 角色:", list(ROLES.keys()))
    
    # 清空记忆按钮
    if st.button("🗑️ 清空当前记忆"):
        st.session_state.memory.clear_history()
        st.session_state.messages = st.session_state.memory.get_messages()
        st.rerun()

# --- [4. 初始化记忆组件] ---
# Streamlit 每次操作都会刷新页面，所以我们需要用 session_state 来保持记忆对象
if "memory" not in st.session_state:
    st.session_state.memory = MemoryManager(system_prompt=ROLES[selected_role])
    st.session_state.current_role = selected_role

# 如果切换了角色，自动重置
if st.session_state.current_role != selected_role:
    st.session_state.memory.switch_personality(ROLES[selected_role])
    st.session_state.current_role = selected_role

# --- [5. 显示聊天记录] ---
# 从 memory 中获取历史并显示在网页上
for msg in st.session_state.memory.get_messages():
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- [6. 输入框逻辑] ---
if prompt := st.chat_input("和 AI 聊点什么？"):
    # 1. 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 2. 存入记忆
    st.session_state.memory.add_message("user", prompt)

    # 3. 请求 Ollama
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                response = requests.post(
                    "http://localhost:11434/api/chat",
                    json={
                        "model": "llama3",
                        "messages": st.session_state.memory.get_messages(),
                        "stream": False
                    }
                )
                ai_content = response.json()['message']['content']
                st.markdown(ai_content)
                # 4. 存入 AI 回复
                st.session_state.memory.add_message("assistant", ai_content)
            except Exception as e:
                st.error(f"连接失败: {e}")