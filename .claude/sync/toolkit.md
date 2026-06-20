# 工具包开发 (plant_toolkit)

## 当前状态

**位置**: `C:\Users\政委\tools\plant_toolkit\`，全局安装（`.pth` 注册），任意目录可导入。

## 三个子模块

| 模块 | 能力 | 状态 |
|------|------|:--:|
| `vision` | 本地 VLM (Qwen2.5-VL-3B) 读图片表格→JSON | ✅ 可用 |
| `pdf_extractor` | PDF→文本+表格+嵌入图片 | ✅ 可用 |
| `data_merger` | CSV 合并去重+物种名/功能区名标准化 | ✅ 可用 |

## 关键函数

- `chart_to_data(image, prompt)` — 单张图片→JSON
- `pdf_images_to_data(pdf)` — PDF 完整链路（文本预判 + 批量 vision）
- `VisionModel` — 可复用模型实例
- `extract_pdf(pdf)` — PDF 全量提取
- `merge_datasets(inputs, output)` — CSV 合并去重

## 已集成到工作流

- 项目 CLAUDE.md "图片表格处理流程"已更新为 vision 优先
- 全局 CLAUDE.md 调用示例已更新
- 柱状图/折线图/饼图/散点图一律跳过，不跑 vision

## 最近更新

2026-06-19: vision.py 新增 `pdf_images_to_data()`，封装 PDF→预过滤→批量识别→汇总完整链路。
