"""
从 dataset.csv 实时生成统计报告。
CLAUDE.md 不应手写统计数字——需要时运行此脚本。
用法: python .claude/_gen_stats_report.py
"""
import csv
from collections import Counter
from pathlib import Path

DS_PATH = Path('C:/Users/政委/Desktop/2026/plant_dust_v2/dataset.csv')

def main():
    with open(DS_PATH, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        header = reader.fieldnames

    total = len(rows)

    # method_level
    ml = Counter(r.get('method_level', '') for r in rows)
    # climate_zone
    cz = Counter(r.get('climate_zone', '') for r in rows)
    # city
    cities = Counter(r.get('city', '') for r in rows)
    # species
    species = set(r.get('plant_species', '') for r in rows)
    # papers
    papers = set(r.get('reference', '')[:80] for r in rows if r.get('reference'))
    # nmr
    nmr = sum(1 for r in rows if r.get('needs_manual_review', '').strip().lower() == 'true')
    # leaf traits
    leaf_db = sum(1 for r in rows if r.get('leaf_db_source', '').strip())
    # TSP/PM10/PM2.5
    tsp = sum(1 for r in rows if r.get('tsp_g_m2', '').strip() and r.get('tsp_g_m2', '').strip() not in ('0', '0.0'))
    pm10 = sum(1 for r in rows if r.get('pm10_g_m2', '').strip() and r.get('pm10_g_m2', '').strip() not in ('0', '0.0'))
    pm25 = sum(1 for r in rows if r.get('pm2_5_g_m2', '').strip() and r.get('pm2_5_g_m2', '').strip() not in ('0', '0.0'))
    # layers
    layers = Counter(r.get('layer', '') for r in rows)
    # functional zones
    zones = Counter(r.get('functional_zone', '') for r in rows)

    print(f"=== 植物叶片滞尘数据集统计 (v4 全国尺度) ===")
    print(f"生成时间: 2026-06-24")
    print(f"数据文件: {DS_PATH}")
    print()
    print(f"## 总量")
    print(f"总记录: {total}")
    print(f"列数: {len(header)}")
    print(f"城市数: {len(cities)}")
    print(f"物种数: {len(species)}")
    print(f"论文数: {len(papers)}")
    print()
    print(f"## 方法学等级")
    print(f"A级(完整方法+数据): {ml.get('A', 0)}")
    print(f"B级(定量但简化): {ml.get('B', 0)}")
    print(f"C级(图表估算/可疑): {ml.get('C', 0)}")
    print(f"needs_manual_review: {nmr}")
    print()
    print(f"## 气候区分布")
    print(f"北方: {cz.get('北方', 0)}")
    print(f"南方: {cz.get('南方', 0)}")
    print(f"西北: {cz.get('西北', 0)}")
    print()
    print(f"## Top 20 城市")
    for city, count in cities.most_common(20):
        print(f"  {city}: {count}")
    print()
    print(f"## 生活型")
    for layer, count in layers.most_common():
        print(f"  {layer}: {count}")
    print()
    print(f"## 功能区 (Top 10)")
    for zone, count in zones.most_common(10):
        print(f"  {zone}: {count}")
    print()
    print(f"## 数据指标覆盖")
    print(f"TSP: {tsp} ({tsp/total*100:.1f}%)")
    print(f"PM10: {pm10} ({pm10/total*100:.1f}%)")
    print(f"PM2.5: {pm25} ({pm25/total*100:.1f}%)")
    print(f"叶片形态因子(FRPS): {leaf_db} ({leaf_db/total*100:.1f}%)")

    # nmr breakdown
    nmr_notes = Counter()
    for r in rows:
        if r.get('needs_manual_review', '').strip().lower() == 'true':
            note = r.get('notes', '')
            # Extract category from notes
            if '张翼飞' in note or 'mg/leaf' in note:
                nmr_notes['张翼飞_mg/leaf'] += 1
            elif '气溶胶' in note:
                nmr_notes['气溶胶法'] += 1
            elif '刘海荣' in note or '单位疑' in note:
                nmr_notes['刘海荣_单位疑'] += 1
            elif '图表估算' in note:
                nmr_notes['图表估算'] += 1
            elif 'OCR' in note:
                nmr_notes['OCR乱码'] += 1
            elif '闰淑君' in note:
                nmr_notes['闰淑君_排序'] += 1
            elif '陶玲' in note or '风洞' in note:
                nmr_notes['陶玲_风洞'] += 1
            elif '木尼拉' in note:
                nmr_notes['木尼拉_PM>10'] += 1
            elif '王松' in note:
                nmr_notes['王松_百分比'] += 1
            elif '王文帆' in note:
                nmr_notes['王文帆_极高值'] += 1
            elif '禹海群' in note or 'g/kg' in note:
                nmr_notes['禹海群_g/kg'] += 1
            else:
                nmr_notes['其他'] += 1

    if nmr_notes:
        print()
        print(f"## needs_manual_review 分类 ({nmr}条)")
        for cat, count in nmr_notes.most_common():
            print(f"  {cat}: {count}")


if __name__ == '__main__':
    main()
