"""
零星数据提取工具 — 从论文 TXT 文本中扫描散布的数值数据。

场景：论文正文中常提及"XX最强(Y g/m²)"或"排序：A>B>C"，
      这些精确数值不在表格中但可直接利用。

用法：
    python extract_scattered_data.py              # 扫描所有 TXT，报告新数据
    python extract_scattered_data.py --json       # JSON 输出
    python extract_scattered_data.py --csv out.csv # 输出可入库 CSV
"""

import os, re, csv, json, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
TEXT_DIR = os.path.join(ROOT, 'data', 'references', 'text')
DATASET = os.path.join(ROOT, 'data', 'dataset.csv')

# === 目标物种（主名 → 别名列表）===
SPECIES = {
    '香樟': ['樟树', 'Cinnamomum camphora'],
    '桂花': ['木犀', 'Osmanthus fragrans'],
    '二球悬铃木': ['悬铃木', '法桐', '法国梧桐', 'Platanus acerifolia'],
    '广玉兰': ['荷花玉兰', 'Magnolia grandiflora'],
    '女贞': ['大叶女贞', 'Ligustrum lucidum'],
    '海桐': ['Pittosporum tobira'],
    '红叶石楠': ['Photinia fraseri', 'Photinia × fraseri'],
    '红花檵木': ['红檵木', 'Loropetalum chinense'],
    '杜鹃': ['锦绣杜鹃', 'Rhododendron simsii'],
    '八角金盘': ['Fatsia japonica'],
    '洒金桃叶珊瑚': ['桃叶珊瑚', 'Aucuba japonica'],
    '麦冬': ['沿阶草', 'Ophiopogon'],
}

# 构建搜索映射（最长优先，避免短名误匹配）
search_to_main = {}
for main, aliases in SPECIES.items():
    for a in aliases:
        search_to_main[a] = main
    search_to_main[main] = main
ALL_TERMS = sorted(search_to_main.keys(), key=len, reverse=True)

# === 正则模式 ===
NUM = r'(\d+\.?\d*)\s*(?:[±±]\s*\d+\.?\d*)?'
UNIT_UG = r'(?:μg·cm|μg/cm|µg·cm|µg/cm|μg\s*cm|µg\s*cm)'
UNIT_MG = r'(?:mg·cm|mg/cm|mg\s*cm)'
UNIT_G  = r'(?:g·m|g/m|g\s*m)'

PATTERNS = [
    # TSP 类
    (re.compile(rf'({ "|".join(map(re.escape, ALL_TERMS)) })[\s\S]{{0,200}}?{NUM}\s*({UNIT_UG}\s*[−–\-2]?\s*\d*)', re.I), 'TSP'),
    (re.compile(rf'({ "|".join(map(re.escape, ALL_TERMS)) })[\s\S]{{0,200}}?{NUM}\s*({UNIT_MG}\s*[−–\-2]?\s*\d*)', re.I), 'TSP'),
    (re.compile(rf'({ "|".join(map(re.escape, ALL_TERMS)) })[\s\S]{{0,200}}?{NUM}\s*({UNIT_G}\s*[−–\-2]?\s*\d*)', re.I), 'TSP'),
    # PM10 类
    (re.compile(rf'({ "|".join(map(re.escape, ALL_TERMS)) })[\s\S]{{0,80}}?PM10[\s\S]{{0,80}}?{NUM}\s*({UNIT_UG}|{UNIT_MG}|{UNIT_G})', re.I), 'PM10'),
    # PM2.5 类
    (re.compile(rf'({ "|".join(map(re.escape, ALL_TERMS)) })[\s\S]{{0,80}}?PM2\.?5[\s\S]{{0,80}}?{NUM}\s*({UNIT_UG}|{UNIT_MG}|{UNIT_G})', re.I), 'PM2.5'),
]


def normalize_species(term):
    for t in ALL_TERMS:
        if t in term:
            return search_to_main[t]
    return None


def convert_to_gm2(value, unit_str):
    """统一转换为 g/m²"""
    if 'μg' in unit_str or 'µg' in unit_str:
        return value / 100
    elif 'mg' in unit_str:
        return value * 10
    elif 'g' in unit_str:
        return value
    return None


