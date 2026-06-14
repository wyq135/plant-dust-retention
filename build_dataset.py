"""
植物叶片滞尘数据提取 —— 标准化数据集构建与初步分析
聚焦：乔木/行道树，单位统一为 g/m2
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pandas as pd
import numpy as np

# ============================================================
# 数据集构建：从多篇近期文献中提取的标准化数据
# 所有数值统一为 g/m2（叶面积单位）
# ============================================================

data = [
    # ===== 研究1: 武汉 (王琴等, 2020, 生态学报) =====
    # 地点: 武汉市洪山区; 土地利用: 城市混合区
    # 年均PM2.5: ~55 ug/m3; 年均PM10: ~85 ug/m3; 年均温度: 16.5°C; 年均湿度: ~75%
    # 方法: 3级滤膜过滤法(10μm/3μm/0.45μm); 采样周期: 雨后7天; 样本量: n=5
    {"plant_species": "二球悬铃木", "latin_name": "Platanus acerifolia", "life_form": "落叶乔木",
     "tsp_g_m2": 1.89, "pm10_g_m2": 0.358, "pm2_5_g_m2": 0.050,
     "city": "武汉", "land_use": "城市混合区", "ambient_pm10_μg_m3": 85, "ambient_pm2_5_μg_m3": 55,
     "temp_c": 16.5, "humidity_pct": 75, "sampling_season": "夏季", "days_after_rain": 7, "sample_count": 5,
     "measurement_method": "3级滤膜过滤法", "reference": "王琴等, 2020, 生态学报", "doi": "10.5846/stxb201808241808"},

    {"plant_species": "石楠", "latin_name": "Photinia serrulata", "life_form": "常绿乔木",
     "tsp_g_m2": 1.68, "pm10_g_m2": 0.195, "pm2_5_g_m2": 0.060,
     "city": "武汉", "land_use": "城市混合区", "ambient_pm10_μg_m3": 85, "ambient_pm2_5_μg_m3": 55,
     "temp_c": 16.5, "humidity_pct": 75, "sampling_season": "夏季", "days_after_rain": 7, "sample_count": 5,
     "measurement_method": "3级滤膜过滤法", "reference": "王琴等, 2020, 生态学报", "doi": "10.5846/stxb201808241808"},

    {"plant_species": "桂花", "latin_name": "Osmanthus fragrans", "life_form": "常绿乔木",
     "tsp_g_m2": 1.29, "pm10_g_m2": 0.195, "pm2_5_g_m2": 0.050,
     "city": "武汉", "land_use": "城市混合区", "ambient_pm10_μg_m3": 85, "ambient_pm2_5_μg_m3": 55,
     "temp_c": 16.5, "humidity_pct": 75, "sampling_season": "夏季", "days_after_rain": 7, "sample_count": 5,
     "measurement_method": "3级滤膜过滤法", "reference": "王琴等, 2020, 生态学报", "doi": "10.5846/stxb201808241808"},

    {"plant_species": "女贞", "latin_name": "Ligustrum lucidum", "life_form": "常绿乔木",
     "tsp_g_m2": 0.83, "pm10_g_m2": 0.195, "pm2_5_g_m2": 0.040,
     "city": "武汉", "land_use": "城市混合区", "ambient_pm10_μg_m3": 85, "ambient_pm2_5_μg_m3": 55,
     "temp_c": 16.5, "humidity_pct": 75, "sampling_season": "夏季", "days_after_rain": 7, "sample_count": 5,
     "measurement_method": "3级滤膜过滤法", "reference": "王琴等, 2020, 生态学报", "doi": "10.5846/stxb201808241808"},

    {"plant_species": "玉兰", "latin_name": "Magnolia denudata", "life_form": "落叶乔木",
     "tsp_g_m2": 0.81, "pm10_g_m2": 0.040, "pm2_5_g_m2": 0.010,
     "city": "武汉", "land_use": "城市混合区", "ambient_pm10_μg_m3": 85, "ambient_pm2_5_μg_m3": 55,
     "temp_c": 16.5, "humidity_pct": 75, "sampling_season": "夏季", "days_after_rain": 7, "sample_count": 5,
     "measurement_method": "3级滤膜过滤法", "reference": "王琴等, 2020, 生态学报", "doi": "10.5846/stxb201808241808"},

    {"plant_species": "银杏", "latin_name": "Ginkgo biloba", "life_form": "落叶乔木",
     "tsp_g_m2": 0.42, "pm10_g_m2": 0.040, "pm2_5_g_m2": 0.020,
     "city": "武汉", "land_use": "城市混合区", "ambient_pm10_μg_m3": 85, "ambient_pm2_5_μg_m3": 55,
     "temp_c": 16.5, "humidity_pct": 75, "sampling_season": "夏季", "days_after_rain": 7, "sample_count": 5,
     "measurement_method": "3级滤膜过滤法", "reference": "王琴等, 2020, 生态学报", "doi": "10.5846/stxb201808241808"},

    {"plant_species": "香樟", "latin_name": "Cinnamomum camphora", "life_form": "常绿乔木",
     "tsp_g_m2": 0.43, "pm10_g_m2": 0.134, "pm2_5_g_m2": 0.030,
     "city": "武汉", "land_use": "城市混合区", "ambient_pm10_μg_m3": 85, "ambient_pm2_5_μg_m3": 55,
     "temp_c": 16.5, "humidity_pct": 75, "sampling_season": "夏季", "days_after_rain": 7, "sample_count": 5,
     "measurement_method": "3级滤膜过滤法", "reference": "王琴等, 2020, 生态学报", "doi": "10.5846/stxb201808241808"},

    {"plant_species": "广玉兰", "latin_name": "Magnolia grandiflora", "life_form": "常绿乔木",
     "tsp_g_m2": 0.53, "pm10_g_m2": 0.040, "pm2_5_g_m2": 0.050,
     "city": "武汉", "land_use": "城市混合区", "ambient_pm10_μg_m3": 85, "ambient_pm2_5_μg_m3": 55,
     "temp_c": 16.5, "humidity_pct": 75, "sampling_season": "夏季", "days_after_rain": 7, "sample_count": 5,
     "measurement_method": "3级滤膜过滤法", "reference": "王琴等, 2020, 生态学报", "doi": "10.5846/stxb201808241808"},

    # ===== 研究2: 乌鲁木齐 (李耀华等, 2022, 生态学报) =====
    # 地点: 乌鲁木齐河滩快速路; 土地利用: 交通干道
    # 年均PM2.5: ~85 ug/m3; 年均PM10: ~135 ug/m3; 年均温度: 7.5°C; 年均湿度: ~55%
    # 方法: 滤膜称重法(10μm/3μm/1μm分级); 采样周期: 雨后7天; 样本量: n=3
    # 原数据单位 μg/cm2, 已转换为 g/m2 (÷100)
    {"plant_species": "榆树(圆冠榆)", "latin_name": "Ulmus densa", "life_form": "落叶乔木",
     "tsp_g_m2": 0.534, "pm10_g_m2": None, "pm2_5_g_m2": None,
     "city": "乌鲁木齐", "land_use": "交通干道", "ambient_pm10_μg_m3": 135, "ambient_pm2_5_μg_m3": 85,
     "temp_c": 7.5, "humidity_pct": 55, "sampling_season": "夏季", "days_after_rain": 7, "sample_count": 3,
     "measurement_method": "滤膜称重分级法", "reference": "李耀华等, 2022, 生态学报", "doi": "10.5846/stxb202103080635"},

    {"plant_species": "山楂", "latin_name": "Crataegus pinnatifida", "life_form": "落叶乔木",
     "tsp_g_m2": 0.355, "pm10_g_m2": None, "pm2_5_g_m2": None,
     "city": "乌鲁木齐", "land_use": "交通干道", "ambient_pm10_μg_m3": 135, "ambient_pm2_5_μg_m3": 85,
     "temp_c": 7.5, "humidity_pct": 55, "sampling_season": "夏季", "days_after_rain": 7, "sample_count": 3,
     "measurement_method": "滤膜称重分级法", "reference": "李耀华等, 2022, 生态学报", "doi": "10.5846/stxb202103080635"},

    {"plant_species": "黄金树", "latin_name": "Catalpa speciosa", "life_form": "落叶乔木",
     "tsp_g_m2": 0.311, "pm10_g_m2": None, "pm2_5_g_m2": None,
     "city": "乌鲁木齐", "land_use": "交通干道", "ambient_pm10_μg_m3": 135, "ambient_pm2_5_μg_m3": 85,
     "temp_c": 7.5, "humidity_pct": 55, "sampling_season": "夏季", "days_after_rain": 7, "sample_count": 3,
     "measurement_method": "滤膜称重分级法", "reference": "李耀华等, 2022, 生态学报", "doi": "10.5846/stxb202103080635"},

    {"plant_species": "旱柳", "latin_name": "Salix matsudana", "life_form": "落叶乔木",
     "tsp_g_m2": 0.194, "pm10_g_m2": None, "pm2_5_g_m2": None,
     "city": "乌鲁木齐", "land_use": "交通干道", "ambient_pm10_μg_m3": 135, "ambient_pm2_5_μg_m3": 85,
     "temp_c": 7.5, "humidity_pct": 55, "sampling_season": "夏季", "days_after_rain": 7, "sample_count": 3,
     "measurement_method": "滤膜称重分级法", "reference": "李耀华等, 2022, 生态学报", "doi": "10.5846/stxb202103080635"},

    # ===== 研究3: 杭州 (李晓璐等, 2022, 中国城市林业) =====
    # 地点: 杭州市区; 土地利用: 城市混合区
    # 年均PM2.5: ~30 ug/m3; 年均PM10: ~60 ug/m3; 年均温度: 17.5°C; 年均湿度: ~78%
    # 方法: 滤膜称重法; 采样周期: 累积滞尘(无降雨间隔)
    # 原数据单位 μg/cm2, 已转换为 g/m2 (÷100)
    {"plant_species": "水杉", "latin_name": "Metasequoia glyptostroboides", "life_form": "落叶乔木(针叶)",
     "tsp_g_m2": 0.765, "pm10_g_m2": None, "pm2_5_g_m2": None,
     "city": "杭州", "land_use": "城市混合区", "ambient_pm10_μg_m3": 60, "ambient_pm2_5_μg_m3": 30,
     "temp_c": 17.5, "humidity_pct": 78, "sampling_season": "夏季", "days_after_rain": None, "sample_count": 3,
     "measurement_method": "滤膜称重法", "reference": "李晓璐等, 2022, 中国城市林业", "doi": None},

    {"plant_species": "杜仲", "latin_name": "Eucommia ulmoides", "life_form": "落叶乔木",
     "tsp_g_m2": 0.700, "pm10_g_m2": None, "pm2_5_g_m2": None,
     "city": "杭州", "land_use": "城市混合区", "ambient_pm10_μg_m3": 60, "ambient_pm2_5_μg_m3": 30,
     "temp_c": 17.5, "humidity_pct": 78, "sampling_season": "夏季", "days_after_rain": None, "sample_count": 3,
     "measurement_method": "滤膜称重法", "reference": "李晓璐等, 2022, 中国城市林业", "doi": None},

    {"plant_species": "二球悬铃木", "latin_name": "Platanus acerifolia", "life_form": "落叶乔木",
     "tsp_g_m2": 0.550, "pm10_g_m2": None, "pm2_5_g_m2": None,
     "city": "杭州", "land_use": "城市混合区", "ambient_pm10_μg_m3": 60, "ambient_pm2_5_μg_m3": 30,
     "temp_c": 17.5, "humidity_pct": 78, "sampling_season": "夏季", "days_after_rain": None, "sample_count": 3,
     "measurement_method": "滤膜称重法", "reference": "李晓璐等, 2022, 中国城市林业", "doi": None},

    {"plant_species": "银杏", "latin_name": "Ginkgo biloba", "life_form": "落叶乔木",
     "tsp_g_m2": 0.200, "pm10_g_m2": None, "pm2_5_g_m2": None,
     "city": "杭州", "land_use": "城市混合区", "ambient_pm10_μg_m3": 60, "ambient_pm2_5_μg_m3": 30,
     "temp_c": 17.5, "humidity_pct": 78, "sampling_season": "夏季", "days_after_rain": None, "sample_count": 3,
     "measurement_method": "滤膜称重法", "reference": "李晓璐等, 2022, 中国城市林业", "doi": None},

    {"plant_species": "玉兰", "latin_name": "Magnolia denudata", "life_form": "落叶乔木",
     "tsp_g_m2": 0.150, "pm10_g_m2": None, "pm2_5_g_m2": None,
     "city": "杭州", "land_use": "城市混合区", "ambient_pm10_μg_m3": 60, "ambient_pm2_5_μg_m3": 30,
     "temp_c": 17.5, "humidity_pct": 78, "sampling_season": "夏季", "days_after_rain": None, "sample_count": 3,
     "measurement_method": "滤膜称重法", "reference": "李晓璐等, 2022, 中国城市林业", "doi": None},

    # ===== 研究4: 兰州西固工业区 (2023, 甘肃农业大学学报) =====
    # 地点: 兰州西固工业区; 土地利用: 工业区
    # 年均PM2.5: ~45 ug/m3; 年均PM10: ~120 ug/m3; 年均温度: 10.0°C; 年均湿度: ~50%
    {"plant_species": "紫叶矮樱", "latin_name": "Prunus × cistena", "life_form": "落叶乔木",
     "tsp_g_m2": 2.92, "pm10_g_m2": None, "pm2_5_g_m2": None,
     "city": "兰州", "land_use": "工业区", "ambient_pm10_μg_m3": 120, "ambient_pm2_5_μg_m3": 45,
     "temp_c": 10.0, "humidity_pct": 50, "sampling_season": "夏季", "days_after_rain": 7, "sample_count": 5,
     "measurement_method": "滤膜称重法", "reference": "甘肃农业大学学报, 2023", "doi": "10.13432/j.cnki.jgsau.2023.04.021"},

    {"plant_species": "紫叶李", "latin_name": "Prunus cerasifera", "life_form": "落叶乔木",
     "tsp_g_m2": 2.30, "pm10_g_m2": None, "pm2_5_g_m2": None,
     "city": "兰州", "land_use": "工业区", "ambient_pm10_μg_m3": 120, "ambient_pm2_5_μg_m3": 45,
     "temp_c": 10.0, "humidity_pct": 50, "sampling_season": "夏季", "days_after_rain": 7, "sample_count": 5,
     "measurement_method": "滤膜称重法", "reference": "甘肃农业大学学报, 2023", "doi": "10.13432/j.cnki.jgsau.2023.04.021"},

    {"plant_species": "榆叶梅", "latin_name": "Amygdalus triloba", "life_form": "落叶乔木",
     "tsp_g_m2": 1.70, "pm10_g_m2": None, "pm2_5_g_m2": None,
     "city": "兰州", "land_use": "工业区", "ambient_pm10_μg_m3": 120, "ambient_pm2_5_μg_m3": 45,
     "temp_c": 10.0, "humidity_pct": 50, "sampling_season": "夏季", "days_after_rain": 7, "sample_count": 5,
     "measurement_method": "滤膜称重法", "reference": "甘肃农业大学学报, 2023", "doi": "10.13432/j.cnki.jgsau.2023.04.021"},

    {"plant_species": "银杏", "latin_name": "Ginkgo biloba", "life_form": "落叶乔木",
     "tsp_g_m2": 0.90, "pm10_g_m2": None, "pm2_5_g_m2": None,
     "city": "兰州", "land_use": "工业区", "ambient_pm10_μg_m3": 120, "ambient_pm2_5_μg_m3": 45,
     "temp_c": 10.0, "humidity_pct": 50, "sampling_season": "夏季", "days_after_rain": 7, "sample_count": 5,
     "measurement_method": "滤膜称重法", "reference": "甘肃农业大学学报, 2023", "doi": "10.13432/j.cnki.jgsau.2023.04.021"},

    # ===== 研究5: 北京 (宋英石等, 2022) =====
    # 地点: 北京市区; 土地利用: 城市混合区/交通干道
    # 年均PM2.5: ~35 ug/m3; 年均PM10: ~65 ug/m3; 年均温度: 12.5°C; 年均湿度: ~55%
    {"plant_species": "栾树", "latin_name": "Koelreuteria paniculata", "life_form": "落叶乔木",
     "tsp_g_m2": 3.71, "pm10_g_m2": None, "pm2_5_g_m2": None,
     "city": "北京", "land_use": "交通干道", "ambient_pm10_μg_m3": 65, "ambient_pm2_5_μg_m3": 35,
     "temp_c": 12.5, "humidity_pct": 55, "sampling_season": "夏季", "days_after_rain": 7, "sample_count": 5,
     "measurement_method": "滤膜称重法", "reference": "宋英石等, 2022", "doi": None},

    # ===== 研究6: 跨城市综述 (郑瑶瑶和李晓燕, 2019) =====
    # 该综述整合了多城市数据, 提供跨城市平均值
    {"plant_species": "国槐", "latin_name": "Sophora japonica", "life_form": "落叶乔木",
     "tsp_g_m2": 5.27, "pm10_g_m2": None, "pm2_5_g_m2": None,
     "city": "多城市", "land_use": "城市混合", "ambient_pm10_μg_m3": None, "ambient_pm2_5_μg_m3": None,
     "temp_c": None, "humidity_pct": None, "sampling_season": "夏季", "days_after_rain": 7, "sample_count": None,
     "measurement_method": "加权平均(多源)", "reference": "郑瑶瑶和李晓燕, 2019", "doi": None},

    {"plant_species": "毛白杨", "latin_name": "Populus tomentosa", "life_form": "落叶乔木",
     "tsp_g_m2": 4.47, "pm10_g_m2": None, "pm2_5_g_m2": None,
     "city": "多城市", "land_use": "城市混合", "ambient_pm10_μg_m3": None, "ambient_pm2_5_μg_m3": None,
     "temp_c": None, "humidity_pct": None, "sampling_season": "夏季", "days_after_rain": 7, "sample_count": None,
     "measurement_method": "加权平均(多源)", "reference": "郑瑶瑶和李晓燕, 2019", "doi": None},

    {"plant_species": "香樟", "latin_name": "Cinnamomum camphora", "life_form": "常绿乔木",
     "tsp_g_m2": 3.60, "pm10_g_m2": None, "pm2_5_g_m2": None,
     "city": "多城市", "land_use": "城市混合", "ambient_pm10_μg_m3": None, "ambient_pm2_5_μg_m3": None,
     "temp_c": None, "humidity_pct": None, "sampling_season": "夏季", "days_after_rain": 7, "sample_count": None,
     "measurement_method": "加权平均(多源)", "reference": "郑瑶瑶和李晓燕, 2019", "doi": None},

    {"plant_species": "银杏", "latin_name": "Ginkgo biloba", "life_form": "落叶乔木",
     "tsp_g_m2": 2.38, "pm10_g_m2": None, "pm2_5_g_m2": None,
     "city": "多城市", "land_use": "城市混合", "ambient_pm10_μg_m3": None, "ambient_pm2_5_μg_m3": None,
     "temp_c": None, "humidity_pct": None, "sampling_season": "夏季", "days_after_rain": 7, "sample_count": None,
     "measurement_method": "加权平均(多源)", "reference": "郑瑶瑶和李晓燕, 2019", "doi": None},

    {"plant_species": "栾树", "latin_name": "Koelreuteria paniculata", "life_form": "落叶乔木",
     "tsp_g_m2": 1.59, "pm10_g_m2": None, "pm2_5_g_m2": None,
     "city": "多城市", "land_use": "城市混合", "ambient_pm10_μg_m3": None, "ambient_pm2_5_μg_m3": None,
     "temp_c": None, "humidity_pct": None, "sampling_season": "夏季", "days_after_rain": 7, "sample_count": None,
     "measurement_method": "加权平均(多源)", "reference": "郑瑶瑶和李晓燕, 2019", "doi": None},

    # ===== 研究7: 北京 (2022第2组, 4种乔木具体数据) =====
    {"plant_species": "国槐", "latin_name": "Sophora japonica", "life_form": "落叶乔木",
     "tsp_g_m2": 3.57, "pm10_g_m2": None, "pm2_5_g_m2": None,
     "city": "北京", "land_use": "城市混合区", "ambient_pm10_μg_m3": 65, "ambient_pm2_5_μg_m3": 35,
     "temp_c": 12.5, "humidity_pct": 55, "sampling_season": "夏季", "days_after_rain": 7, "sample_count": 5,
     "measurement_method": "滤膜称重法", "reference": "宋英石等, 2022, 北京9种绿化树种", "doi": None},

    # ===== 研究8: 合肥 (中国城市森林数据) =====
    {"plant_species": "广玉兰", "latin_name": "Magnolia grandiflora", "life_form": "常绿乔木",
     "tsp_g_m2": 4.21, "pm10_g_m2": None, "pm2_5_g_m2": None,
     "city": "合肥", "land_use": "城市混合区", "ambient_pm10_μg_m3": 70, "ambient_pm2_5_μg_m3": 42,
     "temp_c": 16.0, "humidity_pct": 75, "sampling_season": "春季", "days_after_rain": 7, "sample_count": None,
     "measurement_method": "滤膜称重法", "reference": "中国城市森林(彭镇华)", "doi": None},

    {"plant_species": "女贞", "latin_name": "Ligustrum lucidum", "life_form": "常绿乔木",
     "tsp_g_m2": 3.92, "pm10_g_m2": None, "pm2_5_g_m2": None,
     "city": "合肥", "land_use": "城市混合区", "ambient_pm10_μg_m3": 70, "ambient_pm2_5_μg_m3": 42,
     "temp_c": 16.0, "humidity_pct": 75, "sampling_season": "春季", "days_after_rain": 7, "sample_count": None,
     "measurement_method": "滤膜称重法", "reference": "中国城市森林(彭镇华)", "doi": None},

    {"plant_species": "二球悬铃木", "latin_name": "Platanus acerifolia", "life_form": "落叶乔木",
     "tsp_g_m2": 1.19, "pm10_g_m2": None, "pm2_5_g_m2": None,
     "city": "合肥", "land_use": "城市混合区", "ambient_pm10_μg_m3": 70, "ambient_pm2_5_μg_m3": 42,
     "temp_c": 16.0, "humidity_pct": 75, "sampling_season": "春季", "days_after_rain": 7, "sample_count": None,
     "measurement_method": "滤膜称重法", "reference": "中国城市森林(彭镇华)", "doi": None},

    {"plant_species": "银杏", "latin_name": "Ginkgo biloba", "life_form": "落叶乔木",
     "tsp_g_m2": 1.09, "pm10_g_m2": None, "pm2_5_g_m2": None,
     "city": "合肥", "land_use": "城市混合区", "ambient_pm10_μg_m3": 70, "ambient_pm2_5_μg_m3": 42,
     "temp_c": 16.0, "humidity_pct": 75, "sampling_season": "春季", "days_after_rain": 7, "sample_count": None,
     "measurement_method": "滤膜称重法", "reference": "中国城市森林(彭镇华)", "doi": None},
]

# ============================================================
# 创建 DataFrame
# ============================================================
df = pd.DataFrame(data)

# 单位统一检查：所有滞尘量已是 g/m2
print("=" * 70)
print("植物叶片滞尘标准化数据集")
print("=" * 70)
print(f"总记录数: {len(df)}")
print(f"研究来源数: {df['reference'].nunique()}")
print(f"城市数: {df['city'].nunique()}")
print(f"树种数: {df['plant_species'].nunique()}")
print(f"土地利用类型: {df['land_use'].unique().tolist()}")

# 保存 CSV
csv_path = "C:/Users/政委/plant_dust_analysis/plant_dust_retention_dataset.csv"
df.to_csv(csv_path, index=False, encoding="utf-8-sig")
print(f"\n数据集已保存至: {csv_path}")

# ============================================================
# 初步分析
# ============================================================
print("\n" + "=" * 70)
print("初步分析")
print("=" * 70)

# 1. TSP滞尘量总体统计
tsp_valid = df[df['tsp_g_m2'].notna()]
print(f"\n--- TSP滞尘量描述统计 (n={len(tsp_valid)}) ---")
print(tsp_valid['tsp_g_m2'].describe().round(2))

# 2. 按土地利用类型分组
print("\n--- 不同土地利用类型下的TSP滞尘量 ---")
for lu in df['land_use'].unique():
    subset = df[df['land_use'] == lu]['tsp_g_m2'].dropna()
    if len(subset) > 0:
        print(f"  {lu}: 均值={subset.mean():.2f} g/m2, "
              f"范围={subset.min():.2f}-{subset.max():.2f}, "
              f"n={len(subset)}")

# 3. 按城市分组
print("\n--- 各城市TSP滞尘量 ---")
for city in sorted(df['city'].unique()):
    subset = df[df['city'] == city]['tsp_g_m2'].dropna()
    if len(subset) > 0:
        print(f"  {city}: 均值={subset.mean():.2f} g/m2, "
              f"CV={subset.std()/subset.mean():.2f}, n={len(subset)}")

# 4. 跨城市共同树种分析
print("\n--- 跨城市共同树种滞尘量对比 ---")
common_species = df['plant_species'].value_counts()
common_species = common_species[common_species > 1].index
for sp in common_species:
    subset = df[(df['plant_species'] == sp) & df['tsp_g_m2'].notna()]
    if len(subset) > 1:
        cities = subset['city'].tolist()
        values = subset['tsp_g_m2'].tolist()
        cv = subset['tsp_g_m2'].std() / subset['tsp_g_m2'].mean() if len(subset) > 1 else 0
        print(f"  {sp}: 均值={subset['tsp_g_m2'].mean():.2f}, "
              f"CV={cv:.2f}, "
              f"城市={cities}, 值={[f'{v:.2f}' for v in values]}")

# 5. 滞尘量 Top-5
print("\n--- TSP滞尘量 Top-10 (按树种-城市组合) ---")
top10 = df[df['tsp_g_m2'].notna()].nlargest(10, 'tsp_g_m2')[
    ['plant_species', 'city', 'land_use', 'tsp_g_m2']]
for _, row in top10.iterrows():
    print(f"  {row['plant_species']:12s} | {row['city']:6s} | {row['land_use']:8s} | {row['tsp_g_m2']:.2f} g/m2")

# 6. 环境因素与滞尘量相关性
print("\n--- 环境因素与滞尘量相关性 ---")
env_cols = ['ambient_pm10_μg_m3', 'ambient_pm2_5_μg_m3', 'temp_c', 'humidity_pct']
for col in env_cols:
    valid = df[[col, 'tsp_g_m2']].dropna()
    if len(valid) > 3:
        corr = valid[col].corr(valid['tsp_g_m2'])
        print(f"  {col} vs TSP: r = {corr:.3f} (n={len(valid)})")

print("\n" + "=" * 70)
print("分析完成")
print("=" * 70)
