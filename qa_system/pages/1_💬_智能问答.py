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

# ═══════════════════════════════════════════
# 强制修复 Ollama 中文路径（无条件设置，杀旧进程）
# ═══════════════════════════════════════════
OLLAMA_MODELS_PATH = 'C:/ollama_models'
os.environ['OLLAMA_MODELS'] = OLLAMA_MODELS_PATH  # 无条件覆盖，不检查是否已设

import streamlit as st
import pandas as pd
import subprocess
import time

# ═══════════════════════════════════════════
# 全局 CSS（FA CDN + 背景 + 侧边栏）
# ═══════════════════════════════════════════
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&display=swap" rel="stylesheet">

<style>
    .stApp {
        background: linear-gradient(175deg, #f8faf6 0%, #f2f6ef 40%, #f6f8f3 100%);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f0f4ec 0%, #e8ede4 100%);
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label {
        color: #2d3429 !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #2c4a34 !important;
    }
    hr { border-color: #d8ddd2 !important; }
</style>
""", unsafe_allow_html=True)

st.title("智能问答")
st.caption("基于 Qwen2.5-7B 本地推理 | 4,596 条实测数据 | 支持多轮对话")

# ── 初始化 QABot（session_state，避免 cache_resource 缓存错误状态） ──
if "bot" not in st.session_state:
    st.session_state.bot = None
    st.session_state.ollama_error = None
if "ollama_started" not in st.session_state:
    st.session_state.ollama_started = False

_TRIED_START = False  # 每个会话只尝试启动一次


def _kill_existing_llama_server():
    """杀掉系统托盘启动的旧 llama-server（它没有 OLLAMA_MODELS 环境变量）"""
    try:
        subprocess.run(['taskkill', '/f', '/im', 'llama-server.exe'],
                       capture_output=True, timeout=5)
        subprocess.run(['taskkill', '/f', '/im', 'ollama.exe'],
                       capture_output=True, timeout=5)
        time.sleep(1.5)  # 等进程完全退出
    except Exception:
        pass  # 没找到进程不是错误


def _ensure_ollama_running():
    """确保 Ollama 服务在运行，必要时杀掉旧进程并重新启动"""
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

    # 2. 杀掉系统托盘可能已启动的旧进程（它们没有 OLLAMA_MODELS）
    _kill_existing_llama_server()

    # 3. 启动 ollama serve（带 OLLAMA_MODELS 环境变量）
    ollama_exe = os.path.expandvars('%LOCALAPPDATA%\\Programs\\Ollama\\ollama.exe')
    if not os.path.exists(ollama_exe):
        return False, f"找不到 ollama.exe: {ollama_exe}，请安装 Ollama。"

    # 确保环境变量在子进程中生效
    env = os.environ.copy()
    env['OLLAMA_MODELS'] = OLLAMA_MODELS_PATH

    try:
        subprocess.Popen([ollama_exe, 'serve'],
                         env=env,
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
    except Exception as e:
        return False, f"启动 Ollama 失败: {e}"

    # 4. 等待就绪（最多 20 秒，因为杀进程后重启可能慢一些）
    for i in range(20):
        time.sleep(1)
        try:
            import ollama
            ollama.list()
            return True, ""
        except Exception:
            continue

    return False, "Ollama 启动超时（20秒），请检查 Ollama 安装是否正确。"


if st.session_state.bot is None and st.session_state.ollama_error is None:
    with st.spinner("正在连接 Ollama 服务..."):
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
    # 重试按钮（不使用HTML，st.button 不支持）
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
    # 标题用 st.markdown（支持 HTML/FA 图标）
    st.markdown("""<p style="font-family:'Noto Serif SC','STSong',serif; font-weight:600; font-size:1.1rem; color:#2c4a34;">
        <i class="fa-solid fa-bullseye" style="color:#c4944a;"></i> 预设问题</p>""", unsafe_allow_html=True)

    # 按钮标签只能用纯文本/emoji，不能用 HTML
    golden = [
        ("🔍 精准统计", "南京冬季香樟的TSP滞尘量是多少？"),
        ("🔎 模糊匹配", "法桐在杭州全年的滞尘表现如何？"),
        ("🏆 跨物种排名", "南京道路绿地种植什么乔木滞尘效果比较好？"),
        ("🔬 形态因子", "有毛的植物滞尘效果是不是比无毛的好？"),
        ("🏙️ 城市对比", "北京和杭州的灌木哪个城市滞尘更强？"),
    ]
    for label, q in golden:
        if st.button(f"{label}：{q[:28]}…", use_container_width=True):
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
        st.caption(f"{len(st.session_state.messages)//2} 轮对话")

    st.divider()
    st.caption("💡 提示：问题越具体，回答越精准。例如带上城市名+物种名+季节。")

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
