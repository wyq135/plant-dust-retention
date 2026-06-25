"""
📊 数据总览 — 全局统计仪表盘
城市/物种/气候区分布 + 数据质量概览
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ═══════════════════════════════════════════
# 全局 CSS（FA CDN + 卡片 + 侧边栏）
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
    .section-heading {
        font-family: 'Noto Serif SC', 'Source Han Serif SC', 'STSong', 'SimSun', serif;
        font-size: 1.1rem; font-weight: 600; color: #2c4a34;
        border-bottom: 2px solid #c8dcc8; padding-bottom: 6px;
        margin-top: 14px; margin-bottom: 8px;
    }
    hr { border-color: #d8ddd2 !important; }
    thead th { background: #f0f4ec !important; color: #2c4a34 !important; font-weight: 600 !important; }

    /* KPI 卡片（HTML） */
    .kpi-card {
        background: #ffffff; border-radius: 12px; padding: 16px 18px; text-align: center;
        border: 1px solid #e0e4dc; border-left: 4px solid #3a7d44;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        transition: box-shadow 0.2s ease, transform 0.15s ease;
    }
    .kpi-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.09); transform: translateY(-1px); }
    .kpi-card .kpi-value {
        font-family: 'Noto Serif SC', 'Source Han Serif SC', 'STSong', 'SimSun', serif;
        font-size: 1.7rem; font-weight: 700; color: #2d3429;
    }
    .kpi-card .kpi-label { font-size: 0.78rem; color: #6b7a65; margin-top: 2px; }
    .kpi-card .kpi-icon { font-size: 1rem; color: #3a7d44; display: block; margin-bottom: 4px; }

    /* 质量指标卡片（HTML） */
    .quality-card {
        background: #ffffff; border-radius: 10px; padding: 12px 16px; text-align: center;
        border: 1px solid #e0e4dc; border-left: 3px solid #c4944a;
        box-shadow: 0 1px 6px rgba(0,0,0,0.04);
    }
    .quality-card .q-value {
        font-family: 'Noto Serif SC', 'Source Han Serif SC', 'STSong', 'SimSun', serif;
        font-size: 1.15rem; font-weight: 700; color: #2d3429;
    }
    .quality-card .q-label { font-size: 0.72rem; color: #6b7a65; }
    .quality-card .q-delta { font-size: 0.7rem; color: #3a7d44; font-weight: 600; }

    /* 统计表格内数字衬线 */
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-family: 'Noto Serif SC', 'Source Han Serif SC', 'STSong', 'SimSun', serif;
        font-size: 1.4rem !important; font-weight: 700 !important; color: #2d3429 !important;
    }
    [data-testid="stMetric"] label { font-size: 0.78rem !important; color: #6b7a65 !important; font-weight: 500 !important; }
</style>
""", unsafe_allow_html=True)

st.title("数据总览")
st.caption("长江流域亚热带城市植物叶片滞尘数据集 — v5 全国尺度 (2026-06-24)")

# ═══════════════════════════════════════════
# 数据加载
# ═══════════════════════════════════════════

@st.cache_data
def load_data():
    data_dir = Path(__file__).resolve().parent.parent / "data"
    df = pd.read_csv(data_dir / "dataset.csv")
    for col in ['tsp_g_m2', 'pm10_g_m2', 'pm2_5_g_m2']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

df = load_data()

# ═══════════════════════════════════════════
# KPI 卡片（白底+阴影+绿色左边条）
# ═══════════════════════════════════════════

st.markdown('<p class="section-heading"><i class="fa-solid fa-gauge-high" style="color:#3a7d44;"></i> 核心指标</p>', unsafe_allow_html=True)
k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:
    st.markdown(f'<div class="kpi-card"><span class="kpi-icon"><i class="fa-solid fa-database"></i></span><div class="kpi-value">{len(df):,}</div><div class="kpi-label">总记录数</div></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="kpi-card"><span class="kpi-icon"><i class="fa-solid fa-tree"></i></span><div class="kpi-value">{df["plant_species"].nunique()}</div><div class="kpi-label">物种数</div></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="kpi-card"><span class="kpi-icon"><i class="fa-solid fa-city"></i></span><div class="kpi-value">{df["city"].nunique()}</div><div class="kpi-label">城市数</div></div>', unsafe_allow_html=True)