def load_existing_dataset():
    """加载已有数据集，用于去重"""
    existing = set()
    try:
        with open(DATASET, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                key = (row['plant_species'], row.get('reference', '')[:40])
                existing.add(key)
                # Also add value-based keys for dedup
                try:
                    if row.get('tsp_g_m2', '').strip():
                        existing.add(('TSP', row['plant_species'], round(float(row['tsp_g_m2']), 2)))
                    if row.get('pm10_g_m2', '').strip():
                        existing.add(('PM10', row['plant_species'], round(float(row['pm10_g_m2']), 2)))
                    if row.get('pm2_5_g_m2', '').strip():
                        existing.add(('PM2.5', row['plant_species'], round(float(row['pm2_5_g_m2']), 2)))
                except (ValueError, KeyError):
                    pass
    except FileNotFoundError:
        pass
    return existing


def scan_text(text, fname, existing):
    """扫描单个文本文件，提取所有候选数据"""
    results = []
    text_flat = text.replace('\n', ' ').replace('\r', ' ')

    for pat, pm_type in PATTERNS:
        for m in pat.finditer(text_flat):
            term = m.group(1)
            value = float(m.group(2))
            unit_str = m.group(3) if m.lastindex >= 3 else ''

            norm_sp = normalize_species(term)
            if not norm_sp:
                continue

            converted = convert_to_gm2(value, unit_str)
            if converted is None or not (0.001 < converted < 100):
                continue

            # 去重：与已有数据的值相近（±5%）视为重复
            rounded = round(converted, 2)
            if (pm_type, norm_sp, rounded) in existing:
                continue
            # 宽泛去重：±10% 以内
            for existing_val in [e[2] for e in existing if e[0] == pm_type and e[1] == norm_sp]:
                if abs(rounded - existing_val) / max(existing_val, 0.001) < 0.10:
                    break
            else:
                # 获取上下文
                ctx_start = max(0, m.start() - 50)
                ctx_end = min(len(text_flat), m.end() + 100)
                ctx = text_flat[ctx_start:ctx_end].strip()

                # 过滤明显噪音
                if len(ctx.split()) < 3:
                    continue
                if 'PAGE' in ctx or '---' in ctx:
                    continue

                results.append({
                    'species': norm_sp,
                    'type': pm_type,
                    'value': round(converted, 4),
                    'raw_value': value,
                    'raw_unit': unit_str.strip(),
                    'file': fname,
                    'context': ctx[:300],
                })

    return results


def main():
    existing = load_existing_dataset()
    files = sorted([f for f in os.listdir(TEXT_DIR) if f.endswith('.txt')])

    all_results = []
    for fname in files:
        fpath = os.path.join(TEXT_DIR, fname)
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception:
            continue

        results = scan_text(text, fname, existing)
        all_results.extend(results)

    # 按文件和物种分组输出
    by_file = defaultdict(list)
    for r in all_results:
        fn = r['file'].replace('.txt', '')[:60]
        by_file[fn].append(r)

    if '--json' in sys.argv:
        print(json.dumps(all_results, ensure_ascii=False, indent=2))
        return

    if '--csv' in sys.argv:
        out_path = sys.argv[sys.argv.index('--csv') + 1]
        with open(out_path, 'w', encoding='utf-8-sig', newline='') as f:
            w = csv.DictWriter(f, fieldnames=['species','type','value','raw_unit','file','context'])
            w.writeheader()
            for r in all_results:
                w.writerow({k: r[k] for k in w.fieldnames})
        print(f"[OK] {len(all_results)} 条 → {out_path}")
        return

    # 默认：人类可读输出
    print(f"扫描 {len(files)} 个文件，发现 {len(all_results)} 条新候选数据\n")
    print("=" * 80)

    for fn, items in sorted(by_file.items()):
        # 只显示至少有目标物种数据的文件
        target_items = [i for i in items if i['species'] in SPECIES]
        if not target_items:
            continue

        print(f"\n[{fn}]")
        for r in sorted(items, key=lambda x: (x['species'], x['type'])):
            print(f"  {r['species']:8s} [{r['type']:5s}] {r['value']:.4f} g/m²  ({r['raw_value']} {r['raw_unit']})")
            ctx_clean = r['context'].replace('\n', ' ')[:200]
            print(f"    → {ctx_clean}")

    print(f"\n{'=' * 80}")
    print(f"共 {len(all_results)} 条新候选数据（已过滤与 dataset.csv 重复的值）")
    print(f"请人工核实上下文后决定是否入库。")


if __name__ == '__main__':
    main()
