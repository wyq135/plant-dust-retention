"""
v4第三批合并入库脚本
- 收集6个agent输出CSV
- csv.reader验证列数
- 物种标准化(climate_zone已由agent标注)
- 去重→合并入dataset.csv
"""
import csv, os, sys
from pathlib import Path
from collections import Counter

DESKTOP = Path('C:/Users/政委/Desktop/2026')
DS_PATH = DESKTOP / 'plant_dust_v2/dataset.csv'
BATCH_DIR = DESKTOP / 'plant_dust_v2'
OUTPUT_FILES = [BATCH_DIR / f'_batch3_group{i}_output.csv' for i in range(1, 7)]

REQUIRED_FIELDS = [
    'plant_species', 'latin_name', 'layer', 'functional_zone',
    'tsp_g_m2', 'pm10_g_m2', 'pm2_5_g_m2', 'city',
    'measurement_method', 'method_level', 'original_unit', 'conversion_log',
    'reference', 'notes', 'climate_zone', 'needs_manual_review'
]

EXPECTED_HEADER = [
    'plant_species', 'latin_name', 'layer', 'functional_zone',
    'tsp_g_m2', 'pm10_g_m2', 'pm2_5_g_m2', 'city',
    'ambient_pm10_ug_m3', 'ambient_pm2_5_ug_m3', 'sampling_season',
    'days_after_rain', 'measurement_method', 'leaf_micro_features',
    'reference', 'doi', 'notes', 'method_level', 'original_unit',
    'conversion_log', 'accepted_name', 'needs_manual_review', 'climate_zone'
]

VALID_CLIMATE = {'北方', '南方', '西北'}
NORTH_CITIES = {'北京','天津','石家庄','太原','沈阳','长春','哈尔滨','唐山','保定',
                '大连','青岛','临汾','太谷','徐州','济南','郑州','洛阳'}
NW_CITIES = {'兰州','银川','西安','阿克苏','乌鲁木齐','呼和浩特','延安'}

def validate_city_climate(city, zone):
    """Check climate_zone assignment is consistent"""
    if city in NORTH_CITIES and zone != '北方':
        return f"城市{city}应为北方，实际{zone}"
    if city in NW_CITIES and zone != '西北':
        return f"城市{city}应为西北，实际{zone}"
    return None

def load_aliases():
    """Load species aliases for standardization"""
    alias_path = Path('C:/Users/政委/plant_dust_analysis/qa_system/data/aliases.json')
    if alias_path.exists():
        import json
        with open(alias_path, encoding='utf-8') as f:
            data = json.load(f)
        mapping = {}
        for name, info in data.get('species_aliases', {}).items():
            if 'standard' in info:
                mapping[name] = info['standard']
        return mapping
    return {}

