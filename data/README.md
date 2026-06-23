# data/ — 数据集快照

## 文件说明

| 文件 | 说明 |
|------|------|
| `dataset.csv` | 核心数据集快照（2203条），**主副本**在 `Desktop/2026/plant_dust_v2/dataset.csv` |
| `data_sources.md` | 参考文献清单（已过时，以 CLAUDE.md 为准） |
| `species_cards.md` | 按物种整理的逐城数据档案（已过时） |

## 数据更新流程

1. 所有数据录入/修改 → `Desktop/2026/plant_dust_v2/dataset.csv`（唯一主副本）
2. 推送到 GitHub 前 → 同步快照到本目录 `data/dataset.csv`
3. **不在 `qa_system/data/` 下创建数据副本**（见 `.gitignore`）

## 字段速查

```
plant_species       — 中文种名（标准名）
latin_name          — 拉丁学名（接受名）
city                — 城市
climate_zone        — 气候区（北方/南方/西北）
layer               — 生活型（乔木/灌木/草本/地被/藤本）
functional_zone     — 功能区（9类标准化）
tsp_g_m2            — TSP滞尘量 (g/m²叶面积)
pm10_g_m2           — PM₁₀滞尘量
pm2_5_g_m2          — PM₂.₅滞尘量
measurement_method  — 测量方法描述
method_level        — A/B/C 方法学等级
leaf_shape          — 叶形（FRPS属级数据库）
leaf_surface        — 叶面质地
trichomes           — 毛被
wax_layer           — 蜡质层（论文SEM数据，仅13条）
stomata             — 气孔特征（论文SEM数据，仅15条）
reference           — 论文题录
needs_manual_review — 是否需人工复核
original_unit       — 论文原始单位
conversion_log      — 单位换算过程
```

详细方法论见 `../docs/methodology_leaf_traits.md`。
