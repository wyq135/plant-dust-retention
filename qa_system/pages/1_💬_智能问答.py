"""
💬 智能问答 — 自然语言查询滞尘数据
基于 Qwen2.5-7B 本地推理，支持多轮对话与指代消解
"""
import sys, os
from pathlib import Path

# Streamlit pages/ 子目录运行时 Python path 可能不包含项目根
_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

# 修复 Ollama 中文用户名路径问题（llama.cpp 不支持非ASCII路径）
if not os.environ.get('OLLAMA_MODELS'):
    ollama_models_path = 'C:/ollama_models'
    if os.path.exists(ollama_models_path):
        os.environ['OLLAMA_MODELS'] = ollama_models_path

import streamlit as st
import pandas as pd
import subprocess
import time

st.title("💬 智能问答")
st.caption("基于 Qwen2.5-7B 本地推理 | 4,596 条实测数据 | 支持多轮对话")

# ── 初始化 QABot（session_state，避免 cache_resource 缓存错误状态） ──
if "bot" not in st.session_state:
    st.session_state.bot = None
    st.session_state.ollama_error = None
if "ollama_started" not in st.session_state:
    st.session_state.ollama_started = False

_TRIED_START = False  # 每个会话只尝试启动一次

def _ensure_ollama_running():
    """确保 Ollama 服务在运行，必要时自动启动"""
    global _TRIED_START

    # 1. 先尝试连接
    try:
        import ollama
        ollama.list()
        return True, ""
    except ImportError:
        return False, "ollama 包未安装，请运行: pip install ollama"
    except Exception:
        pass  # 服务未运行，尝试启动

    if _TRIED_START:
        return False, "Ollama 服务未启动，自动启动也失败了。请手动启动 Ollama 后刷新页面。"
    _TRIED_START = True

    # 2. 自动启动 ollama serve
    ollama_exe = os.path.expandvars('%LOCALAPPDATA%\\Programs\\Ollama\\ollama.exe')
    if not os.path.exists(ollama_exe):
        return False, f"找不到 ollama.exe: {ollama_exe}，请安装 Ollama。"

    try:
        subprocess.Popen([ollama_exe, 'serve'],
                         env=os.environ.copy(),
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
    except Exception as e:
        return False, f"启动 Ollama 失败: {e}"

    # 3. 等待就绪（最多 15 秒）
    for i in range(15):
        time.sleep(1)
        try:
            import ollama
            ollama.list()
            return True, ""
        except Exception:
            continue

    return False, "Ollama 启动超时（15秒），请检查 Ollama 安装是否正确。"


if st.session_state.bot is None and st.session_state.ollama_error is None:
    with st.spinner("🔄 正在连接 Ollama 服务..."):
        ok, err = _ensure_ollama_running()

    if not ok:
        st.session_state.ollama_error = err
    else:
        # 检查是否有 Qwen 模型
        try:
            import ollama
            models = ollama.list()
            has_model = any('qwen' in m.model.lower() for m in models.models)
            if not has_model:
                st.session_state.ollama_error = "Ollama 已启动但未找到 Qwen 模型。请运行: ollama pull qwen2.5:7b"
            else:
                try:
                    from qa_system.qa_bot import QABot
                    st.session_state.bot = QABot()
                    st.session_state.ollama_started = True
                except Exception as e:
                    st.session_state.ollama_error = f"QABot 初始化失败: {e}"
        except Exception as e:
            st.session_state.ollama_error = f"Ollama 连接异常: {e}"

# 显示错误（如果有）
if st.session_state.ollama_error:
    st.error(f"⚠️ {st.session_state.ollama_error}")
    st.info("""
    **离线模式**：智能问答需要 Ollama 服务支持。当前可使用以下功能：
    - 📊 **数据总览**：查看全局统计和分布
    - 🍃 **形态因子分析**：交互式探索叶片特征与滞尘效果的关系
    """)
    # 提供重试按钮
    if st.button("🔄 重试连接", use_container_width=False):
        st.session_state.ollama_error = None
        st.rerun()
    st.stop()

bot = st.session_state.bot

if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# ── 处理待处理问题（来自侧边栏按钮） ──
if st.session_state.pending_question:
    q = st.session_state.pending_question
    st.session_state.pending_question = None
    with st.chat_message("assistant"):
        try:
            response_stream = bot.chat_stream(q)
            full_response = st.write_stream(response_stream)
        except Exception as e:
            full_response = f"⚠️ 查询出错: {e}"
            st.error(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.rerun()

# ── 侧边栏 ──
with st.sidebar:
    st.header("🎯 预设问题")
    golden = [
        ("精准统计", "南京冬季香樟的TSP滞尘量是多少？"),
        ("模糊匹配", "法桐在杭州全年的滞尘表现如何？"),
        ("跨物种排名", "南京道路绿地种植什么乔木滞尘效果比较好？"),
        ("形态因子", "有毛的植物滞尘效果是不是比无毛的好？"),
        ("城市对比", "北京和杭州的灌木哪个城市滞尘更强？"),
    ]
    for label, q in golden:
        if st.button(f"**{label}**：{q[:30]}…", use_container_width=True):
            # 避免重复添加
            if not st.session_state.messages or st.session_state.messages[-1].get("content") != q:
                st.session_state.messages.append({"role": "user", "content": q})
                st.session_state.pending_question = q
                st.rerun()

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🗑️ 清空对话", use_container_width=True):
            st.session_state.messages = []
            bot.reset()
            st.rerun()
    with c2:
        st.caption(f"📊 {len(st.session_state.messages)//2} 轮对话")

    st.divider()
    st.caption("💡 提示：问题越具体，回答越精准。\n例如带上城市名+物种名+季节。")

# ── 聊天历史 ──
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg.get("content", ""))

# ── 用户输入 ──
if prompt := st.chat_input("请输入您的问题，例如「南京香樟夏季TSP滞尘量是多少？」"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response_stream = bot.chat_stream(prompt)
            full_response = st.write_stream(response_stream)
        except Exception as e:
            full_response = f"⚠️ 查询出错: {e}"
            st.error(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
