# 城市植物叶片滞尘数据集

**Plant Leaf Dust Retention — National-Scale Urban Dataset (China)**

全国尺度城市植物叶片滞尘量数据集，覆盖三大气候区（北方/南方/西北），为城市绿地规划与大气污染防治提供系统性数据基础。

- **GitHub**: https://github.com/wyq135/yangtze-plant-dust-retention
- **方法论**: 气候分区×异质纳入 — A/B/C三级数据质量透明标注

## 数据概况

| 指标 | 当前值 |
|------|:------:|
| 记录数 | **2,203** |
| 物种 | **349** 种 / **183** 属 |
| 城市 | **39** 个 |
| 论文来源 | **106** 篇 |
| 气候区 | 南方 72.7% · 北方 21.8% · 西北 5.5% |
| 数据质量 | A=635 B=1,483 C=85 |
| TSP 覆盖 | 94.1% |

## 目录结构

```
plant_dust_analysis/
├── data/dataset.csv           ← 核心数据集（快照副本）
├── tools/                     ← 可复用数据处理工具
├── qa_system/                 ← QA 查询系统（自然语言查询物种/城市/气候区）
├── docs/                      ← 方法论文档与论文素材
├── .claude/                   ← AI辅助开发配置与规划
└── CLAUDE.md                  ← 项目完整技术文档
```

> **数据源**: 主数据集位于 `Desktop/2026/plant_dust_v2/dataset.csv`，本仓库 `data/dataset.csv` 为同步快照。

## 快速开始

```bash
git clone git@github.com:wyq135/yangtze-plant-dust-retention.git
cd yangtze-plant-dust-retention

# 启动 QA 查询系统
cd qa_system && streamlit run app.py

# 生成统计报告
python tools/build_v2_dataset.py

# 论文零星数据扫描
python tools/extract_scattered_data.py
```

## 主要字段

`plant_species` | `latin_name` | `city` | `climate_zone` | `layer` | `functional_zone` | `tsp_g_m2` | `pm10_g_m2` | `pm2_5_g_m2` | `measurement_method` | `method_level` | `reference`

详见 [`CLAUDE.md`](CLAUDE.md) 和 [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md)。

## 依赖

Python 3.10+, pandas, streamlit