with k4:
    n_papers = df['reference_short'].nunique() if 'reference_short' in df.columns else df['reference'].nunique()
    st.markdown(f'<div class="kpi-card"><span class="kpi-icon"><i class="fa-solid fa-file-lines"></i></span><div class="kpi-value">{n_papers}</div><div class="kpi-label">论文数</div></div>', unsafe_allow_html=True)
with k5:
    st.markdown(f'<div class="kpi-card"><span class="kpi-icon"><i class="fa-solid fa-globe-asia"></i></span><div class="kpi-value">{df["climate_zone"].nunique()}</div><div class="kpi-label">气候区</div></div>', unsafe_allow_html=True)
with k6:
    tsp_median = df['tsp_g_m2'].dropna().median()
    st.markdown(f'<div class="kpi-card"><span class="kpi-icon"><i class="fa-solid fa-chart-line"></i></span><div class="kpi-value">{tsp_median:.2f}</div><div class="kpi-label">TSP 中位数 (g/m²)</div></div>', unsafe_allow_html=True)

# 数据质量指标第二行
st.markdown("")
q1, q2, q3, q4, q5, q6 = st.columns(6)
with q1:
    a_pct = (df['method_level'] == 'A').sum()
    st.markdown(f'<div class="quality-card"><div class="q-value">{a_pct}</div><div class="q-label"><i class="fa-solid fa-microscope"></i> A级数据</div><div class="q-delta">{a_pct/len(df)*100:.1f}%</div></div>', unsafe_allow_html=True)
with q2:
    tsp_cov = df['tsp_g_m2'].notna().sum()
    st.markdown(f'<div class="quality-card"><div class="q-value">{tsp_cov}</div><div class="q-label"><i class="fa-solid fa-chart-area"></i> TSP覆盖</div><div class="q-delta">{tsp_cov/len(df)*100:.1f}%</div></div>', unsafe_allow_html=True)
with q3:
    pm10_cov = df['pm10_g_m2'].notna().sum()
    st.markdown(f'<div class="quality-card"><div class="q-value">{pm10_cov}</div><div class="q-label"><i class="fa-solid fa-chart-bar"></i> PM10覆盖</div><div class="q-delta">{pm10_cov/len(df)*100:.1f}%</div></div>', unsafe_allow_html=True)
with q4:
    pm25_cov = df['pm2_5_g_m2'].notna().sum()
    st.markdown(f'<div class="quality-card"><div class="q-value">{pm25_cov}</div><div class="q-label"><i class="fa-solid fa-chart-simple"></i> PM2.5覆盖</div><div class="q-delta">{pm25_cov/len(df)*100:.1f}%</div></div>', unsafe_allow_html=True)
with q5:
    leaf_cov = df['leaf_surface'].notna().sum()
    st.markdown(f'<div class="quality-card"><div class="q-value">{leaf_cov}</div><div class="q-label"><i class="fa-solid fa-leaf"></i> 叶片因子</div><div class="q-delta">{leaf_cov/len(df)*100:.1f}%</div></div>', unsafe_allow_html=True)
with q6:
    nmr = df['needs_manual_review'].sum() if 'needs_manual_review' in df.columns else 0
    st.markdown(f'<div class="quality-card"><div class="q-value">{int(nmr)}</div><div class="q-label"><i class="fa-solid fa-triangle-exclamation"></i> 待人工复核</div><div class="q-delta">{int(nmr)/len(df)*100:.1f}%</div></div>', unsafe_allow_html=True)

st.divider()

# ═══════════════════════════════════════════
# 第一行：气候区 + 方法学
# ═══════════════════════════════════════════

col1, col2 = st.columns(2)

with col1:
    st.markdown('<p class="section-heading"><i class="fa-solid fa-globe-asia" style="color:#3a7d44;"></i> 气候区分布</p>', unsafe_allow_html=True)
    cz = df['climate_zone'].value_counts().reset_index()
    cz.columns = ['气候区', '记录数']
    fig_cz = px.pie(cz, values='记录数', names='气候区', color='气候区',
                     color_discrete_map={'北方': '#5470c6', '南方': '#91cc75', '西北': '#fac858'},
                     hole=0.4)
    fig_cz.update_traces(textposition='inside', textinfo='percent+label+value')
    fig_cz.update_layout(height=380, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_cz, use_container_width=True)

