# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv("C:/Users/政委/plant_dust_analysis/plant_dust_retention_dataset.csv")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. 各城市TSP滞尘量分布（箱线图）
ax1 = axes[0, 0]
city_order = sorted(df['city'].unique())
city_data = [df[df['city'] == c]['tsp_g_m2'].dropna().values for c in city_order]
bp = ax1.boxplot(city_data, patch_artist=True)
ax1.set_xticklabels(city_order, rotation=45)
for patch in bp['boxes']:
    patch.set_facecolor('#4CAF50')
    patch.set_alpha(0.6)
ax1.set_title('1. TSP Dust Retention by City')
ax1.set_ylabel('TSP (g/m2)')
ax1.tick_params(axis='x', rotation=45)

# 2. 土地利用类型对比
ax2 = axes[0, 1]
lu_means = df.groupby('land_use')['tsp_g_m2'].agg(['mean', 'std', 'count'])
colors = ['#2196F3', '#FF9800', '#F44336', '#9C27B0']
bars = ax2.bar(range(len(lu_means)), lu_means['mean'], yerr=lu_means['std'],
               color=colors, edgecolor='black', capsize=5)
for i, (_, row) in enumerate(lu_means.iterrows()):
    ax2.text(i, row['mean'] + 0.1, f"n={int(row['count'])}", ha='center')
ax2.set_xticks(range(len(lu_means)))
ax2.set_xticklabels(lu_means.index, rotation=20, ha='right')
ax2.set_title('2. TSP by Land Use Type')
ax2.set_ylabel('TSP (g/m2)')

# 3. 跨城市共同树种热力图
ax3 = axes[1, 0]
pivot = df.pivot_table(values='tsp_g_m2', index='plant_species',
                        columns='city', aggfunc='mean')
common = pivot.dropna(thresh=2).dropna(axis=1, thresh=1)
if not common.empty and len(common) > 1:
    im = ax3.imshow(common.values, aspect='auto', cmap='YlOrRd')
    ax3.set_xticks(range(len(common.columns)))
    ax3.set_xticklabels(common.columns, rotation=45, ha='right')
    ax3.set_yticks(range(len(common.index)))
    ax3.set_yticklabels(common.index)
    ax3.set_title('3. Cross-City Same-Species TSP (g/m2)')
    for i in range(len(common.index)):
        for j in range(len(common.columns)):
            val = common.values[i, j]
            if not np.isnan(val):
                ax3.text(j, i, f'{val:.1f}', ha='center', va='center',
                         fontsize=8, fontweight='bold')
    plt.colorbar(im, ax=ax3, shrink=0.8)
else:
    ax3.text(0.5, 0.5, 'Insufficient data', transform=ax3.transAxes, ha='center')

# 4. Top物种滞尘量排名
ax4 = axes[1, 1]
top_spp = (df.groupby('plant_species')['tsp_g_m2']
           .agg(['mean', 'count'])
           .query('count >= 2')
           .sort_values('mean', ascending=True))
colors_sp = plt.cm.viridis(np.linspace(0.2, 0.9, len(top_spp)))
ax4.barh(range(len(top_spp)), top_spp['mean'], color=colors_sp, edgecolor='black')
ax4.set_yticks(range(len(top_spp)))
ax4.set_yticklabels(top_spp.index)
ax4.set_title('4. Species Mean TSP (cross-city, n>=2)')
ax4.set_xlabel('TSP (g/m2)')

plt.tight_layout()
plt.savefig("C:/Users/政委/plant_dust_analysis/analysis_charts.png", dpi=150, bbox_inches='tight')
print("图表已保存至: analysis_charts.png")
