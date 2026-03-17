# Ollama-Memory-Vault 🧠

A lightweight Python tool to provide **persistent memory** and **custom personalities** for local LLMs (Ollama).  
一个为本地大模型（Ollama）提供**持久化记忆**和**自定义性格**的轻量级 Python 工具。

---

## 🌟 Key Features / 核心功能
- **Persistent Context**: Automatically saves and loads chat history via `history.json`.  
  (持久化上下文：通过 `history.json` 自动保存和加载对话历史。)
- **System Prompting**: Easily define AI personalities (e.g., Cyberpunk, Security Expert).  
  (系统提示词：轻松定义 AI 性格，如赛博朋克、安全专家。)
- **Memory Management**: Keeps context length under control to prevent performance drops.  
  (记忆管理：自动控制上下文长度，防止模型响应变慢。)

## 🚀 Getting Started / 快速上手

### 1. Prerequisites / 环境准备
- [Ollama](https://ollama.com/) installed and running.
- Python 3.10+ installed.

### 2. Installation / 安装
Clone this repository and install dependencies:  
克隆仓库并安装依赖：
```bash
git clone [https://github.com/zengniu222/Ollama-Memory-Vault.git]
cd Ollama-Memory-Vault
pip install -r requirements.txt

### 🛠️ Developer Commands / 开发者指令
During the chat, you can use the following commands:
在对话过程中，你可以使用以下指令：
- `/clear`: Reset memory and start over. (重置记忆，重新开始)
- `/status`: View current memory status. (查看当前记忆状态)
- `/exit`: Safe exit. (安全退出)
### 🎭 Role Switching /切换角色
Type /switch [role_name] to change AI personality:
/switch sentinel (Default)
/switch teacher (English learning)
/switch hacker (Security expert)
