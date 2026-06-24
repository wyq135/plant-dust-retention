"""
📊 数据总览 — 全局统计仪表盘
城市/物种/气候区分布 + 数据质量概览
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ── 自定义 CSS ──
st.markdown("""
<style>
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px; padding: 16px 20px; text-align: center;
        color: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .kpi-card .kpi-value { font-size: 1.8rem; font-weight: 800; }
    .kpi-card .kpi-label { font-size: 0.8rem; opacity: 0.9; margin-top: 4px; }
    .kpi-card.green { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: #1a3a2a; }
    .kpi-card.blue { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: #1a2a3a; }
    .kpi-card.orange { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: #3a1a2a; }
    .kpi-card.purple { background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%); color: #2a1a3a; }
    .kpi-card.teal { background: linear-gradient(135deg, #0093E9 0%, #80D0C7 100%); }
    .kpi-card.coral { background: linear-gradient(135deg, #ff6a88 0%, #ff99ac 100%); }
    .section-header {
        border-left: 4px solid #667eea; padding-left: 12px;
        margin: 20px 0 10px 0; font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 数据总览")
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
# KPI 卡片（彩色渐变）
# ═══════════════════════════════════════════

st.markdown('<p class="section-header">核心指标</p>', unsafe_allow_html=True)
k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{len(df):,}</div><div class="kpi-label">📋 总记录数</div></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="kpi-card green"><div class="kpi-value">{df["plant_species"].nunique()}</div><div class="kpi-label">🌳 物种数</div></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="kpi-card blue"><div class="kpi-value">{df["city"].nunique()}</div><div class="kpi-label">🏙️ 城市数</div></div>', unsafe_allow_html=True)
with k4:
    n_papers = df['reference_short'].nunique() if 'reference_short' in df.columns else df['reference'].nunique()
    st.markdown(f'<div class="kpi-card orange"><div class="kpi-value">{n_papers}</div><div class="kpi-label">📄 论文数</div></div>', unsafe_allow_html=True)
with k5:
    st.markdown(f'<div class="kpi-card purple"><div class="kpi-value">{df["climate_zone"].nunique()}</div><div class="kpi-label">🌍 气候区</div></div>', unsafe_allow_html=True)
with k6:
    tsp_median = df['tsp_g_m2'].dropna().median()
    st.markdown(f'<div class="kpi-card coral"><div class="kpi-value">{tsp_median:.2f}</div><div class="kpi-label">📉 TSP 中位数 (g/m²)</div></div>', unsafe_allow_html=True)

# 数据质量指标第二行
st.markdown("")
q1, q2, q3, q4, q5, q6 = st.columns(6)
with q1:
    a_pct = (df['method_level'] == 'A').sum()
    st.metric("🔬 A级数据", f"{a_pct}条", f"{a_pct/len(df)*100:.1f}%")
with q2:
    tsp_cov = df['tsp_g_m2'].notna().sum()
    st.metric("📈 TSP覆盖", f"{tsp_cov}条", f"{tsp_cov/len(df)*100:.1f}%")
with q3:
    pm10_cov = df['pm10_g_m2'].notna().sum()
    st.metric("📊 PM10覆盖", f"{pm10_cov}条", f"{pm10_cov/len(df)*100:.1f}%")
with q4:
    pm25_cov = df['pm2_5_g_m2'].notna().sum()
    st.metric("📊 PM2.5覆盖", f"{pm25_cov}条", f"{pm25_cov/len(df)*100:.1f}%")
with q5:
    leaf_cov = df['leaf_surface'].notna().sum()
    st.metric("🍃 叶片因子", f"{leaf_cov}条", f"{leaf_cov/len(df)*100:.1f}%")
with q6:
    nmr = df['needs_manual_review'].sum() if 'needs_manual_review' in df.columns else 0
    st.metric("⚠️ 待人工复核", f"{int(nmr)}条")

st.divider()

# ═══════════════════════════════════════════
# 第一行：气候区 + 方法学
# ═══════════════════════════════════════════

col1, col2 = st.columns(2)

with col1:
    st.subheader("🌍 气候区分布")
    cz = df['climate_zone'].value_counts().reset_index()
    cz.columns = ['气候区', '记录数']
    fig_cz = px.pie(cz, values='记录数', names='气候区', color='气候区',
                     color_discrete_map={'北方': '#5470c6', '南方': '#91cc75', '西北': '#fac858'},
                     hole=0.4)
    fig_cz.update_traces(textposition='inside', textinfo='percent+label+value')
    fig_cz.update_layout(height=380, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_cz, use_container_width=True)

with col2:
    st.subheader("🔬 方法学等级分布")
    ml = df['method_level'].value_counts().reindex(['A', 'B', 'C']).reset_index()
    ml.columns = ['等级', '记录数']
    ml['说明'] = ['直接测量标准方法', '间接但有明确换算', '估算或方法不标准']
    fig_ml = px.bar(ml, x='等级', y='记录数', color='等级',
                     color_discrete_map={'A': '#43e97b', 'B': '#4facfe', 'C': '#fa709a'},
                     text='记录数', hover_data=['说明'])
    fig_ml.update_traces(textposition='outside')
    fig_ml.update_layout(showlegend=False, height=380, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_ml, use_container_width=True)

# ═══════════════════════════════════════════
# 第二行：城市 Top 25 + 生活型分布
# ═══════════════════════════════════════════

col3, col4 = st.columns(2)

with col3:
    st.subheader("🏙️ 城市数据量 Top 25")
    city_counts = df['city'].value_counts().nlargest(25).reset_index()
    city_counts.columns = ['城市', '记录数']
    fig_city = px.bar(city_counts, x='记录数', y='城市', orientation='h',
                       color='记录数', color_continuous_scale='Viridis')
    fig_city.update_layout(height=520, yaxis={'categoryorder': 'total ascending'},
                          margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_city, use_container_width=True)

with col4:
    st.subheader("🌿 生活型分布")
    layer = df['layer'].value_counts().reset_index()
    layer.columns = ['生活型', '记录数']
    fig_layer = px.bar(layer, x='生活型', y='记录数', color='生活型',
                        color_discrete_sequence=px.colors.qualitative.Set2,
                        text='记录数')
    fig_layer.update_traces(textposition='outside')
    fig_layer.update_layout(showlegend=False, height=250, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_layer, use_container_width=True)

    st.subheader("📍 功能区分布")
    zone = df['functional_zone'].value_counts().reset_index()
    zone.columns = ['功能区', '记录数']
    fig_zone = px.bar(zone, x='记录数', y='功能区', orientation='h',
                       color='记录数', color_continuous_scale='Teal')
    fig_zone.update_layout(height=320, yaxis={'categoryorder': 'total ascending'},
                          margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_zone, use_container_width=True)

# ═══════════════════════════════════════════
# 第三行：TSP 分布 + 气候区×生活型交叉
# ═══════════════════════════════════════════

col5, col6 = st.columns(2)

with col5:
    st.subheader("📈 TSP 滞尘量分布")
    tsp_data = df['tsp_g_m2'].dropna()
    tsp_data = tsp_data[(tsp_data > 0) & (tsp_data < 50)]
    fig_hist = px.histogram(tsp_data, nbins=60,
                             labels={'value': 'TSP (g/m²)'},
                             color_discrete_sequence=['#667eea'])
    fig_hist.add_vline(x=tsp_data.median(), line_dash="dash", line_color="#ff6a88",
                        annotation_text=f"中位数={tsp_data.median():.2f}")
    fig_hist.add_vline(x=tsp_data.mean(), line_dash="dot", line_color="#fa709a",
                        annotation_text=f"均值={tsp_data.mean():.2f}")
    fig_hist.update_layout(height=380, margin=dict(l=10, r=10, t=40, b=10),
                           title=f"TSP 分布 (n={len(tsp_data):,}, 排除>50 g/m²的极端值)")
    st.plotly_chart(fig_hist, use_container_width=True)

with col6:
    st.subheader("🌍×🌿 气候区×生活型交叉分布")
    cross = df.groupby(['climate_zone', 'layer']).size().reset_index(name='记录数')
    # 过滤掉极小样本
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
    st.subheader("📊 数据指标覆盖")
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
                             orientation='h', marker_color='#43e97b', text=coverage['有数据']))
    fig_cov.add_trace(go.Bar(name='缺失', y=coverage['指标'], x=coverage['缺失'],
                             orientation='h', marker_color='#e0e0e0', text=coverage['缺失']))
    fig_cov.update_layout(barmode='stack', height=250,
                          margin=dict(l=10, r=10, t=10, b=10),
                          legend=dict(orientation='h', yanchor='bottom', y=1.02))
    st.plotly_chart(fig_cov, use_container_width=True)

with col8:
    st.subheader("🏆 物种数据量 Top 15")
    sp_top = df['plant_species'].value_counts().nlargest(15).reset_index()
    sp_top.columns = ['物种', '记录数']
    fig_sp = px.bar(sp_top, x='记录数', y='物种', orientation='h',
                     color='记录数', color_continuous_scale='Magma')
    fig_sp.update_layout(height=380, yaxis={'categoryorder': 'total ascending'},
                        margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_sp, use_container_width=True)

# ═══════════════════════════════════════════
# 底部：完整论文列表（可展开）
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

# 底部信息
st.divider()
st.caption("💡 所有统计与图表均基于 Pandas/Plotly 实时计算，数据来源可追溯至每篇原始论文。悬停图表查看详情。")
