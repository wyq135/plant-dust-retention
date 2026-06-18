#!/usr/bin/env python3
"""
编译从英文/中文 PDF 中新提取的标准化滞尘数据
输出格式与 dataset.csv 完全一致，可直接追加
"""
import csv
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(ROOT, 'data', 'new_records_latest.csv')

FIELD_NAMES = [
    "plant_species", "latin_name", "layer", "functional_zone",
    "tsp_g_m2", "pm10_g_m2", "pm2_5_g_m2", "city",
    "ambient_pm10_ug_m3", "ambient_pm2_5_ug_m3",
    "temp_c", "humidity_pct", "sampling_season",
    "days_after_rain", "sample_count", "measurement_method",
    "leaf_micro_features", "reference", "doi", "notes"
]

records = []

def add(**kw):
    """添加一条记录。未指定的可选字段默认为空字符串。"""
    rec = {f: "" for f in FIELD_NAMES}
    rec.update(kw)
    records.append(rec)


# ============================================================================
# 1. 张北京等 (2025) — 武汉 8 目标物种 × 2 功能区
#    Journal of Environmental Management 373, 124027
#    PM2.5 + PM10 数据，秋冬两季均值
#    ⚠️ 单位换算: μg/cm² ÷ 100 = g/m²（2026-06-17修正: 原÷10错误）
#    注意: 此脚本生成的数据已用 fix_ug_per_cm2_conversion.py 修复为÷100
# ============================================================================
ZONE_INSIDE = "公园清洁区"
ZONE_OUTSIDE = "交通干道"
REF_ZBJ = "Zhang B-J et al., 2025, Journal of Environmental Management"
DOI_ZBJ = "10.1016/j.jenvman.2024.124027"

# (species_cn, latin, layer, pm25_in, pm10_in, pm25_out, pm10_out, features)
zbj_species = [
    ("香樟", "Cinnamomum camphora", "乔木",
     0.306, 1.706, 0.230, 1.233,
     "叶面具浅沟槽;气孔狭长;蜡质层薄(47-57μg/cm²)"),
    ("女贞", "Ligustrum lucidum", "乔木",
     0.258, 1.139, 0.335, 1.434,
     "叶面光滑;气孔密度低;蜡质中等(69-80μg/cm²)"),
    ("广玉兰", "Magnolia grandiflora", "乔木",
     0.264, 1.511, 0.197, 1.187,
     "叶面光滑;密被锈色绒毛;蜡质少(21-35μg/cm²)"),
    ("桂花", "Osmanthus fragrans", "乔木",
     0.250, 1.420, 0.267, 1.684,
     "叶面光滑;气孔密度最高;蜡质中等(65-70μg/cm²)"),
    ("红花檵木", "Loropetalum chinense var. rubrum", "灌木",
     0.277, 1.294, 0.492, 2.021,
     "叶面粗糙;星状毛密被;沟槽宽;蜡质中高(91-121μg/cm²)"),
    ("海桐", "Pittosporum tobira", "灌木",
     0.333, 1.431, 0.354, 1.981,
     "叶面光滑微起伏;幼叶被稀疏柔毛;蜡质少(33-67μg/cm²)"),
    ("杜鹃", "Rhododendron simsii", "灌木",
     0.326, 1.469, 0.536, 2.476,
     "叶面密被糙伏毛;蜡质层最厚(185-257μg/cm²)"),
    ("麦冬", "Ophiopogon japonicus", "地被",
     0.567, 2.542, 0.485, 2.167,
     "叶面条带状沟槽;气孔区间凸起呈瘤状;蜡质中(30-68μg/cm²)"),
]

for (cn, latin, layer, pm25_in, pm10_in, pm25_out, pm10_out, features) in zbj_species:
    # 公园清洁区（inside park）
    add(plant_species=cn, latin_name=latin, layer=layer,
        functional_zone=ZONE_INSIDE,
        pm10_g_m2=round(pm10_in, 4), pm2_5_g_m2=round(pm25_in, 4),
        city="武汉",
        ambient_pm2_5_ug_m3=73.0,
        sampling_season="秋冬",
        days_after_rain=7,
        sample_count=16,
        measurement_method="滤膜称重法(分级过滤,0.2-2.5-10μm)",
        leaf_micro_features=features,
        reference=REF_ZBJ, doi=DOI_ZBJ,
        notes="武汉解放公园内外双地点,秋冬两季均值(n=16)。PM10=PM2.5+粗颗粒(2.5-10μm)。TSP未测定。")
    # 交通干道（outside park）
    add(plant_species=cn, latin_name=latin, layer=layer,
        functional_zone=ZONE_OUTSIDE,
        pm10_g_m2=round(pm10_out, 4), pm2_5_g_m2=round(pm25_out, 4),
        city="武汉",
        ambient_pm2_5_ug_m3=73.0,
        sampling_season="秋冬",
        days_after_rain=7,
        sample_count=16,
        measurement_method="滤膜称重法(分级过滤,0.2-2.5-10μm)",
        leaf_micro_features=features,
        reference=REF_ZBJ, doi=DOI_ZBJ,
        notes="武汉解放公园外道路旁,秋冬两季均值(n=16)。PM10=PM2.5+粗颗粒(2.5-10μm)。TSP未测定。")


