#!/usr/bin/env python3
"""从英文论文文本中系统提取滞尘数据，生成 dataset.csv 候选记录。"""
import os, re, json, csv

ROOT = os.path.dirname(os.path.abspath(__file__))
TEXT_DIR = os.path.join(ROOT, 'data', 'references', 'text')
OUT_CSV = os.path.join(ROOT, 'data', 'references', 'extracted_candidates.csv')
OUT_JSON = os.path.join(ROOT, 'data', 'references', 'extracted_candidates.json')

# 14 目标物种的中文名和 Latin 名映射
TARGET_SPECIES = {
    'Cinnamomum camphora': ('香樟', '乔木'),
    'Osmanthus fragrans': ('桂花', '乔木'),
    'Platanus acerifolia': ('二球悬铃木', '乔木'),
    'Platanus × acerifolia': ('二球悬铃木', '乔木'),
    'Platanus orientalis': ('二球悬铃木', '乔木'),  # 有时混用
    'Magnolia grandiflora': ('广玉兰', '乔木'),
    'Ligustrum lucidum': ('女贞', '乔木'),
    'Loropetalum chinense': ('红花檵木', '灌木'),
    'Photinia × fraseri': ('红叶石楠', '灌木'),
    'Photinia fraseri': ('红叶石楠', '灌木'),
    'Photinia serratifolia': ('红叶石楠', '灌木'),
    'Pittosporum tobira': ('海桐', '灌木'),
    'Rhododendron pulchrum': ('杜鹃', '灌木'),
    'Rhododendron simsii': ('杜鹃', '灌木'),
    'Rhododendron': ('杜鹃', '灌木'),
    'Lagerstroemia indica': ('紫薇', '灌木'),
    'Ophiopogon japonicus': ('麦冬', '地被'),
    'Ophiopogon bodinieri': ('沿阶草', '地被'),
    'Fatsia japonica': ('八角金盘', '地被'),
    'Aucuba japonica': ('洒金桃叶珊瑚', '地被'),
    'Podocarpus macrophyllus': ('罗汉松', '乔木'),  # 非目标但常出现
    'Cinnamomum japonicum': ('日本肉桂', '乔木'),  # 非目标
}

# 城市识别模式
CITY_PATTERNS = [
    (r'\b(Hangzhou|Hangzhou City)\b', '杭州'),
    (r'\b(Changsha)\b', '长沙'),
    (r'\b(Wuhan)\b', '武汉'),
    (r'\b(Nanjing|Nanjing City)\b', '南京'),
    (r'\b(Shanghai)\b', '上海'),
    (r'\b(Hefei)\b', '合肥'),
    (r'\b(Fuzhou)\b', '福州'),
    (r'\b(Shenzhen)\b', '深圳'),
    (r'\b(Guangzhou)\b', '广州'),
    (r'\b(Beijing)\b', '北京'),
    (r'\b(Kunming|Kunming City)\b', '昆明'),
    (r'\b(Zhengzhou)\b', '郑州'),
    (r'\b(Yangzhou)\b', '扬州'),
]

# 功能区识别模式
ZONE_PATTERNS = [
    (r'\b(industrial)\s*(area|zone|site|region)?\b', '工业区'),
    (r'\b(traffic|roadside|road\s*side|street)\s*(area|zone|site)?\b', '交通干道'),
    (r'\b(park|clean|control|university\s*campus|campus)\s*(area|zone|site)?\b', '公园清洁区'),
    (r'\b(residential|urban\s*residential)\s*(area|zone|site)?\b', '居住区'),
    (r'\b(urban|commercial)\s*(area|zone|site)?\b', '城市混合'),
]

# PM 数值提取模式：在物种名附近找 g/m² 数值
PM_VALUE_PATTERNS = [
    # "Total PM retention of X was Y g/m2"
    (r'(?:total\s*(?:PM|particulate\s*matter|TSP)\s*(?:retention|capacity|accumulation)\s*(?:of\s*\w+[\s\w]*?)?(?:was|is|of|:)\s*)?(\d+\.?\d*)\s*g\s*[·/]?\s*m\s*[-−]?\s*2', 'TSP'),
    # "PM2.5 ... was Y g/m2"
    (r'PM\s*2\.?\s*5\s*(?:retention|accumulation|content|capture)?\s*(?:of\s*\w+[\s\w]*?)?(?:was|is|of|:)\s*(\d+\.?\d*)\s*g\s*[·/]?\s*m\s*[-−]?\s*2', 'PM2.5'),
    # "PM10 ... was Y g/m2"
    (r'PM\s*10\s*(?:retention|accumulation|content|capture)?\s*(?:of\s*\w+[\s\w]*?)?(?:was|is|of|:)\s*(\d+\.?\d*)\s*g\s*[·/]?\s*m\s*[-−]?\s*2', 'PM10'),
    # Generic g/m2 values near species names
    (r'(\d+\.?\d*)\s*g\s*[·/]?\s*m\s*[-−]?\s*2', 'TSP'),
]