def main():
    alias_map = load_aliases()
    print(f"物种别名映射: {len(alias_map)}条")

    # === Phase 1: Collect & Validate ===
    all_rows = []
    stats = {'total_files': 0, 'total_rows': 0, 'bad_rows': 0, 'column_errors': []}
    paper_counts = Counter()

    for fpath in OUTPUT_FILES:
        if not fpath.exists():
            print(f"⚠ 缺失: {fpath.name}")
            continue

        stats['total_files'] += 1
        with open(fpath, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            header = reader.fieldnames

            # Validate header
            missing_cols = set(EXPECTED_HEADER) - set(header)
            extra_cols = set(header) - set(EXPECTED_HEADER)
            if missing_cols:
                stats['column_errors'].append(f"{fpath.name}: 缺列{missing_cols}")
            if extra_cols:
                print(f"  ℹ {fpath.name}: 额外列{extra_cols}")

            for row in reader:
                # Skip empty rows
                if not row.get('plant_species', '').strip():
                    continue

                # Validate required
                for col in REQUIRED_FIELDS:
                    if col not in row:
                        row[col] = ''

                # Validate climate_zone
                zone = row.get('climate_zone', '')
                if zone not in VALID_CLIMATE:
                    city = row.get('city', '')
                    # Auto-correct
                    if city in NORTH_CITIES:
                        row['climate_zone'] = '北方'
                    elif city in NW_CITIES:
                        row['climate_zone'] = '西北'
                    else:
                        row['climate_zone'] = '南方'

                # Validate city-climate consistency
                city = row.get('city', '')
                zone = row.get('climate_zone', '')
                err = validate_city_climate(city, zone)
                if err:
                    print(f"  ⚠ {err}")

                # Standardize species name
                sp = row.get('plant_species', '').strip()
                if sp in alias_map:
                    row['plant_species'] = alias_map[sp]
                    if 'notes' not in row or not row['notes']:
                        row['notes'] = f'异名标准化: {sp}→{alias_map[sp]}'

                # Track paper
                ref = row.get('reference', '')
                if ref:
                    paper_counts[ref[:60]] += 1

                all_rows.append(row)
                stats['total_rows'] += 1

    print(f"\n=== 收集结果 ===")
    print(f"输出文件: {stats['total_files']}/6")
    print(f"总行数: {stats['total_rows']}")
    print(f"涉及论文: {len(paper_counts)}篇")

    if stats['column_errors']:
        print(f"列错误: {stats['column_errors']}")

    # === Phase 2: Dedup against existing dataset ===
    print(f"\n=== 去重 ===")
    existing_keys = set()
    with open(DS_PATH, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            key = (row.get('plant_species',''), row.get('city',''),
                   row.get('tsp_g_m2',''), row.get('reference','')[:60])
            existing_keys.add(key)

    new_rows = []
    dup_count = 0
    for row in all_rows:
        key = (row.get('plant_species',''), row.get('city',''),
               row.get('tsp_g_m2',''), row.get('reference','')[:60])
        if key in existing_keys:
            dup_count += 1
        else:
            new_rows.append(row)
            existing_keys.add(key)

    print(f"重复: {dup_count}条")
    print(f"新增: {len(new_rows)}条")

    if not new_rows:
        print("无新数据，跳过合并")
        return

    # === Phase 3: Method level stats ===
    ml = Counter(r.get('method_level', '?') for r in new_rows)
    print(f"method_level: A={ml.get('A',0)} B={ml.get('B',0)} C={ml.get('C',0)}")

    cz = Counter(r.get('climate_zone', '?') for r in new_rows)
    print(f"气候区: 北方={cz.get('北方',0)} 南方={cz.get('南方',0)} 西北={cz.get('西北',0)}")

    cities_new = set(r['city'] for r in new_rows if r.get('city'))
    print(f"城市: {len(cities_new)} → {sorted(cities_new)}")

    # === Phase 4: Merge ===
    print(f"\n=== 合并入库 ===")

    # Read existing
    with open(DS_PATH, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        existing_rows = list(reader)
        ds_header = reader.fieldnames

    # Ensure new rows have only dataset columns (drop extras like 'accepted_name')
    clean_new = []
    for row in new_rows:
        clean_row = {}
        for col in ds_header:
            clean_row[col] = row.get(col, '')
        clean_new.append(clean_row)

    # Merge
    merged = existing_rows + clean_new

    # Backup
    backup = DESKTOP / 'plant_dust_v2/dataset.csv.bak'
    import shutil
    shutil.copy2(DS_PATH, backup)
    print(f"备份: {backup}")

    # Write
    with open(DS_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=ds_header, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(merged)

    # Verify
    with open(DS_PATH, encoding='utf-8') as f:
        verify_rows = list(csv.DictReader(f))
    print(f"验证: 合并后共{len(verify_rows)}条 (原{len(existing_rows)} + 新{len(new_rows)})")

    # Species count
    species = set(r['plant_species'] for r in verify_rows if r.get('plant_species'))
    city_set = set(r['city'] for r in verify_rows if r.get('city'))
    papers = set(r['reference'][:80] for r in verify_rows if r.get('reference'))
    print(f"物种: {len(species)} | 城市: {len(city_set)} | 论文: {len(papers)}")

if __name__ == '__main__':
    main()
