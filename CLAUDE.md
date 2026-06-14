# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概况

植物叶片滞尘（Plant Dust Retention）可行性验证与数据集构建。当前阶段目标：证明"先定物种 → 搜集华东+华中跨功能区数据"的方法论可行，为后续论文撰写提供数据基础。

- **GitHub**: https://github.com/wyq135/plant-dust-retention
- **核心方法论**: 物种优先 × 跨功能区对比（工业区/交通干道/公园清洁区/居住区），而非城市优先。

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

## 文献元数据抓取

### 问题诊断

Claude Code 内置 WebFetch 无法访问中文学术网站，**根因是 Anthropic 服务端对 `.cn` 域名有白名单过滤**，与本地网络、VPN 无关。用户无法配置绕过。

### 三条技术路线对比

| 路线 | 工具 | 中文学术网站 | 国际期刊 | 结论 |
|------|------|:--:|:--:|------|
| 1 | Claude WebFetch | ❌ 全部被拦 | ⚠️ 部分可用 | 服务端域名白名单，不可控 |
| 2 | Firecrawl API | ❌ JS劫持 | ⚠️ 付费墙 | 浏览器渲染被挂马网站劫持 |
| 3 | **curl + Python** | ✅ 可用 | ⚠️ 付费墙 | **首选方案** |

**路线2 失败原因**：`ecologica.cn` 等中文学术网站被大面积挂马，检测到浏览器 User-Agent 后注入恶意 JS 重定向到色情广告域名。Firecrawl 使用真实浏览器渲染，JS 劫持生效。curl 不执行 JS，天然免疫。

### 中文 DOI 解析路径

```
doi.org → chndoi.org（中文 DOI 注册中心）→ link.cnki.net（知网，付费墙）
                ↓
        "多重解析地址选择页面"
        含：题名、作者、DOI
        不含：摘要、期刊名 ← 需要知网认证
```

- **chndoi.org** 是中文 DOI 注册中心，介于 doi.org 和知网之间
- 提供论文标题和完整作者列表（可修正数据集中"X等"的简写）
- 期刊名被 CNKI 出版商信息覆盖，需从其他来源补充
- 完整摘要和数值数据需通过学校图书馆/知网获取

### scrape_paper.py 使用方法

```bash
cd plant_dust_analysis

# 基本用法：通过 DOI 抓取
python scrape_paper.py "10.5846/stxb201808241808"

# 保存为 JSON
python scrape_paper.py "10.13275/j.cnki.lykxyj.2021.04.010" --json -o meta.json

# 也支持直接 URL
python scrape_paper.py "https://www.ecologica.cn/stxb/article/abstract/201808241808"
```

**技术流程**：
```
DOI/URL → curl -sL（跟随重定向，伪装 Chrome UA）
       → 自动编码检测（UTF-8 → GB18030 → GBK → GB2312）
       → 正则清洗 HTML（去标签、解实体）
       → 结构化 JSON（标题/作者/摘要/期刊/DOI/基金/卷期页）
```

**关键设计决策**：
- 编码检测按优先级依次尝试，以页面中是否出现「摘要/标题/DOI」等关键词判断解码成功
- chndoi.org 的"多重解析地址选择页面"有专用解析逻辑
- 作者提取优先用"引用本文"格式（中文姓名连续出现），而非表单标签
- 期刊名通过引用格式 `期刊名, 年份, 卷(期): 页` 正则提取

### 核实结果（9篇论文）

| 论文 | 标题 | 作者 | 摘要 | 期刊/卷期 |
|------|:--:|:--:|:--:|:--:|
| 李海梅等(2021) | ✅ | ✅ | ❌ | ❌ |
| 王琴等(2020) | ✅ | ✅ | ✅ | ✅ |
| 张俊叶等(2019) | ✅ | ✅ | ❌ | ❌ |
| 罗佳等(2019) | ✅ | ✅ | ❌ | ❌ |
| Dang et al.(2022) | ❌ | ❌ | ❌ | ❌ |
| 吴艳芳等(2017) | ✅ | ✅ | ❌ | ❌ |
| 殷卓君等(2020) | ✅ | ✅ | ❌ | ❌ |
| Wang et al.(2020) | ❌ | ❌ | ❌ | ❌ |
| 王书恒等(2021) | ✅ | ✅ | ❌ | ❌ |

- **标题/作者提取成功**: 7/9（78%）— 仅两篇国际期刊（Elsevier、波兰期刊）失败
- **完整元数据**: 1/9（11%）— 仅王琴(2020) 生态学报页面提供全部字段
- **关键发现**: 数据集引用"X等"实为多人合著（如殷卓君等含8位作者，王琴等含10位），已从 chndoi.org 补全

### 已知限制

| 限制 | 影响 | 应对 |
|------|------|------|
| chndoi.org 不含摘要/期刊名 | 多数论文缺摘要 | 期刊名从数据集已有信息补充 |
| Elsevier/ScienceDirect 付费墙 | 国际期刊无法抓取 | 接受；本项目以中文文献为主 |
| 知网付费墙 | 无法获取全文数据 | 需学校图书馆 VPN 或校外访问 |
| 中文学术网站挂马 | Firecrawl 等浏览器方案不可用 | curl 方案天然免疫 |
| GBK 编码页面 | Windows 终端可能乱码 | 输出到 UTF-8 文件后读取 |

### 相关文件

| 文件 | 用途 |
|------|------|
| `scrape_paper.py` | 通用抓取脚本（核心工具） |
| `LESSONS_LEARNED.md` | 完整技术选型报告 |
| `Desktop/2026/paper_meta/` | 各论文的结构化元数据 JSON |
| `Desktop/2026/paper_meta/__VERIFICATION_REPORT.md` | 9篇论文逐篇核实报告 |
