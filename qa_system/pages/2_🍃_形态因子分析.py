"""
🍃 形态因子分析 — v2 核心页面
探索叶片表面特征、毛被、蜡质层等形态因子对滞尘效果的影响
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ── 自定义 CSS ──
st.markdown("""
<style>
    .trait-stat-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
        border-radius: 10px;
        padding: 12px 16px;
        text-align: center;
        border: 1px solid #dee2e6;
    }
    .trait-stat-card .value { font-size: 1.4rem; font-weight: 700; color: #2c3e50; }
    .trait-stat-card .label { font-size: 0.75rem; color: #6c757d; }
    .warning-banner {
        background: #fff3cd; border: 1px solid #ffc107; border-radius: 8px;
        padding: 10px 16px; color: #856404;
    }
</style>
""", unsafe_allow_html=True)

st.title("🍃 叶片形态因子与滞尘效果分析")
st.caption("探索叶片微观形态特征（叶表面/毛被/蜡质/叶形/气孔）如何影响大气颗粒物滞留能力")

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
# 形态因子文本 → 类别解析
# ═══════════════════════════════════════════

def categorize_leaf_surface(text):
    """解析 leaf_surface 文本为类别（FRPS属级描述为文本基础）"""
    if pd.isna(text) or not str(text).strip():
        return "未标注"
    t = str(text).lower()
    if any(k in t for k in ['粗糙', 'rough', 'scabrous', '具疣']):
        return "粗糙"
    if any(k in t for k in ['有毛', '被毛', '柔毛', '绒毛', '短毛', '长毛', '绵毛', '星状毛',
                              'pubescent', 'hairy', 'pilose', 'tomentose', '毛被', '具毛']):
        return "有毛"
    if any(k in t for k in ['蜡质', '蜡层', 'waxy', '白粉', '粉霜', '粉白']):
        return "蜡质/粉霜"
    if any(k in t for k in ['光滑', '平滑', 'glabrous', '无毛', '两面无毛']):
        return "光滑无毛"
    if any(k in t for k in ['皱', 'rugose', '泡状', '皱缩']):
        return "皱缩/泡状"
    if any(k in t for k in ['革质', 'leathery', '厚革质']):
        return "革质"
    if any(k in t for k in ['纸质', '膜质', 'membranous']):
        return "纸质/膜质"
    if any(k in t for k in ['光泽', '发亮', 'shining', 'shiny']):
        return "有光泽"
    if any(k in t for k in ['具腺', '腺点', '腺体', 'gland']):
        return "具腺点"
    if any(k in t for k in ['具齿', '锯齿', 'serrate', 'dentate', '全缘']):
        return "具齿/全缘"
    if any(k in t for k in ['绿色', '深绿', '浅绿', '灰白', '灰绿', '黄绿', '暗绿',
                              '上面', '下面', '背面', '中脉', '侧脉', '叶脉']):
        return "颜色为主(纹理未详述)"
    return "纹理未详述"

def categorize_trichomes(text):
    if pd.isna(text) or not str(text).strip():
        return "未标注"
    t = str(text).lower()
    if any(k in t for k in ['腺毛', 'glandular']):
        return "腺毛"
    if any(k in t for k in ['星状毛', 'stellate', '鳞片']):
        return "星状毛/鳞片"
    if any(k in t for k in ['无毛', 'glabrous', 'absent', '光滑']):
        return "无毛"
    if any(k in t for k in ['有毛', '被毛', '柔毛', '绒毛', '短毛', '长毛', '硬毛',
                              'pubescent', 'hairy', 'pilose', 'tomentose', 'hirsute',
                              '疏毛', '密毛', '绵毛', '刚毛', '糙毛']):
        return "有毛"
    return "有毛"

def categorize_wax(text):
    if pd.isna(text) or not str(text).strip():
        return "未标注"
    t = str(text).lower()
    if any(k in t for k in ['有', '蜡', 'wax', 'present', '白粉', '粉霜']):
        return "有蜡质"
    if any(k in t for k in ['无', 'absent', 'none']):
        return "无蜡质"
    return "其他"

def extract_leaf_shape(text):
    if pd.isna(text) or not str(text).strip():
        return "未标注"
    t = str(text)
    patterns = [
        ('披针形', '披针形'), ('椭圆形', '椭圆形'), ('卵形', '卵形'),
        ('倒卵形', '倒卵形'), ('线形', '线形/条形'), ('圆形', '圆形'),
        ('心形', '心形'), ('扇形', '扇形'), ('针形', '针形/鳞形'),
        ('长圆形', '长圆形'), ('匙形', '匙形'), ('菱形', '菱形'),
        ('三角形', '三角形'), ('肾形', '肾形'), ('掌状', '掌状'),
    ]
    for keyword, label in patterns:
        if keyword in t:
            return label
    if any(k in t for k in ['针', '鳞', '钻']):
        return "针形/鳞形"
    return "其他"

def categorize_stomata(text):
    if pd.isna(text) or not str(text).strip():
        return "未标注"
    t = str(text).lower()
    if any(k in t for k in ['下陷', 'sunken']):
        return "下陷型"
    if any(k in t for k in ['突出', 'raised']):
        return "突出型"
    if any(k in t for k in ['密', '多', 'high density']):
        return "高密度"
    if any(k in t for k in ['疏', '少', 'low density']):
        return "低密度"
    return "有描述"

@st.cache_data
def add_trait_categories(_df):
    df = _df.copy()
    df['叶表面类别'] = df['leaf_surface'].apply(categorize_leaf_surface)
    df['毛被类别'] = df['trichomes'].apply(categorize_trichomes)
    df['蜡质类别'] = df['wax_layer'].apply(categorize_wax)
    df['叶形类别'] = df['leaf_shape'].apply(extract_leaf_shape)
    df['气孔类别'] = df['stomata'].apply(categorize_stomata)
    return df

df = add_trait_categories(df)

# ═══════════════════════════════════════════
# 侧边栏
# ═══════════════════════════════════════════

with st.sidebar:
    st.header("🔍 筛选条件")

    pm_label = st.selectbox("颗粒物类型", ["TSP", "PM10", "PM2.5"], index=0)
    pm_col = {'TSP': 'tsp_g_m2', 'PM10': 'pm10_g_m2', 'PM2.5': 'pm2_5_g_m2'}[pm_label]

    st.divider()

    st.subheader("🌍 数据范围")
    climate_options = df['climate_zone'].dropna().unique().tolist()
    selected_climate = st.multiselect("气候区", climate_options, default=climate_options,
                                       help="北方=温带季风/大陆性, 南方=亚热带/热带, 西北=干旱/半干旱")

    layer_options = ['乔木', '灌木', '草本', '地被', '藤本']
    available_layers = [l for l in layer_options if l in df['layer'].values]
    selected_layers = st.multiselect("生活型", available_layers, default=available_layers[:3])

    ml_options = ['A', 'B', 'C']
    selected_ml = st.multiselect("方法学等级", ml_options, default=['A', 'B'],
                                  help="A=直接测量标准方法, B=间接但有明确换算, C=估算或方法不标准")

    st.divider()

    st.subheader("🍃 形态因子维度")
    trait_display = st.selectbox(
        "选择要分析的形态特征",
        ["叶表面特征 (leaf_surface)", "毛被特征 (trichomes)",
         "蜡质层 (wax_layer)", "叶形 (leaf_shape)", "气孔特征 (stomata)"],
        index=0
    )
    trait_map = {
        "叶表面特征 (leaf_surface)": '叶表面类别',
        "毛被特征 (trichomes)": '毛被类别',
        "蜡质层 (wax_layer)": '蜡质类别',
        "叶形 (leaf_shape)": '叶形类别',
        "气孔特征 (stomata)": '气孔类别',
    }
    trait_col = trait_map[trait_display]

    st.divider()
    st.caption(f"📊 总数据集: 4,596条 | 叶片因子: 99.0%覆盖")

# ═══════════════════════════════════════════
# 数据过滤
# ═══════════════════════════════════════════

filtered = df[
    (df['climate_zone'].isin(selected_climate)) &
    (df['layer'].isin(selected_layers)) &
    (df['method_level'].isin(selected_ml)) &
    (df[pm_col].notna()) & (df[pm_col] > 0) &
    (df[trait_col].notna())
]

categories_in_use = filtered[trait_col].value_counts()

if filtered.empty:
    st.warning("⚠️ 当前筛选条件下无数据，请调整左侧条件。")
    st.stop()

# ═══════════════════════════════════════════
# 稀疏维度警告
# ═══════════════════════════════════════════

SPARSE_WARNINGS = {
    '蜡质类别': ('wax_layer',
        '蜡质层数据仅来自 12 篇论文的 SEM 观测，非 FRPS 属级描述。'
        '大部分记录的蜡质层信息已包含在 leaf_surface 文本中（如"蜡质/粉霜"）。'),
    '气孔类别': ('stomata',
        '气孔数据仅来自 15 篇论文的 SEM 观测，非 FRPS 属级描述。'
        '如需了解气孔特征的物种分布，建议查看叶表面文本中的气孔相关描述。'),
}
if trait_col in SPARSE_WARNINGS:
    _, msg = SPARSE_WARNINGS[trait_col]
    n_filtered = filtered[trait_col].notna().sum()
    st.markdown(f"""
    <div class="warning-banner">
        <b>⚠️ 数据稀疏提醒</b>：{msg} 当前筛选下仅 <b>{n_filtered}</b> 条可用记录。
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════
# 统计卡片
# ═══════════════════════════════════════════

st.subheader("📊 统计概览")
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(f'<div class="trait-stat-card"><div class="value">{len(filtered):,}</div><div class="label">📋 记录数</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="trait-stat-card"><div class="value">{filtered["plant_species"].nunique()}</div><div class="label">🌳 物种数</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="trait-stat-card"><div class="value">{filtered["city"].nunique()}</div><div class="label">🏙️ 城市数</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="trait-stat-card"><div class="value">{filtered[pm_col].mean():.2f}</div><div class="label">📈 {pm_label} 均值 (g/m²)</div></div>', unsafe_allow_html=True)
with c5:
    st.markdown(f'<div class="trait-stat-card"><div class="value">{filtered[pm_col].median():.2f}</div><div class="label">📉 {pm_label} 中位数 (g/m²)</div></div>', unsafe_allow_html=True)

st.divider()

# ═══════════════════════════════════════════
# 图表区
# ═══════════════════════════════════════════

valid_cats = categories_in_use[categories_in_use >= 3].index.tolist()
plot_df = filtered[filtered[trait_col].isin(valid_cats)]

# ── 固定颜色映射 ──
TRAIT_COLORS = {
    '光滑无毛': '#66bb6a', '粗糙': '#ef5350', '有毛': '#ffa726',
    '蜡质/粉霜': '#42a5f5', '革质': '#8d6e63', '有光泽': '#ab47bc',
    '纸质/膜质': '#ffca28', '皱缩/泡状': '#78909c', '具腺点': '#26a69a',
    '具齿/全缘': '#5c6bc0', '颜色为主(纹理未详述)': '#bdbdbd', '纹理未详述': '#e0e0e0',
    '无毛': '#66bb6a', '星状毛/鳞片': '#ab47bc', '腺毛': '#ef5350',
    '有蜡质': '#42a5f5', '无蜡质': '#bdbdbd', '其他': '#e0e0e0',
    '下陷型': '#5c6bc0', '突出型': '#ef5350', '高密度': '#ffa726', '低密度': '#66bb6a', '有描述': '#bdbdbd',
    '未标注': '#eeeeee',
}
cat_colors = {cat: TRAIT_COLORS.get(cat, '#90a4ae') for cat in valid_cats}

trait_label = trait_display.split('(')[0].strip()

col_left, col_right = st.columns([2, 1])

with col_left:
    # --- 箱线图 ---
    st.subheader(f"「{trait_label}」对 {pm_label} 滞尘量的影响")
    fig_box = px.box(
        plot_df, x=trait_col, y=pm_col, color=trait_col,
        points="outliers",
        color_discrete_map=cat_colors,
        labels={trait_col: '', pm_col: f'{pm_label} (g/m²)'},
        category_orders={trait_col: valid_cats}
    )
    fig_box.update_layout(showlegend=False, height=500,
                          margin=dict(l=10, r=10, t=40, b=10),
                          plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_box, use_container_width=True)

    # --- 散点图 ---
    st.subheader("物种级别数据点分布")
    hover_cols = ['plant_species', 'city', 'climate_zone']
    hover_cols = [c for c in hover_cols if c in plot_df.columns]
    fig_strip = px.strip(
        plot_df, x=trait_col, y=pm_col, color=trait_col,
        hover_data=hover_cols,
        color_discrete_map=cat_colors,
        title="每个点 = 一条实测记录（悬停查看物种/城市/气候区）",
        labels={trait_col: '', pm_col: f'{pm_label} (g/m²)'},
        category_orders={trait_col: valid_cats}
    )
    fig_strip.update_layout(showlegend=False, height=400, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_strip, use_container_width=True)

with col_right:
    # --- 类别统计表 ---
    st.subheader("各类别统计")
    stats_rows = []
    for cat in valid_cats:
        subset = plot_df[plot_df[trait_col] == cat]
        stats_rows.append({
            '类别': cat,
            '记录': len(subset),
            '物种数': subset['plant_species'].nunique(),
            f'{pm_label}均值': f"{subset[pm_col].mean():.2f}",
            f'{pm_label}中位': f"{subset[pm_col].median():.2f}",
            f'{pm_label}最大': f"{subset[pm_col].max():.2f}",
        })
    stats_df = pd.DataFrame(stats_rows)
    st.dataframe(stats_df, use_container_width=True, hide_index=True,
                 column_config={'类别': st.column_config.TextColumn(width='small')})

    # --- Top 15 物种 ---
    st.subheader(f"🏆 {pm_label} 滞尘量 Top 15 物种")
    top15 = filtered.groupby('plant_species').agg(
        **{f'{pm_label}中位数': (pm_col, 'median'),
           '记录数': (pm_col, 'count')}
    ).query('记录数 >= 2').nlargest(15, f'{pm_label}中位数').reset_index()
    top15.columns = ['物种', f'{pm_label}中位数(g/m²)', '记录数']
    st.dataframe(top15, use_container_width=True, hide_index=True)

    # --- 按气候区分组对比 ---
    if len(selected_climate) > 1:
        st.subheader(f"🌍 气候区分组对比")
        climate_stats = filtered.groupby('climate_zone').agg(
            **{f'{pm_label}均值': (pm_col, 'mean'),
               '记录数': (pm_col, 'count')}
        ).round(2).reset_index()
        climate_stats.columns = ['气候区', f'{pm_label}均值(g/m²)', '记录数']
        st.dataframe(climate_stats, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════
# 底部：当前筛选数据表（可下载）
# ═══════════════════════════════════════════

st.divider()
with st.expander("📋 查看当前筛选的原始数据（可下载 CSV）"):
    show_cols = ['plant_species', 'latin_name', 'city', 'climate_zone',
                 trait_col, pm_col, 'layer', 'functional_zone', 'sampling_season', 'reference_short']
    show_cols = [c for c in show_cols if c in filtered.columns]
    st.dataframe(filtered[show_cols], use_container_width=True)
    csv_data = filtered[show_cols].to_csv(index=False).encode('utf-8-sig')
    st.download_button("💾 下载当前筛选数据为 CSV", csv_data,
                       f"leaf_trait_{pm_label}_{trait_col}.csv", "text/csv")