with col2:
    st.markdown('<p class="section-heading"><i class="fa-solid fa-microscope" style="color:#3a7d44;"></i> 方法学等级分布</p>', unsafe_allow_html=True)
    ml = df['method_level'].value_counts().reindex(['A', 'B', 'C']).reset_index()
    ml.columns = ['等级', '记录数']
    ml['说明'] = ['直接测量标准方法', '间接但有明确换算', '估算或方法不标准']
    fig_ml = px.bar(ml, x='等级', y='记录数', color='等级',
                     color_discrete_map={'A': '#3a7d44', 'B': '#3b82b0', 'C': '#c4944a'},
                     text='记录数', hover_data=['说明'])
    fig_ml.update_traces(textposition='outside')
    fig_ml.update_layout(showlegend=False, height=380, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_ml, use_container_width=True)

# ═══════════════════════════════════════════
# 第二行：城市 Top 25 + 生活型分布
# ═══════════════════════════════════════════

col3, col4 = st.columns(2)

with col3:
    st.markdown('<p class="section-heading"><i class="fa-solid fa-city" style="color:#3a7d44;"></i> 城市数据量 Top 25</p>', unsafe_allow_html=True)
    city_counts = df['city'].value_counts().nlargest(25).reset_index()
    city_counts.columns = ['城市', '记录数']
    fig_city = px.bar(city_counts, x='记录数', y='城市', orientation='h',
                       color='记录数', color_continuous_scale='Greens')
    fig_city.update_layout(height=520, yaxis={'categoryorder': 'total ascending'},
                          margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_city, use_container_width=True)

with col4:
    st.markdown('<p class="section-heading"><i class="fa-solid fa-leaf" style="color:#3a7d44;"></i> 生活型分布</p>', unsafe_allow_html=True)
    layer = df['layer'].value_counts().reset_index()
    layer.columns = ['生活型', '记录数']
    fig_layer = px.bar(layer, x='生活型', y='记录数', color='生活型',
                        color_discrete_sequence=px.colors.qualitative.Set2,
                        text='记录数')
    fig_layer.update_traces(textposition='outside')
    fig_layer.update_layout(showlegend=False, height=250, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_layer, use_container_width=True)

    st.markdown('<p class="section-heading"><i class="fa-solid fa-location-dot" style="color:#3a7d44;"></i> 功能区分布</p>', unsafe_allow_html=True)
    zone = df['functional_zone'].value_counts().reset_index()
    zone.columns = ['功能区', '记录数']
    fig_zone = px.bar(zone, x='记录数', y='功能区', orientation='h',
                       color='记录数', color_continuous_scale='Greens')
    fig_zone.update_layout(height=320, yaxis={'categoryorder': 'total ascending'},
                          margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_zone, use_container_width=True)

# ═══════════════════════════════════════════
# 第三行：TSP 分布 + 气候区×生活型交叉
# ═══════════════════════════════════════════

col5, col6 = st.columns(2)

with col5:
    st.markdown('<p class="section-heading"><i class="fa-solid fa-chart-line" style="color:#3a7d44;"></i> TSP 滞尘量分布</p>', unsafe_allow_html=True)
    tsp_data = df['tsp_g_m2'].dropna()
    tsp_data = tsp_data[(tsp_data > 0) & (tsp_data < 50)]
    fig_hist = px.histogram(tsp_data, nbins=60,
                             labels={'value': 'TSP (g/m²)'},
                             color_discrete_sequence=['#3a7d44'])
    fig_hist.add_vline(x=tsp_data.median(), line_dash="dash", line_color="#c4944a",
                        annotation_text=f"中位数={tsp_data.median():.2f}")
    fig_hist.add_vline(x=tsp_data.mean(), line_dash="dot", line_color="#e07b39",
                        annotation_text=f"均值={tsp_data.mean():.2f}")
    fig_hist.update_layout(height=380, margin=dict(l=10, r=10, t=40, b=10),
                           title=f"TSP 分布 (n={len(tsp_data):,}, 排除 >50 g/m² 的极端值)")
    st.plotly_chart(fig_hist, use_container_width=True)

