"""
植物滞尘分析系统 v2 — 主页
启动: cd plant_dust_analysis && streamlit run qa_system/app.py --server.address 0.0.0.0 --server.port 8501
"""
import streamlit as st

st.set_page_config(page_title="植物滞尘分析系统", page_icon="🌿", layout="wide")

# ═══════════════════════════════════════════
# 全局 CSS：CDN + 背景 + 侧边栏 + 卡片 + 字体
# ═══════════════════════════════════════════
st.markdown("""
<!-- Font Awesome 6 矢量图标 -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

<!-- Google Fonts: Noto Serif SC（标题衬线体） -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&display=swap" rel="stylesheet">

<style>
    /* ═══ 全局背景：暖绿调渐变 ═══ */
    .stApp {
        background: linear-gradient(175deg, #f8faf6 0%, #f2f6ef 40%, #f6f8f3 100%);
    }

    /* ═══ 侧边栏：浅灰绿，原生控件零修改 ═══ */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f0f4ec 0%, #e8ede4 100%);
    }
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stCaption {
        color: #2d3429 !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #2c4a34 !important;
    }

    /* ═══ 标题衬线体 + 绿色下划线装饰 ═══ */
    .hero-title {
        font-family: 'Noto Serif SC', 'Source Han Serif SC', 'STSong', 'SimSun', serif;
        font-size: 2.2rem; font-weight: 700; color: #2c4a34;
        margin-bottom: 0; letter-spacing: 0.02em;
    }
    .hero-subtitle {
        font-family: 'Noto Serif SC', 'Source Han Serif SC', 'STSong', 'SimSun', serif;
        font-size: 0.95rem; color: #6b7a65; margin-top: 2px;
        font-weight: 400;
    }
    .section-heading {
        font-family: 'Noto Serif SC', 'Source Han Serif SC', 'STSong', 'SimSun', serif;
        font-size: 1.15rem; font-weight: 600; color: #2c4a34;
        border-bottom: 2px solid #c8dcc8; padding-bottom: 6px;
        margin-top: 18px; margin-bottom: 10px;
    }

    /* ═══ st.container(border=True) → 卡片左侧绿色 accent 条 ═══ */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-left: 4px solid #3a7d44 !important;
        border-top: 1px solid #e0e4dc !important;
        border-right: 1px solid #e0e4dc !important;
        border-bottom: 1px solid #e0e4dc !important;
        border-radius: 10px !important;
        background: #ffffff;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        transition: box-shadow 0.2s ease;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 4px 18px rgba(0,0,0,0.09);
    }

    /* ═══ 统计芯片（stat-chip） ═══ */
    .stat-chip {
        background: #ffffff; border: 1px solid #d8ddd2; border-radius: 10px;
        padding: 10px 14px; text-align: center; display: inline-block; margin: 3px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        min-width: 80px;
    }
    .stat-chip:hover { transform: translateY(-1px); box-shadow: 0 3px 10px rgba(0,0,0,0.08); }
    .stat-chip .num {
        font-family: 'Noto Serif SC', 'Source Han Serif SC', 'STSong', 'SimSun', serif;
        font-weight: 700; color: #3a7d44; font-size: 1.2rem;
    }
    .stat-chip .txt { font-size: 0.72rem; color: #6b7a65; }
    .stat-chip .fa-icon { font-size: 0.8rem; color: #3a7d44; margin-right: 2px; }

    /* ═══ 功能卡片（feature-card） ═══ */
    .feature-card {
        background: #ffffff; border-radius: 12px; padding: 24px;
        border: 1px solid #e0e4dc; border-left: 4px solid #3a7d44;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 24px rgba(0,0,0,0.10);
    }
    .feature-card .icon-circle {
        width: 48px; height: 48px; border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 10px;
        font-size: 1.3rem; color: #ffffff;
    }
    .feature-card h3 {
        font-family: 'Noto Serif SC', 'Source Han Serif SC', 'STSong', 'SimSun', serif;
        font-size: 1.1rem; color: #2c4a34; margin: 8px 0 4px 0; font-weight: 600;
    }
    .feature-card p { font-size: 0.88rem; color: #6b7a65; line-height: 1.55; }

    /* ═══ 版本徽章 ═══ */
    .version-badge {
        background: #3a7d44; color: #ffffff; border-radius: 20px;
        padding: 4px 16px; font-size: 0.78rem; font-weight: 600;
        display: inline-block;
    }

    /* ═══ hero 横幅渐变条 ═══ */
    .hero-bar {
        background: linear-gradient(90deg, #3a7d44 0%, #6aa76a 50%, #a8d0a8 100%);
        height: 3px; border-radius: 2px; margin: 2px 0 12px 0;
    }

    /* ═══ st.metric 美化 ═══ */
    [data-testid="stMetric"] { background: transparent; }
    [data-testid="stMetric"] label {
        font-size: 0.78rem !important; color: #6b7a65 !important;
        font-weight: 500 !important;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-family: 'Noto Serif SC', 'Source Han Serif SC', 'STSong', 'SimSun', serif;
        font-size: 1.5rem !important; font-weight: 700 !important; color: #2d3429 !important;
    }

    /* ═══ divider 弱化 ═══ */
    hr { border-color: #d8ddd2 !important; }

    /* ═══ 表格表头 ═══ */
    thead th { background: #f0f4ec !important; color: #2c4a34 !important; font-weight: 600 !important; }

    /* ═══ 侧边栏内 radio/checkbox 的选中态颜色 ═══ */
    [data-testid="stSidebar"] .st-cb,
    [data-testid="stSidebar"] .st-cg { accent-color: #3a7d44; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
# 标题区（Hero）
# ═══════════════════════════════════════════
st.markdown('<p class="hero-title"><i class="fa-solid fa-leaf" style="color:#3a7d44;"></i> 植物叶片滞尘数据分析与可视化系统</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">长江流域亚热带城市群 · 全国三大气候区 · v5 全国尺度</p>', unsafe_allow_html=True)
st.markdown('<div class="hero-bar"></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════
# 数据快照芯片
# ═══════════════════════════════════════════
sc1, sc2, sc3, sc4, sc5, sc6, sc7 = st.columns(7)
chip_html = '<div class="stat-chip"><span class="fa-icon"><i class="fa-solid {}"></i></span> <div class="num">{}</div><div class="txt">{}</div></div>'

with sc1:
    st.markdown(chip_html.format('fa-database', '4,596', '总记录'), unsafe_allow_html=True)
with sc2:
    st.markdown(chip_html.format('fa-tree', '593', '物种'), unsafe_allow_html=True)
with sc3:
    st.markdown(chip_html.format('fa-city', '85', '城市'), unsafe_allow_html=True)
with sc4:
    st.markdown(chip_html.format('fa-file-lines', '220', '论文'), unsafe_allow_html=True)
with sc5:
    st.markdown(chip_html.format('fa-globe-asia', '3', '气候区'), unsafe_allow_html=True)
with sc6:
    st.markdown(chip_html.format('fa-microscope', '99%', '叶片因子'), unsafe_allow_html=True)
with sc7:
    st.markdown(chip_html.format('fa-chart-line', '95%', 'TSP 覆盖'), unsafe_allow_html=True)

st.divider()

# ═══════════════════════════════════════════
# 功能卡片
# ═══════════════════════════════════════════
st.markdown('<p class="section-heading"><i class="fa-solid fa-cubes" style="color:#3a7d44;"></i> 功能模块</p>', unsafe_allow_html=True)

fc1, fc2, fc3 = st.columns(3)

with fc1:
    st.markdown("""
    <div class="feature-card">
        <div class="icon-circle" style="background:#3a7d44;"><i class="fa-solid fa-comments"></i></div>
        <h3>智能问答</h3>
        <p>用自然语言查询滞尘数据。Qwen2.5-7B 本地推理驱动，支持多轮对话。<br>
        <i style="color:#6b7a65;">"南京冬季香樟的TSP是多少？"<br>"有毛的植物滞尘效果更好吗？"</i></p>
        <p style="color:#3a7d44; font-size:0.78rem; font-weight:600;"><i class="fa-solid fa-circle-info"></i> 需 Ollama 运行 Qwen2.5-7B</p>
    </div>
    """, unsafe_allow_html=True)

with fc2:
    st.markdown("""
    <div class="feature-card">
        <div class="icon-circle" style="background:#c4944a;"><i class="fa-solid fa-microscope"></i></div>
        <h3>形态因子分析 <span style="font-size:0.7rem; color:#c4944a; font-weight:700;">★核心</span></h3>
        <p>交互式探索叶片表面特征、毛被、蜡质、叶形、气孔对滞尘效果的影响。<br>
        <i style="color:#6b7a65;">箱线图 · 散点图 · 统计对比 · 气候区分组 · Top 15 物种</i></p>
        <p style="color:#c4944a; font-size:0.78rem; font-weight:600;"><i class="fa-solid fa-star"></i> 论文核心论点可视化</p>
    </div>
    """, unsafe_allow_html=True)

with fc3:
    st.markdown("""
    <div class="feature-card">
        <div class="icon-circle" style="background:#3b82b0;"><i class="fa-solid fa-chart-pie"></i></div>
        <h3>数据总览</h3>
        <p>全局统计仪表盘。KPI卡片 · 气候区分布 · 城市Top25 · 生活型·功能区 · TSP分布直方图 · 论文列表<br>
        <i style="color:#6b7a65;">一键了解数据集全貌</i></p>
        <p style="color:#3b82b0; font-size:0.78rem; font-weight:600;"><i class="fa-solid fa-table-list"></i> 实时统计，数据可追溯</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ═══════════════════════════════════════════
# 技术栈 + 版本信息
# ═══════════════════════════════════════════
col_tech, col_ver = st.columns([2, 1])

with col_tech:
    st.markdown('<p class="section-heading"><i class="fa-solid fa-gear" style="color:#3a7d44;"></i> 技术栈</p>', unsafe_allow_html=True)
    st.markdown("""
    | 组件 | 技术 | 说明 |
    |------|------|------|
    | 前端 | Streamlit 1.58 | 多页面应用，零前端代码 |
    | 图表 | Plotly 6.8 | 交互式图表，支持悬停/缩放/筛选 |
    | 推理 | Qwen2.5-7B (Ollama) | 本地推理，数据不出本机 |
    | 数据 | Pandas + CSV | 4596条实测数据，即时过滤聚合 |
    | 形态因子 | FRPS 中国植物志 | 238属级叶片特征数据库 |
    """)

with col_ver:
    st.markdown('<p class="section-heading"><i class="fa-solid fa-box" style="color:#3a7d44;"></i> 数据版本</p>', unsafe_allow_html=True)
    st.markdown('<span class="version-badge"><i class="fa-solid fa-seedling" style="margin-right:4px;"></i>v5 第四批</span>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.85rem; color:#6b7a65; line-height:1.7; margin-top:8px;">
    <b>发布日期</b>: 2026-06-24<br>
    <b>数据来源</b>: 220 篇论文<br>
    <b>覆盖范围</b>: 85 城 / 3 气候区<br>
    <b>方法学</b>: A / B / C 三级透明<br>
    <b>叶片因子</b>: 99.0% FRPS 覆盖<br>
    <b>QA 系统</b>: aliases 104 物种 + 117 城市
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption("💡 所有数据 100% 可验证 — 每个统计数字均可追溯至对应的原始论文记录。双击桌面「植物滞尘Q&A-网页版.bat」即可启动。")
