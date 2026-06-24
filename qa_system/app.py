"""
植物滞尘分析系统 v2 — 主页
启动: cd plant_dust_analysis && streamlit run qa_system/app.py --server.address 0.0.0.0 --server.port 8501
"""
import streamlit as st

st.set_page_config(page_title="植物滞尘分析系统", page_icon="🌿", layout="wide")

# ── 自定义 CSS ──
st.markdown("""
<style>
    .hero-title { font-size: 2.4rem; font-weight: 800; color: #2c3e50; margin-bottom: 0; }
    .hero-subtitle { font-size: 1.05rem; color: #6c757d; margin-top: 0; }
    .feature-card {
        background: white; border-radius: 12px; padding: 24px;
        border: 1px solid #e9ecef; transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
    .feature-card:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.1); }
    .feature-card .icon { font-size: 2rem; margin-bottom: 8px; }
    .feature-card h3 { font-size: 1.15rem; color: #2c3e50; margin: 8px 0 4px 0; }
    .feature-card p { font-size: 0.9rem; color: #6c757d; line-height: 1.5; }
    .version-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border-radius: 20px; padding: 4px 14px;
        font-size: 0.8rem; font-weight: 600; display: inline-block;
    }
    .stat-chip {
        background: #f0f4ff; border-radius: 8px; padding: 8px 14px;
        text-align: center; display: inline-block; margin: 2px;
    }
    .stat-chip .num { font-weight: 700; color: #667eea; font-size: 1.1rem; }
    .stat-chip .txt { font-size: 0.75rem; color: #6c757d; }
</style>
""", unsafe_allow_html=True)

# ── 标题区 ──
st.markdown('<p class="hero-title">🌿 植物叶片滞尘数据分析与可视化系统</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">长江流域亚热带城市群 · 全国三大气候区 · v5 全国尺度</p>', unsafe_allow_html=True)

st.markdown("")

# ── 数据快照条 ──
sc1, sc2, sc3, sc4, sc5, sc6, sc7 = st.columns(7)
with sc1:
    st.markdown('<div class="stat-chip"><div class="num">4,596</div><div class="txt">📋 总记录</div></div>', unsafe_allow_html=True)
with sc2:
    st.markdown('<div class="stat-chip"><div class="num">593</div><div class="txt">🌳 物种</div></div>', unsafe_allow_html=True)
with sc3:
    st.markdown('<div class="stat-chip"><div class="num">85</div><div class="txt">🏙️ 城市</div></div>', unsafe_allow_html=True)
with sc4:
    st.markdown('<div class="stat-chip"><div class="num">220</div><div class="txt">📄 论文</div></div>', unsafe_allow_html=True)
with sc5:
    st.markdown('<div class="stat-chip"><div class="num">3</div><div class="txt">🌍 气候区</div></div>', unsafe_allow_html=True)
with sc6:
    st.markdown('<div class="stat-chip"><div class="num">99%</div><div class="txt">🍃 叶片因子</div></div>', unsafe_allow_html=True)
with sc7:
    st.markdown('<div class="stat-chip"><div class="num">95%</div><div class="txt">📈 TSP覆盖</div></div>', unsafe_allow_html=True)

st.divider()

# ── 功能卡片 ──
st.markdown("### 👈 选择功能模块")

fc1, fc2, fc3 = st.columns(3)

with fc1:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">💬</div>
        <h3>智能问答</h3>
        <p>用自然语言查询滞尘数据。Qwen2.5-7B 本地推理驱动，支持多轮对话。<br>
        <i>"南京冬季香樟的TSP是多少？"<br>"有毛的植物滞尘效果更好吗？"</i></p>
        <p style="color: #667eea; font-size: 0.8rem;">📍 需 Ollama 运行 Qwen2.5-7B</p>
    </div>
    """, unsafe_allow_html=True)

with fc2:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">🍃</div>
        <h3>形态因子分析 ★核心</h3>
        <p>交互式探索叶片表面特征、毛被、蜡质、叶形、气孔对滞尘效果的影响。<br>
        <i>箱线图 · 散点图 · 统计对比 · 气候区分组 · Top 15 物种</i></p>
        <p style="color: #43e97b; font-size: 0.8rem;">📍 论文核心论点可视化</p>
    </div>
    """, unsafe_allow_html=True)

with fc3:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">📊</div>
        <h3>数据总览</h3>
        <p>全局统计仪表盘。KPI卡片 · 气候区分布 · 城市Top25 · 生活型·功能区 · TSP分布直方图 · 论文列表<br>
        <i>一键了解数据集全貌</i></p>
        <p style="color: #4facfe; font-size: 0.8rem;">📍 实时统计，数据可追溯</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ── 技术栈 ──
col_tech, col_ver = st.columns([2, 1])
with col_tech:
    st.markdown("""
    #### 🔧 技术栈
    | 组件 | 技术 | 说明 |
    |------|------|------|
    | 前端 | Streamlit 1.58 | 多页面应用，零前端代码 |
    | 图表 | Plotly 6.8 | 交互式图表，支持悬停/缩放/筛选 |
    | 推理 | Qwen2.5-7B (Ollama) | 本地推理，数据不出本机 |
    | 数据 | Pandas + CSV | 4596条实测数据，即时过滤聚合 |
    | 形态因子 | FRPS 中国植物志 | 238属级叶片特征数据库 |
    """)

with col_ver:
    st.markdown("""
    #### 📦 数据版本
    """)
    st.markdown('<span class="version-badge">v5 第四批</span>', unsafe_allow_html=True)
    st.markdown("""
    - **发布日期**: 2026-06-24
    - **数据来源**: 220篇论文
    - **覆盖范围**: 85城/3气候区
    - **方法学**: A/B/C三级透明
    - **叶片因子**: 99.0% FRPS覆盖
    - **QA系统**: aliases 104物种+117城市
    """)

st.divider()
st.caption("💡 所有数据 100% 可验证 — 每个统计数字均可追溯至对应的原始论文记录。双击桌面「植物滞尘Q&A-网页版.bat」即可启动。")