def extract_city(text):
    cities = []
    for pattern, name in CITY_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            cities.append(name)
    return list(set(cities))

def extract_zones(text):
    zones = []
    for pattern, name in ZONE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            zones.append(name)
    return list(set(zones))

def extract_days_after_rain(text):
    patterns = [
        r'(?:no\s*(?:previous\s*)?rainfall|no\s*rain)\s*(?:for|over|more\s*than)\s*(\d+)\s*days?',
        r'(\d+)\s*days?\s*(?:after|since|without)\s*(?:rain|rainfall|precipitation)',
        r'(?:sampled|collected)\s*(?:at|on)\s*(?:day|days?)\s*(\d+)\s*(?:after|since)\s*(?:rain|rainfall)',
        r'(?:rain|rainfall|precipitation)\s*(?:exceed\w*\s*)?(?:more\s*than\s*)?(\d+\.?\d*)\s*mm',
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return int(float(m.group(1))) if '.' not in m.group(1) else m.group(1)
    return None

def extract_ambient_pm(text):
    """提取环境 PM 浓度"""
    pm10 = pm25 = None
    # PM10 ambient
    m10 = re.search(r'(?:annual\s*(?:mean|average)\s*)?PM\s*10\s*(?:concentration|level)?\s*(?:was|is|of|:|=)\s*(\d+\.?\d*)\s*(?:µg|ug|μg)\s*[·/]?\s*m\s*[-−]?\s*3', text, re.I)
    if m10:
        pm10 = float(m10.group(1))
    m25 = re.search(r'(?:annual\s*(?:mean|average)\s*)?PM\s*2\.?\s*5\s*(?:concentration|level)?\s*(?:was|is|of|:|=)\s*(\d+\.?\d*)\s*(?:µg|ug|μg)\s*[·/]?\s*m\s*[-−]?\s*3', text, re.I)
    if m25:
        pm25 = float(m25.group(1))
    return pm10, pm25

def find_species_in_text(text):
    """在文本中查找目标物种，返回出现位置和物种信息"""
    found = []
    for latin, (chinese, layer) in TARGET_SPECIES.items():
        # 搜索 Latin 名（可能被换行分割）
        latin_simple = latin.replace(' × ', ' ').replace(' var. ', ' ')
        pattern = latin_simple.replace(' ', r'\s+')
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        if matches:
            found.append({
                'latin_name': latin,
                'chinese_name': chinese,
                'layer': layer,
                'matches': len(matches),
                'positions': [m.start() for m in matches],
            })
    return found

def extract_pm_values_near_species(text, species_name, window=500):
    """在物种名周围提取 PM 数值"""
    latin_simple = species_name.replace(' × ', ' ').replace(' var. ', ' ')
    results = []
    for m in re.finditer(latin_simple.replace(' ', r'\s+'), text, re.IGNORECASE):
        start = max(0, m.start() - window)
        end = min(len(text), m.end() + window)
        context = text[start:end]

        tsp_vals = re.findall(r'(\d+\.?\d*)\s*g\s*[·/]?\s*m\s*[-−]?\s*2', context)
        pm25_vals = re.findall(r'PM\s*2\.?\s*5[^\d]*?(\d+\.\d+)\s*g\s*[·/]?\s*m\s*[-−]?\s*2', context, re.I)
        pm10_vals = re.findall(r'PM\s*10[^\d]*?(\d+\.\d+)\s*g\s*[·/]?\s*m\s*[-−]?\s*2', context, re.I)

        if tsp_vals or pm25_vals or pm10_vals:
            results.append({
                'context_window': context[:300],
                'tsp_values': [float(v) for v in tsp_vals],
                'pm25_values': [float(v) for v in pm25_vals],
                'pm10_values': [float(v) for v in pm10_vals],
            })
    return results

def parse_li_2019_data():
    """Li 2019 IJERPH: 从文本提取已知的物种×功能区数据"""
    # 从 Figure 3 的均值排名（三功能区平均）
    # From text: M. grandiflora (4.20) > P. acerifolia (3.43) > C. japonicum (2.53) >
    #   L. chinense (2.46) > O. fragrans (2.25) > R. pulchrum (2.12) >
    #   E. japonica (1.90) > P. glomerata (1.83) > C. kunmingensis (1.71) >
    #   P. cerasifera (1.60) > L. lucidum (1.47) > P. majestica (1.34) > C. camphora (0.99)
    overall_means = {
        'Magnolia grandiflora': 4.20,
        'Platanus acerifolia': 3.43,
        'Cinnamomum japonicum': 2.53,
        'Loropetalum chinense': 2.46,
        'Osmanthus fragrans': 2.25,
        'Rhododendron pulchrum': 2.12,
        'Euonymus japonica': 1.90,
        'Photinia glomerata': 1.83,
        'Celtis kunmingensis': 1.71,
        'Prunus cerasifera': 1.60,
        'Ligustrum lucidum': 1.47,
        'Prunus majestica': 1.34,
        'Cinnamomum camphora': 0.99,
    }

    # 从 Figure 5 按功能区聚类（区间值）
    # Industrial: cluster1 (>5.22) = M. grandiflora, P. acerifolia
    #             cluster2 (2.31-3.65) = O. fragrans, C. japonicum, L. chinense, R. pulchrum,
    #                                      P. majestica, L. lucidum, P. cerasifera, C. kunmingensis,
    #                                      P. glomerata, E. japonica
    #             cluster3 (1.24) = C. camphora
    # Traffic:    cluster1 (2.18-4.05) = M. grandiflora, C. japonicum, L. chinense, R. pulchrum,
    #                                      O. fragrans, P. acerifolia
    #             cluster2 (1.4-1.97) = E. japonica, C. kunmingensis, P. glomerata, P. cerasifera
    #             cluster3 (0.74-1.04) = L. lucidum, P. majestica, C. camphora
    # Campus:     cluster1 (1.36-2.76) = M. grandiflora, L. chinense, C. japonicum, O. fragrans
    #             cluster2 (0.8-1.23) = P. acerifolia, E. japonica, L. lucidum, R. pulchrum, C. kunmingensis
    #             cluster3 (0.33-0.66) = P. cerasifera, P. glomerata, P. majestica, C. camphora

    zone_data = {
        '工业区': {
            'Magnolia grandiflora': (5.22, 7.80),
            'Platanus acerifolia': (5.22, 7.80),
            'Osmanthus fragrans': (2.31, 3.65),
            'Cinnamomum japonicum': (2.31, 3.65),
            'Loropetalum chinense': (2.31, 3.65),
            'Cinnamomum camphora': (1.24, 1.24),
        },
        '交通干道': {
            'Magnolia grandiflora': (2.18, 4.05),
            'Osmanthus fragrans': (2.18, 4.05),
            'Loropetalum chinense': (2.18, 4.05),
            'Platanus acerifolia': (2.18, 4.05),
            'Cinnamomum camphora': (0.74, 1.04),
        },
        '公园清洁区': {
            'Magnolia grandiflora': (1.36, 2.76),
            'Osmanthus fragrans': (1.36, 2.76),
            'Loropetalum chinense': (1.36, 2.76),
            'Platanus acerifolia': (0.80, 1.23),
            'Cinnamomum camphora': (0.33, 0.66),
        },
    }
    return overall_means, zone_data

def main():
    all_records = []
    all_findings = {}

    txt_files = sorted([f for f in os.listdir(TEXT_DIR) if f.endswith('.txt')])

    for txt_file in txt_files:
        path = os.path.join(TEXT_DIR, txt_file)
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()

        # 提取元数据
        cities = extract_city(text)
        zones = extract_zones(text)
        days_rain = extract_days_after_rain(text)
        ambient_pm10, ambient_pm25 = extract_ambient_pm(text)

        # 找目标物种
        species_found = find_species_in_text(text)

        print(f"\n{'='*70}")
        print(f"文件: {txt_file[:80]}")
        print(f"城市: {cities}")
        print(f"功能区: {zones}")
        print(f"雨后天数: {days_rain}")
        print(f"环境PM10: {ambient_pm10}, PM2.5: {ambient_pm25}")
        print(f"目标物种: {[(s['chinese_name'], s['latin_name']) for s in species_found]}")

        findings = {
            'file': txt_file,
            'cities': cities,
            'zones': zones,
            'days_after_rain': days_rain,
            'ambient_pm10': ambient_pm10,
            'ambient_pm25': ambient_pm25,
            'species': [],
        }

        # 对每个找到的目标物种，在周围提取数值
        for sp in species_found:
            pm_data = extract_pm_values_near_species(text, sp['latin_name'])
            sp_info = {
                'latin': sp['latin_name'],
                'chinese': sp['chinese_name'],
                'layer': sp['layer'],
                'occurrences': sp['matches'],
                'pm_data': pm_data,
            }
            findings['species'].append(sp_info)

            if pm_data:
                print(f"  {sp['chinese_name']} ({sp['latin_name']}):")
                for d in pm_data[:3]:
                    print(f"    TSP={d['tsp_values'][:3]}, PM10={d['pm10_values'][:3]}, PM2.5={d['pm25_values'][:3]}")

        all_findings[txt_file] = findings

    # 保存 JSON
    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(all_findings, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nJSON 已保存: {OUT_JSON}")

if __name__ == '__main__':
    main()