# ============================================================================
# 2. 贺丹等 (2025) — 郑州 13 种常绿灌木, 秋季
#    浙江农林大学学报, 42(3)
#    TSP + PM>10 + PM10 + PM2.5 完整四级数据
# ============================================================================
REF_HD = "贺丹等, 2025, 浙江农林大学学报"
DOI_HD = ""

hd_species = [
    ("八角金盘", "Fatsia japonica", "地被",
     2.23, 1.13, 1.01,
     "叶面积大;叶面粗糙有凸起;气孔周围有绒毛"),
    ("洒金桃叶珊瑚", "Aucuba japonica var. variegata", "地被",
     0.81, 0.12, 0.07,
     "叶面平滑;PM>10占总TSP的86%;细颗粒滞留能力极弱"),
    ("海桐", "Pittosporum tobira", "灌木",
     1.15, 0.39, 0.28,
     "叶面较平整;少量颗粒物沉积;气孔凹陷较浅"),
]

for (cn, latin, layer, tsp, pm10, pm25, features) in hd_species:
    add(plant_species=cn, latin_name=latin, layer=layer,
        functional_zone="城市混合",
        tsp_g_m2=tsp, pm10_g_m2=pm10, pm2_5_g_m2=pm25,
        city="郑州",
        sampling_season="秋季",
        sample_count=3,
        measurement_method="分级滤膜过滤法(超声清洗,0.2-2.5-10μm)",
        leaf_micro_features=features,
        reference=REF_HD, doi=DOI_HD,
        notes="郑州建成区常见常绿灌木,秋季采样。n=3株/种。PM10和PM2.5为整套分级数据。")


# ============================================================================
# 3. 王珍珍 (硕士论文) — 南昌 8 种常绿道路绿化树种
#    南昌市道路绿地的植物配置及滞尘效应, 江西农业大学
#    TSP 数据,雨后 25d 饱和滞尘量
# ============================================================================
REF_WZZ = "王珍珍, 硕士论文, 江西农业大学"
DOI_WZZ = ""

wzz_species = [
    ("杜鹃", "Rhododendron simsii", "灌木", 3.2544,
     "叶革质,上下密被褐色糙伏毛;叶面粗糙度高"),
    ("红叶石楠", "Photinia × fraseri", "灌木", 2.5474,
     "叶革质,倒卵状,边缘锯齿;叶面光滑蜡质层明显"),
    ("红花檵木", "Loropetalum chinense var. rubrum", "灌木", 2.2862,
     "叶革质互生,两面密被星状柔毛;叶面极粗糙"),
    ("桂花", "Osmanthus fragrans", "乔木", 1.8454,
     "叶革质,椭圆状披针形;叶面光滑"),
    ("广玉兰", "Magnolia grandiflora", "乔木", 1.6011,
     "叶倒卵状长椭圆形,背被锈色绒毛;叶面有光泽"),
    ("香樟", "Cinnamomum camphora", "乔木", 1.4615,
     "叶革质,椭圆状卵形;离基三出脉;叶面光滑"),
]

for (cn, latin, layer, tsp, features) in wzz_species:
    add(plant_species=cn, latin_name=latin, layer=layer,
        functional_zone="交通干道",
        tsp_g_m2=tsp,
        city="南昌",
        sampling_season="秋季",
        days_after_rain=25,
        sample_count=2,
        measurement_method="超声波清洗+滤膜称重(0.45μm)",
        leaf_micro_features=features,
        reference=REF_WZZ, doi=DOI_WZZ,
        notes="南昌凤凰中大道分车绿带,2018年9-11月连续5次采样,取第25d最大滞尘量。TSP数据,无PM分级。")


# ============================================================================
# 写入 CSV
# ============================================================================
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

with open(OUT_PATH, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=FIELD_NAMES, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(records)

print(f"已生成 {len(records)} 条新记录 → {OUT_PATH}")
print()
for r in records:
    tsp = r['tsp_g_m2'] or '-'
    pm10 = r['pm10_g_m2'] or '-'
    pm25 = r['pm2_5_g_m2'] or '-'
    print(f"  {r['plant_species']:8s} | {r['city']:4s} | {r['functional_zone']:6s} | "
          f"TSP={tsp:>8} | PM10={pm10:>8} | PM2.5={pm25:>8} | {r['reference'][:40]}")