with col6:
    st.markdown('<p class="section-heading"><i class="fa-solid fa-layer-group" style="color:#3a7d44;"></i> 气候区 × 生活型交叉分布</p>', unsafe_allow_html=True)
    cross = df.groupby(['climate_zone', 'layer']).size().reset_index(name='记录数')
    cross = cross[cross['记录数'] >= 3]
    fig_cross = px.bar(cross, x='climate_zone', y='记录数', color='layer',
                        barmode='group', color_discrete_sequence=px.colors.qualitative.Set2,
                        labels={'climate_zone': '气候区', 'layer': '生活型'})
    fig_cross.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_cross, use_container_width=True)

# ═══════════════════════════════════════════
# 第四行：数据覆盖 + 物种 Top 15
# ═══════════════════════════════════════════

col7, col8 = st.columns(2)

with col7:
    st.markdown('<p class="section-heading"><i class="fa-solid fa-chart-pie" style="color:#3a7d44;"></i> 数据指标覆盖</p>', unsafe_allow_html=True)
    total = len(df)
    tsp_cov_n = df['tsp_g_m2'].notna().sum()
    pm10_cov_n = df['pm10_g_m2'].notna().sum()
    pm25_cov_n = df['pm2_5_g_m2'].notna().sum()
    leaf_db_n = df['leaf_db_source'].notna().sum() if 'leaf_db_source' in df.columns else df['leaf_surface'].notna().sum()

    coverage = pd.DataFrame({
        '指标': ['TSP', 'PM10', 'PM2.5', '叶片因子(FRPS)'],
        '有数据': [tsp_cov_n, pm10_cov_n, pm25_cov_n, leaf_db_n],
        '缺失': [total - tsp_cov_n, total - pm10_cov_n, total - pm25_cov_n, total - leaf_db_n]
    })
    fig_cov = go.Figure()
    fig_cov.add_trace(go.Bar(name='有数据', y=coverage['指标'], x=coverage['有数据'],
                             orientation='h', marker_color='#3a7d44', text=coverage['有数据']))
    fig_cov.add_trace(go.Bar(name='缺失', y=coverage['指标'], x=coverage['缺失'],
                             orientation='h', marker_color='#e0e4dc', text=coverage['缺失']))
    fig_cov.update_layout(barmode='stack', height=250,
                          margin=dict(l=10, r=10, t=10, b=10),
                          legend=dict(orientation='h', yanchor='bottom', y=1.02))
    st.plotly_chart(fig_cov, use_container_width=True)

with col8:
    st.markdown('<p class="section-heading"><i class="fa-solid fa-trophy" style="color:#c4944a;"></i> 物种数据量 Top 15</p>', unsafe_allow_html=True)
    sp_top = df['plant_species'].value_counts().nlargest(15).reset_index()
    sp_top.columns = ['物种', '记录数']
    fig_sp = px.bar(sp_top, x='记录数', y='物种', orientation='h',
                     color='记录数', color_continuous_scale='Greens')
    fig_sp.update_layout(height=380, yaxis={'categoryorder': 'total ascending'},
                        margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_sp, use_container_width=True)

# ═══════════════════════════════════════════
# 底部：完整论文列表
# ═══════════════════════════════════════════

st.divider()
with st.expander("📄 收录论文列表（按数据量排序，点击展开）"):
    if 'reference_short' in df.columns:
        ref_col = 'reference_short'
    else:
        ref_col = 'reference'
    paper_stats = df.groupby(ref_col).agg(
        记录数=('plant_species', 'count'),
        物种数=('plant_species', 'nunique'),
        代表城市=('city', lambda x: ', '.join(sorted(x.unique())[:3]))
    ).sort_values('记录数', ascending=False).reset_index()
    paper_stats.columns = ['论文', '记录数', '物种数', '代表城市（前3）']
    st.dataframe(paper_stats, use_container_width=True, height=400)

st.divider()
st.caption("💡 所有统计与图表均基于 Pandas/Plotly 实时计算，数据来源可追溯至每篇原始论文。悬停图表查看详情。")
