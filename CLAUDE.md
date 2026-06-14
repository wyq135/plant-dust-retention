# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概况

植物叶片滞尘（Plant Dust Retention）可行性验证与数据集构建。当前阶段目标：证明"先定物种 → 搜集华东+华中跨功能区数据"的方法论可行，为后续论文撰写提供数据基础。

**核心方法论**: 物种优先 × 跨功能区对比（工业区/交通干道/公园清洁区/居住区），而非城市优先。

## 目录结构

```
C:\Users\政委\
├── plant_dust_analysis/           ← 脚本与源码
│   ├── build_v2_dataset.py        ← 【核心】生成 v2 数据集的 Python 脚本
│   ├── build_dataset.py           ← v1 版本（废弃，参考用）
│   ├── visualize.py               ← 可视化脚本
│   └── analysis_charts.png        ← 输出的图表
├── Desktop\2026\                  ← 【所有输出统一存放】
│   └── plant_dust_v2\
│       ├── dataset.csv            ← 70条标准化记录（核心产物）
│       ├── data_sources.md        ← 18篇参考文献清单
│       ├── species_cards.md       ← 9个物种的逐城逐功能区档案
│       └── README.md              ← 数据集使用说明
└── .claude\
    ├── CLAUDE.md                  ← 全局指令（仅含语言偏好）
    └── plans\                     ← 历史计划文件
```

## 目标物种（3乔木 + 3灌木 + 3地被）

| 层级 | 物种 | 学名 | 数据量 |
|------|------|------|:------:|
| 乔木 | 香樟 | Cinnamomum camphora | 14 |
| 乔木 | 桂花 | Osmanthus fragrans | 13 |
| 乔木 | 二球悬铃木 | Platanus acerifolia | 7 |
| 灌木 | 红花檵木 | Loropetalum chinense var. rubrum | 8 |
| 灌木 | 红叶石楠 | Photinia × fraseri | 12 |
| 灌木 | 海桐 | Pittosporum tobira | 8 |
| 地被 | 麦冬/沿阶草 | Ophiopogon japonicus/bodinieri | 3 |
| 地被 | 八角金盘 | Fatsia japonica | 2 |
| 地被 | 洒金桃叶珊瑚 | Aucuba japonica var. variegata | 3 |

**研究区域**: 杭州/扬州/南京/上海/武汉/长沙/合肥/福州/深圳（华东+华中）

## 数据格式 (dataset.csv)

| 字段 | 类型 | 说明 |
|------|------|------|
| plant_species | str | 中文种名 |
| latin_name | str | 拉丁学名 |
| layer | str | 乔木/灌木/地被 |
| functional_zone | str | 工业区/交通干道/公园清洁区/居住区/城市混合 |
| tsp_g_m2 | float | TSP滞尘量，统一为 g/m² |
| pm10_g_m2 | float | PM10滞尘量（可选） |
| pm2_5_g_m2 | float | PM2.5滞尘量（可选） |
| city | str | 研究城市 |
| ambient_pm10_ug_m3 | float | 环境PM10浓度 μg/m³ |
| ambient_pm2_5_ug_m3 | float | 环境PM2.5浓度 μg/m³ |
| days_after_rain | int | 采样距上次降雨天数 |
| reference | str | 文献引用 |
| doi | str | DOI链接 |

## 重建/更新数据集的命令

```bash
# 在 Git Bash 中运行
cd /c/Users/政委/plant_dust_analysis
python build_v2_dataset.py
```

输出自动写入 `C:/Users/政委/Desktop/2026/plant_dust_v2/dataset.csv`。

## 关键论文（跨功能区对比核心）

- **李海梅等(2021)** 林业科学研究 — 单篇覆盖5物种×3功能区（杭州），方法统一，是最核心的数据源
- **俞莉莉等(2012)** 北方园艺 — 3灌木种×4功能区（扬州）
- **肖慧玲(2013)** 华中农大硕士 — 3乔木种×3功能区（武汉），提供法桐跨环境数据
- **王琴等(2020)** 生态学报 — 最完整的 TSP/PM10/PM2.5 三分级数据（武汉）

## 已知局限（写论文时需注意）

1. 地被层仅8条记录，远少于乔木(34)和灌木(28)
2. 不同研究采样间隔（雨后天数）未完全标准化
3. 部分环境背景数据（ambient PM、温湿度）为论文原文缺失后的估计值
4. 广州/深圳缺乏乔木组数据

## 后续扩展方向

- ASReview 已安装（`pip install asreview`），可用于大规模文献筛选
- 优先寻找更多"单一论文多物种多功能区"数据源以保持方法一致性
- 地被层数据需重点补充
