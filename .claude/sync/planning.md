# 项目总体规划

## 当前阶段

**v4 全国三大气候区升级** — 从长江流域亚热带 → 全国尺度（北方/南方/西北）

## 进度

| 阶段 | 状态 | 说明 |
|------|:--:|------|
| P0 删除域外数据 | ✅ | 24条郑州/洛阳/深圳/福州 |
| P1 返工5篇论文 | ✅ | 恢复遗漏物种，239→279条，+26新物种 |
| P2 大规模搜索新城市 | ✅ | 18城市宽搜完成，11城确认无数据 |
| P3 叶片因子回补 | ✅ | 98属FRPS数据库，覆盖率99.4%(1077/1083) |
| P4 功能区命名统一 | ✅ | 38→9类标准类别 |
| P5 5城CNKI补充搜索 | ✅ | 5篇345条已录入 |
| P6 综合数据质量检查 | ✅ | 3维QC+126条列偏移修复 |
| v3 阶段汇总 | ✅ | 1104条, 19城市, ~169物种, 55篇论文 |
| v4 文献预筛 | ✅ | 3批1162篇CNKI搜索+AI筛选完成 |
| v4 第一批下载 | ✅ | CDP直连30篇PDF成功，26篇CAPTCHA拦截待重试 |
| v4 第一批提取 | ✅ | 3并行agent 302条（北方236/南方41/西北25） |
| v4 第一批入库 | ✅ | 合并去重→dataset.csv 1104→1406条 |
| v4 第二批下载 | 🔄 | 28篇CAPTCHA重试仍拦截（需手动滑块或隔天冷却） |
| v4 vision提取 | 🔄 | 7张表格图片vision提取中（王会霞2013×4/李晨2013×3） |
| v3 climate_zone回填 | ✅ | 1104条全部标注（南方1137/北方244/西北25），总1406条全覆盖 |
| v4 图片分类 | ✅ | 104张VLM分类完成（表格7/文字49/柱状图11/不清晰34/SEM2/流程1） |
| qa_system 专家库 | ⏳ | 已建7文件基础框架，aliases待扩充 |

## 关键文件

- 核心数据集: `C:\Users\政委\Desktop\2026\plant_dust_v2\dataset.csv` (1104条)
- **v4下载脚本**: `.claude/cnki_downloader.py` (v2, 360行，CDP WebSocket + requests，详情页方案)
  - 通过 magic bytes 检测真实格式（不依赖 Content-Type）
  - 搜索: `Page.navigate` URL导航到 `kns8s/defaultresult/index?kw=标题`
  - 下载: 进详情页 → 提取 `#pdfDown` → Cookie同步 → requests静默下载
  - 输入: 含有 title/author/year 列的 CSV
  - ⚠️ `batch_cnki_download.py`（根目录）为旧版残留，以 `.claude/cnki_downloader.py` 为准
- v4下载清单: `Desktop/2026/references/meta/v4_下载清单.csv` (50篇待下载)
- 论文预筛清单: `.claude/batch*_screened_*.csv`
- 下载目录: `~/Desktop/2026/references/downloaded/_待提取/`

## 启动流程（每次新会话）

1. Edge 以调试端口启动: `msedge.exe --remote-debugging-port=9222`
2. 在 Edge 中登录知网 `https://kns.cnki.net/`
3. 运行下载: `cd C:/Users/政委/plant_dust_analysis && python .claude/cnki_downloader.py "C:/Users/政委/Desktop/2026/references/meta/v4_下载清单.csv"`
4. 下载完成后并行 agent 提取数据

## 最近决策

2026-06-22: v2下载器改为原始CDP WebSocket + requests方案，放弃Playwright。搜索改用URL导航而非DOM填表。知网新版kns8s是SPA，无textarea，不能用表单提交方式搜索。
2026-06-22: `.claude/settings.json` 全工具白名单已配置，需从项目目录启动 Claude Code 才能加载。
2026-06-21: v3方法论→v4气候分区×异质纳入。CLAUDE.md已重写。

## 已知待解决

- v4第一批下载: 50篇（北京15篇优先），运行 `cnki_downloader.py`
- CAJ文件处理: 早期论文(2003-2010)多数仅CAJ格式，需CAJViewer或找PDF替代源
- has_data=True 仅13篇（筛得太严？），是否需要放宽重筛
- batch3 14城949篇 has_data=0，大概率筛选agent保守，需人工抽查
- qa_system/ 专家知识库待创建（物种异名映射 aliases.json 等）
