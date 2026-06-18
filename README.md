# 植物叶片滞尘 (Plant Dust Retention)

**可行性验证与数据集构建** — 植物叶片滞尘能力的跨功能区、跨物种定量研究。

## 快速导航

| 文件 | 说明 |
|------|------|
| [`data/dataset.csv`](data/dataset.csv) | **核心数据** — 179条标准化滞尘记录 |
| [`data/data_sources.md`](data/data_sources.md) | 参考文献清单 |
| [`data/species_cards.md`](data/species_cards.md) | 12个物种的逐城逐功能区档案 |
| [`data/README.md`](data/README.md) | 数据集使用说明 |
| [`CLAUDE.md`](CLAUDE.md) | 项目技术文档（供 AI 辅助工具读取） |
| [`METHODOLOGY.md`](METHODOLOGY.md) | 完整方法论与经验教训 |

## 项目概况

- **核心方法论**: 物种优先 × 跨功能区对比（工业区/交通干道/公园清洁区/居住区）
- **研究区域**: 华中+华东 12 城
- **覆盖物种**: 12 种（5 乔木 + 4 灌木 + 3 地被）
- **数据记录**: 179 条

## 快速开始

```bash
git clone git@github.com:wyq135/plant-dust-retention.git
cd plant-dust-retention

# 重建数据集
python build_v2_dataset.py

# 扫描论文文本中的零星数据
python extract_scattered_data.py

# 生成可视化图表
python visualize.py

# 生成 Excel 报告
python export_excel.py
```

## 依赖

- Python 3.8+
- pandas, matplotlib, openpyxl
