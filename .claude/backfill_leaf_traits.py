import csv, sys

# === Genus synonyms (updated classification → FRPS name used in database) ===
GENUS_SYNONYMS = {
    'Triadica': 'Sapium',  # Triadica sebifera = Sapium sebiferum (FRPS Vol.44)
}

# === Genus-level leaf trait database (from FRPS/Flora of China) ===
GENUS_TRAITS = GENUS_TRAITS = {
    'Acer': {
        'leaf_shape': '掌状5-7裂; 纸质; 裂片边缘有锯齿',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '幼叶两面被柔毛; 老叶仅下面脉腋有簇毛',
        'source': 'FRPS Vol.46',
    },
    'Agrostis': {
        'leaf_shape': '线形; 禾本科; 扁平; 叶舌膜质',
        'leaf_surface': '深绿色; 两面微粗糙',
        'trichomes': '无毛或叶面疏被微毛',
        'source': 'FRPS Vol.9(3)',
    },
    'Ailanthus': {
        'leaf_shape': '奇数羽状复叶; 小叶卵状披针形; 纸质; 全缘; 基部有1-2对腺齿',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '幼叶被柔毛; 老叶无毛或下面沿脉有毛',
        'source': 'FRPS Vol.43(3)',
    },
    'Albizia': {
        'leaf_shape': '二回偶数羽状复叶; 小叶镰刀形/长圆形; 纸质',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '小叶无毛或下面被柔毛',
        'source': 'FRPS Vol.39',
    },
    'Alocasia': {
        'leaf_shape': '心形/箭形/宽卵形; 革质; 全缘; 大型叶; 盾状着生',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色; 叶脉明显凸起',
        'trichomes': '无毛',
        'source': 'FRPS Vol.13(2)',
    },
    'Alpinia': {
        'leaf_shape': '长椭圆形/披针形; 革质; 全缘; 平行脉; 叶鞘抱茎',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色; 斑叶品种有黄白色条纹',
        'trichomes': '无毛或叶缘/叶背被毛',
        'source': 'FRPS Vol.16(2)',
    },
    'Alstonia': {
        'leaf_shape': '倒卵形/椭圆形; 革质; 全缘; 轮生',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛; 有乳汁',
        'source': 'FRPS Vol.63',
    },
    'Amygdalus': {
        'leaf_shape': '卵形/椭圆状披针形/倒卵状披针形; 纸质; 边缘有锯齿',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或下面沿脉被柔毛',
        'source': 'FRPS Vol.38',
    },
    'Arachis': {
        'leaf_shape': '偶数羽状复叶; 小叶倒卵形/椭圆形; 纸质; 全缘',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或下面疏被柔毛',
        'source': 'FRPS Vol.41',
    },
    'Armeniaca': {
        'leaf_shape': '卵形/椭圆状卵形; 纸质; 边缘有细锯齿',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或下面脉腋有簇毛',
        'source': 'FRPS Vol.38',
    },
    'Aucuba': {
        'leaf_shape': '卵形/椭圆状披针形; 革质; 边缘有锯齿',
        'leaf_surface': '上面深绿色有光泽; 洒金品种有黄斑; 下面淡绿色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.56',
    },
    'Bambusa': {
        'leaf_shape': '披针形/线状披针形; 竹亚科; 纸质; 全缘; 平行脉',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或下面基部被微毛',
        'source': 'FRPS Vol.9(1)',
    },
    'Bauhinia': {
        'leaf_shape': '卵形/近圆形; 纸质; 先端2裂(羊蹄甲特征); 掌状脉',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或下面疏被柔毛',
        'source': 'FRPS Vol.39',
    },
    'Begonia': {
        'leaf_shape': '斜卵形/心形; 肉质; 边缘有锯齿; 基部偏斜不对称',
        'leaf_surface': '上面深绿色偶有白斑; 下面常紫红色',
        'trichomes': '无毛或疏被柔毛',
        'source': 'FRPS Vol.52(1)',
    },
    'Berberis': {
        'leaf_shape': '倒卵形/椭圆形/匙形; 纸质或薄革质; 全缘或具刺齿; 叶脉网状',
        'leaf_surface': '上面深绿色; 下面淡绿色或灰白色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.29',
    },
    'Betula': {
        'leaf_shape': '卵形/三角状卵形; 纸质; 边缘有重锯齿; 羽状脉',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '幼叶两面被柔毛; 老叶仅下面沿脉有毛',
        'source': 'FRPS Vol.21',
    },
    'Bischofia': {
        'leaf_shape': '三出复叶; 小叶卵形/椭圆形; 革质; 边缘有锯齿',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.44(1)',
    },
    'Bismarckia': {
        'leaf_shape': '扇形掌状深裂; 裂片线形; 革质; 棕榈科大型叶',
        'leaf_surface': '上面银灰绿色; 下面有白粉',
        'trichomes': '无毛; 叶柄有锯齿',
        'source': 'FRPS Vol.13(1)',
    },
    'Broussonetia': {
        'leaf_shape': '卵形/宽卵形; 纸质; 边缘有锯齿或2-5裂',
        'leaf_surface': '上面粗糙; 下面密被柔毛',
        'trichomes': '两面被毛; 上面粗糙有毛',
        'source': 'FRPS Vol.23(1)',
    },
    'Buchloe': {
        'leaf_shape': '线形/狭线形; 禾本科; 扁平或内卷; 全缘',
        'leaf_surface': '灰绿色; 两面疏被柔毛',
        'trichomes': '疏被柔毛',
        'source': 'FRPS Vol.10(1)',
    },
    'Buxus': {
        'leaf_shape': '椭圆形/倒卵形/匙形; 革质; 全缘',
        'leaf_surface': '上面有光泽; 下面无光泽',
        'trichomes': '无毛; 或叶背中脉有毛',
        'source': 'FRPS Vol.45(1)',
    },
    'Camellia': {
        'leaf_shape': '椭圆形/卵形/倒卵形; 革质; 边缘有细锯齿',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛; 或下面幼时被柔毛',
        'source': 'FRPS Vol.49(3)',
    },
    'Canna': {
        'leaf_shape': '长椭圆形/卵状披针形; 革质; 全缘; 平行脉; 叶鞘抱茎',
        'leaf_surface': '上面深绿色或紫褐色; 下面淡绿色',
        'trichomes': '无毛; 有白粉',
        'source': 'FRPS Vol.16(2)',
    },
    'Cassia': {
        'leaf_shape': '偶数羽状复叶; 小叶卵形/椭圆状披针形; 纸质; 全缘',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或下面被微柔毛',
        'source': 'FRPS Vol.39',
    },
    'Casuarina': {
        'leaf_shape': '鳞片状; 退化叶轮生; 小枝绿色似松针',
        'leaf_surface': '绿色(小枝); 退化叶极小',
        'trichomes': '无毛',
        'source': 'FRPS Vol.20(1)',
    },
    'Catalpa': {
        'leaf_shape': '宽卵形/心形; 纸质; 全缘或3浅裂; 掌状5出脉',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '上面无毛; 下面沿脉被柔毛',
        'source': 'FRPS Vol.69',
    },
    'Cedrus': {
        'leaf_shape': '针形; 三棱状; 长枝散生短枝簇生',
        'leaf_surface': '深绿色; 每面有气孔线',
        'trichomes': '无毛(裸子植物)',
        'source': 'FRPS Vol.7',
    },
    'Celtis': {
        'leaf_shape': '卵形/卵状椭圆形; 纸质; 边缘有锯齿; 三出脉',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '幼叶两面被柔毛; 老叶仅下面脉上有毛',
        'source': 'FRPS Vol.22',
    },
    'Cerasus': {
        'leaf_shape': '卵形/椭圆形/倒卵形; 纸质; 边缘有锯齿',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或下面沿脉有毛',
        'source': 'FRPS Vol.38',
    },
    'Cercis': {
        'leaf_shape': '心形/近圆形; 纸质; 全缘; 掌状5出脉; 基部心形',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛或下面基部脉腋有簇毛',
        'source': 'FRPS Vol.39',
    },
    'Chaenomeles': {
        'leaf_shape': '卵形/椭圆形; 革质; 边缘有锯齿; 互生',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛或幼叶下面沿脉有毛',
        'source': 'FRPS Vol.36',
    },
    'Chimonanthus': {
        'leaf_shape': '卵形/椭圆状披针形; 纸质; 全缘',
        'leaf_surface': '上面粗糙; 下面淡绿色',
        'trichomes': '上面粗糙有沙纸感; 下面无毛',
        'source': 'FRPS Vol.30(2)',
    },
    'Chlorophytum': {
        'leaf_shape': '线形/狭线形; 基生丛生; 全缘; 平行脉',
        'leaf_surface': '深绿色; 银边品种有白色条纹',
        'trichomes': '无毛',
        'source': 'FRPS Vol.14',
    },
    'Chrysalidocarpus': {
        'leaf_shape': '羽状复叶; 小叶线形/披针形; 革质; 全缘; 棕榈科',
        'leaf_surface': '上面深绿色有光泽; 下面灰白色',
        'trichomes': '无毛; 叶鞘抱茎',
        'source': 'FRPS Vol.13(1)',
    },
    'Chukrasia': {
        'leaf_shape': '偶数或奇数羽状复叶; 小叶卵形/椭圆状披针形; 纸质; 全缘',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或下面沿脉被柔毛',
        'source': 'FRPS Vol.43(3)',
    },
    'Cinnamomum': {
        'leaf_shape': '卵状椭圆形; 离基三出脉',
        'leaf_surface': '光滑有光泽; 下面脉腋有腺窝',
        'trichomes': '无毛或幼时下面微被柔毛; 腺窝内被柔毛',
        'source': 'FRPS Vol.31',
    },
    'Citrus': {
        'leaf_shape': '卵形/椭圆形; 革质; 全缘或有锯齿; 有透明油腺点',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.43(2)',
    },
    'Clerodendrum': {
        'leaf_shape': '卵形/宽卵形; 纸质; 全缘或有锯齿; 对生',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '两面被柔毛或仅下面沿脉有毛',
        'source': 'FRPS Vol.65(1)',
    },
    'Cocos': {
        'leaf_shape': '羽状复叶; 小叶线形/狭披针形; 革质; 全缘; 棕榈科大型叶',
        'leaf_surface': '上面深绿色有光泽; 下面灰白色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.13(1)',
    },
    'Commelina': {
        'leaf_shape': '卵状披针形/披针形; 纸质; 全缘; 叶鞘抱茎',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或疏被柔毛',
        'source': 'FRPS Vol.13(3)',
    },
    'Cordyline': {
        'leaf_shape': '披针形/狭披针形; 革质; 全缘; 丛生茎端; 平行脉',
        'leaf_surface': '上面深绿色; 下面淡绿色; 紫叶品种紫红色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.14',
    },
    'Cornus': {
        'leaf_shape': '卵形/椭圆形; 纸质; 全缘; 对生; 弧形脉',
        'leaf_surface': '上面深绿色; 下面灰白色',
        'trichomes': '两面被贴伏柔毛; 下面较密',
        'source': 'FRPS Vol.56',
    },
    'Cotinus': {
        'leaf_shape': '倒卵形/近圆形; 纸质; 全缘; 单叶互生',
        'leaf_surface': '上面深绿色; 下面淡绿色; 秋季变红',
        'trichomes': '无毛或下面沿脉被柔毛',
        'source': 'FRPS Vol.45(1)',
    },
    'Crataegus': {
        'leaf_shape': '宽卵形/倒卵形; 纸质; 边缘有锯齿或羽状浅裂',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '上面无毛; 下面沿脉被柔毛或脉腋有簇毛',
        'source': 'FRPS Vol.36',
    },
    'Crinum': {
        'leaf_shape': '宽线形/带状; 肉质; 全缘; 基生丛生; 平行脉',
        'leaf_surface': '深绿色有光泽; 两面无毛',
        'trichomes': '无毛',
        'source': 'FRPS Vol.16(1)',
    },
    'Cryptomeria': {
        'leaf_shape': '钻形/线状钻形; 螺旋状排列; 常绿',
        'leaf_surface': '深绿色; 横切面菱形',
        'trichomes': '无毛',
        'source': 'FRPS Vol.7',
    },
    'Cunninghamia': {
        'leaf_shape': '线状披针形; 螺旋状排列; 常绿',
        'leaf_surface': '深绿色; 沿中脉两侧有气孔线',
        'trichomes': '无毛',
        'source': 'FRPS Vol.7',
    },
    'Cuphea': {
        'leaf_shape': '披针形/卵状披针形; 纸质; 全缘; 对生或轮生',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '两面被柔毛或腺毛',
        'source': 'FRPS Vol.52(2)',
    },
    'Cycas': {
        'leaf_shape': '羽状复叶; 小叶线形/条形; 革质; 全缘; 边缘反卷',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛或幼叶被锈色绒毛; 裸子植物',
        'source': 'FRPS Vol.7',
    },
    'Cynodon': {
        'leaf_shape': '线形; 禾本科; 互生; 叶舌短',
        'leaf_surface': '深绿色; 两面无毛',
        'trichomes': '无毛',
        'source': 'FRPS Vol.10(1)',
    },
    'Dianella': {
        'leaf_shape': '线形/剑形; 革质; 全缘; 基生丛生; 平行脉',
        'leaf_surface': '深绿色; 银边品种有白色条纹',
        'trichomes': '无毛',
        'source': 'FRPS Vol.14',
    },
    'Dianthus': {
        'leaf_shape': '线形/线状披针形; 革质; 全缘; 对生; 基部抱茎',
        'leaf_surface': '灰绿色; 两面无毛',
        'trichomes': '无毛',
        'source': 'FRPS Vol.26',
    },
    'Dichondra': {
        'leaf_shape': '肾形/圆形; 纸质; 全缘; 匍匐茎',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '两面被柔毛或下面被毛',
        'source': 'FRPS Vol.64(1)',
    },
    'Distylium': {
        'leaf_shape': '椭圆形/倒卵状椭圆形; 革质; 全缘或上部有锯齿',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛或幼叶被鳞毛后脱落',
        'source': 'FRPS Vol.35(2)',
    },
    'Dracontomelon': {
        'leaf_shape': '奇数羽状复叶; 小叶卵形/椭圆状披针形; 纸质; 全缘',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛或下面沿脉有毛',
        'source': 'FRPS Vol.45(1)',
    },
    'Duranta': {
        'leaf_shape': '卵形/椭圆形; 纸质; 全缘或上部有锯齿',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或下面沿脉有毛',
        'source': 'FRPS Vol.65(1)',
    },
    'Eichhornia': {
        'leaf_shape': '圆形/宽卵形; 肉质; 全缘; 叶柄膨大成气囊',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.13(3)',
    },
    'Elaeagnus': {
        'leaf_shape': '椭圆形/卵状椭圆形; 纸质或革质; 全缘',
        'leaf_surface': '上面深绿色; 下面密被银白色鳞片',
        'trichomes': '上面有银白色鳞片后脱落; 下面密被银白色鳞片',
        'source': 'FRPS Vol.52(2)',
    },
    'Elaeocarpus': {
        'leaf_shape': '椭圆形/倒卵状椭圆形; 纸质; 边缘有锯齿',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或下面沿脉有毛',
        'source': 'FRPS Vol.49(1)',
    },
    'Eriobotrya': {
        'leaf_shape': '倒卵形/倒卵状披针形/长椭圆形; 革质; 边缘有锯齿',
        'leaf_surface': '上面深绿色有光泽; 下面密被锈色绒毛',
        'trichomes': '叶背密被锈色绒毛',
        'source': 'FRPS Vol.36',
    },
    'Erythrina': {
        'leaf_shape': '三出复叶; 小叶卵形/菱状卵形; 纸质; 全缘',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或下面沿脉有毛',
        'source': 'FRPS Vol.41',
    },
    'Eucommia': {
        'leaf_shape': '椭圆形/卵形; 纸质; 边缘有锯齿; 单叶互生',
        'leaf_surface': '上面深绿色; 下面淡绿色; 撕开有银白色胶丝',
        'trichomes': '幼叶被柔毛; 老叶上面无毛下面沿脉有毛',
        'source': 'FRPS Vol.35(2)',
    },
    'Euonymus': {
        'leaf_shape': '卵形/椭圆形/倒卵形; 革质或纸质; 边缘有细锯齿',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.45(3)',
    },
    'Euryops': {
        'leaf_shape': '羽状深裂; 裂片线形; 革质; 互生簇生',
        'leaf_surface': '上面深绿色; 下面灰白色',
        'trichomes': '无毛或疏被柔毛',
        'source': 'FRPS Vol.76(1)',
    },
    'Fatsia': {
        'leaf_shape': '掌状7-9深裂; 革质; 大型叶(直径达30cm)',
        'leaf_surface': '深绿色有光泽; 叶面粗糙有凸起',
        'trichomes': '无毛或幼时疏被柔毛',
        'source': 'FRPS Vol.54',
    },
    'Festuca': {
        'leaf_shape': '线形/丝状; 禾本科; 内卷或扁平; 叶舌短',
        'leaf_surface': '深绿色; 上面有纵沟; 下面平滑',
        'trichomes': '无毛或疏被微毛',
        'source': 'FRPS Vol.9(2)',
    },
    'Ficus': {
        'leaf_shape': '狭椭圆形/椭圆形/卵状椭圆形; 薄革质; 全缘',
        'leaf_surface': '深绿色有光泽; 两面密生小瘤状突起; 钟乳体明显',
        'trichomes': '无毛',
        'source': 'FRPS Vol.23(1)',
    },
    'Firmiana': {
        'leaf_shape': '心形/掌状3-5裂; 纸质; 全缘',
        'leaf_surface': '上面深绿色; 下面密被星状绒毛',
        'trichomes': '叶背密被星状绒毛',
        'source': 'FRPS Vol.49(2)',
    },
    'Forsythia': {
        'leaf_shape': '卵形/椭圆状卵形; 纸质; 边缘有锯齿或全缘; 单叶对生',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或下面沿脉被柔毛',
        'source': 'FRPS Vol.61',
    },
    'Fraxinus': {
        'leaf_shape': '奇数羽状复叶; 小叶卵形/椭圆状披针形; 纸质; 边缘有锯齿',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或下面沿脉有毛',
        'source': 'FRPS Vol.61',
    },
    'Gardenia': {
        'leaf_shape': '倒卵状长椭圆形/椭圆形/倒披针形; 革质; 全缘',
        'leaf_surface': '上面亮绿色; 下面淡绿色',
        'trichomes': '无毛或仅下面脉腋有簇毛',
        'source': 'FRPS Vol.71(1)',
    },
    'Ginkgo': {
        'leaf_shape': '扇形; 二歧分叉脉; 长枝互生短枝簇生',
        'leaf_surface': '光滑; 上表皮平滑; 下表皮有突起和纹斑',
        'trichomes': '无毛',
        'source': 'FRPS Vol.7',
    },
    'Grevillea': {
        'leaf_shape': '羽状深裂(银桦)/全缘; 裂片线形; 革质',
        'leaf_surface': '上面深绿色; 下面密被银灰色绢毛',
        'trichomes': '下面密被银灰色绢毛',
        'source': 'FRPS Vol.24',
    },
    'Hemerocallis': {
        'leaf_shape': '线形/带状; 基生丛生; 全缘; 平行脉',
        'leaf_surface': '深绿色; 两面无毛',
        'trichomes': '无毛',
        'source': 'FRPS Vol.14',
    },
    'Hibiscus': {
        'leaf_shape': '卵形/宽卵形; 纸质; 3出脉; 边缘有锯齿',
        'leaf_surface': '上面绿色; 下面淡绿色',
        'trichomes': '叶背沿脉被星状毛',
        'source': 'FRPS Vol.49(2)',
    },
    'Hosta': {
        'leaf_shape': '卵形/心形/宽卵形; 纸质; 全缘; 基生丛生; 平行脉',
        'leaf_surface': '上面深绿色; 下面淡绿色; 多品种具黄白斑纹',
        'trichomes': '无毛',
        'source': 'FRPS Vol.14',
    },
    'Hydrangea': {
        'leaf_shape': '宽卵形/倒卵形; 纸质; 边缘有锯齿; 对生',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '上面疏被柔毛; 下面沿脉被柔毛',
        'source': 'FRPS Vol.35(1)',
    },
    'Hymenocallis': {
        'leaf_shape': '宽线形/带状; 革质; 全缘; 基生丛生; 平行脉',
        'leaf_surface': '深绿色有光泽; 两面无毛',
        'trichomes': '无毛',
        'source': 'FRPS Vol.16(1)',
    },
    'Hypericum': {
        'leaf_shape': '卵形/椭圆形/披针形; 纸质; 全缘; 有透明腺点',
        'leaf_surface': '上面绿色; 下面淡绿色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.50(2)',
    },
    'Ilex': {
        'leaf_shape': '椭圆形/卵状椭圆形/倒卵形; 革质; 全缘或具锯齿',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛或幼时被微柔毛',
        'source': 'FRPS Vol.45(2)',
    },
    'Iris': {
        'leaf_shape': '剑形/线形; 基生; 全缘; 平行脉',
        'leaf_surface': '深绿色; 两面无毛',
        'trichomes': '无毛',
        'source': 'FRPS Vol.16(1)',
    },
    'Ixora': {
        'leaf_shape': '椭圆形/倒卵形; 革质; 全缘; 对生或轮生',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.71(2)',
    },
    'Jacaranda': {
        'leaf_shape': '二回羽状复叶; 小叶长圆形/椭圆状披针形; 纸质; 全缘',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.69',
    },
    'Japonica': {
        'leaf_shape': '奇数羽状复叶; 小叶卵状披针形; 纸质; 全缘',
        'leaf_surface': '上面深绿色; 下面灰白色',
        'trichomes': '下面疏被贴伏柔毛',
        'source': 'FRPS Vol.40',
    },
    'Jasminum': {
        'leaf_shape': '卵形/椭圆形; 纸质或革质; 全缘',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.61',
    },
    'Juglans': {
        'leaf_shape': '奇数羽状复叶; 小叶卵形/椭圆状卵形; 纸质; 全缘或有锯齿',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '上面无毛; 下面脉腋有簇毛',
        'source': 'FRPS Vol.21',
    },
    'Juniperus': {
        'leaf_shape': '鳞形(圆柏)/刺形; 交互对生; 常绿',
        'leaf_surface': '深绿色',
        'trichomes': '无毛; 裸子植物',
        'source': 'FRPS Vol.7',
    },
    'Kerria': {
        'leaf_shape': '卵形/三角状卵形; 纸质; 边缘有重锯齿; 单叶互生',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '上面无毛; 下面沿脉疏被柔毛',
        'source': 'FRPS Vol.37',
    },
    'Khaya': {
        'leaf_shape': '偶数羽状复叶; 小叶卵形/椭圆状披针形; 革质; 全缘',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.43(3)',
    },
    'Koelreuteria': {
        'leaf_shape': '奇数羽状复叶或二回羽状复叶; 小叶卵形/椭圆状披针形; 纸质; 边缘有锯齿',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或下面沿脉有毛',
        'source': 'FRPS Vol.47(1)',
    },
    'Kolkwitzia': {
        'leaf_shape': '卵形/椭圆形; 纸质; 全缘或疏锯齿; 对生',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '两面被柔毛; 下面较密',
        'source': 'FRPS Vol.72',
    },
    'Lagerstroemia': {
        'leaf_shape': '椭圆形/倒卵形/卵形; 纸质; 全缘',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色; 叶面常有不规则凹凸',
        'trichomes': '无毛或下面沿脉被柔毛',
        'source': 'FRPS Vol.52(2)',
    },
    'Lantana': {
        'leaf_shape': '卵形/宽卵形; 纸质; 边缘有锯齿; 对生; 叶面粗糙有皱纹',
        'leaf_surface': '上面粗糙有皱纹; 下面淡绿色',
        'trichomes': '两面被糙硬毛',
        'source': 'FRPS Vol.65(1)',
    },
    'Ligustrum': {
        'leaf_shape': '卵形/椭圆形/椭圆状披针形; 革质或薄革质; 全缘',
        'leaf_surface': '上面有光泽; 下面淡绿色',
        'trichomes': '无毛或幼时被短柔毛后脱落',
        'source': 'FRPS Vol.61',
    },
    'Liquidambar': {
        'leaf_shape': '掌状3裂(枫香)/5-7裂; 纸质; 边缘有锯齿',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '幼叶两面被柔毛; 老叶无毛',
        'source': 'FRPS Vol.35(2)',
    },
    'Liriodendron': {
        'leaf_shape': '马褂形(4-6裂); 纸质; 全缘',
        'leaf_surface': '上面深绿色; 下面灰白色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.30(1)',
    },
    'Liriope': {
        'leaf_shape': '线形/狭线形; 丛生禾叶状; 全缘',
        'leaf_surface': '深绿色; 上面有沟槽',
        'trichomes': '无毛',
        'source': 'FRPS Vol.15',
    },
    'Litsea': {
        'leaf_shape': '椭圆形/倒卵状披针形; 革质或纸质; 全缘',
        'leaf_surface': '上面深绿色有光泽; 下面粉绿色或灰白色',
        'trichomes': '无毛或下面被柔毛',
        'source': 'FRPS Vol.31',
    },
    'Lonicera': {
        'leaf_shape': '卵形/椭圆形/卵状披针形; 纸质; 全缘; 对生',
        'leaf_surface': '上面深绿色; 下面淡绿色或灰白色',
        'trichomes': '两面被柔毛或仅下面被毛; 种间差异大',
        'source': 'FRPS Vol.72',
    },
    'Loropetalum': {
        'leaf_shape': '卵形/椭圆形; 革质; 全缘',
        'leaf_surface': '粗糙; 下面稍带灰白色',
        'trichomes': '密被星状毛; 上面略有粗毛',
        'source': 'FRPS Vol.35(2)',
    },
    'Magnolia': {
        'leaf_shape': '倒卵状椭圆形/椭圆形; 厚革质',
        'leaf_surface': '深绿色有光泽; 叶缘微反卷',
        'trichomes': '叶背密被锈色短绒毛(广玉兰); 或无毛(玉兰)',
        'source': 'FRPS Vol.30(1)',
    },
    'Mahonia': {
        'leaf_shape': '奇数羽状复叶; 小叶卵形/椭圆状披针形; 革质; 边缘有刺齿',
        'leaf_surface': '上面深绿色有光泽; 下面黄绿色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.29',
    },
    'Malus': {
        'leaf_shape': '卵形/椭圆形; 纸质; 边缘有细锯齿',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '幼叶两面被柔毛; 老叶无毛',
        'source': 'FRPS Vol.36',
    },
    'Metasequoia': {
        'leaf_shape': '条形; 交互对生羽状排列; 落叶性',
        'leaf_surface': '淡绿色; 中脉在上面凹下',
        'trichomes': '无毛',
        'source': 'FRPS Vol.7',
    },
    'Michelia': {
        'leaf_shape': '椭圆形/倒卵状椭圆形; 革质; 全缘',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛或下面被柔毛',
        'source': 'FRPS Vol.30(1)',
    },
    'Monstera': {
        'leaf_shape': '心形/宽卵形; 革质; 全缘->羽状深裂; 大型叶; 幼叶全缘老叶带穿孔',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.13(2)',
    },
    'Morus': {
        'leaf_shape': '卵形/宽卵形; 纸质; 边缘有粗锯齿或分裂',
        'leaf_surface': '上面粗糙; 下面沿脉有毛',
        'trichomes': '上面粗糙; 下面脉腋有簇毛',
        'source': 'FRPS Vol.23(1)',
    },
    'Mucuna': {
        'leaf_shape': '三出复叶; 小叶卵形/菱状卵形; 纸质; 全缘',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或下面被柔毛',
        'source': 'FRPS Vol.41',
    },
    'Musa': {
        'leaf_shape': '长椭圆形/长圆形; 大型叶; 全缘; 平行脉; 叶鞘抱茎成假茎',
        'leaf_surface': '上面深绿色有光泽; 下面灰白色',
        'trichomes': '无毛或下面被白粉',
        'source': 'FRPS Vol.16(2)',
    },
    'Myrica': {
        'leaf_shape': '倒卵形/倒卵状披针形; 革质; 全缘或上部有锯齿',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.21',
    },
    'Nandina': {
        'leaf_shape': '2-3回奇数羽状复叶; 小叶椭圆状披针形; 革质; 全缘',
        'leaf_surface': '上面深绿色; 下面淡绿色; 冬季常变红色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.29',
    },
    'Nerium': {
        'leaf_shape': '狭披针形/线状披针形; 革质; 全缘; 3-4叶轮生',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.63',
    },
    'Oenothera': {
        'leaf_shape': '倒披针形/椭圆形; 纸质; 边缘有锯齿或波状; 基生莲座状',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '两面被柔毛',
        'source': 'FRPS Vol.53(2)',
    },
    'Olea': {
        'leaf_shape': '椭圆形/披针形; 革质; 全缘; 对生',
        'leaf_surface': '上面深绿色有光泽; 下面密被锈色鳞片',
        'trichomes': '下面密被锈色鳞片',
        'source': 'FRPS Vol.61',
    },
    'Ophiopogon': {
        'leaf_shape': '线形/狭线形; 丛生禾叶状; 边缘具细锯齿',
        'leaf_surface': '深绿色; 上面有沟槽; 下面中脉明显隆起',
        'trichomes': '无毛',
        'source': 'FRPS Vol.15',
    },
    'Orychophragmus': {
        'leaf_shape': '卵形/椭圆形; 纸质; 边缘有锯齿或大头羽裂; 基生茎生叶异形',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或疏被柔毛',
        'source': 'FRPS Vol.33',
    },
    'Osmanthus': {
        'leaf_shape': '椭圆形/椭圆状披针形; 革质',
        'leaf_surface': '光滑有光泽; 中脉和侧脉上面凹入; 两面有小水泡状腺点',
        'trichomes': '无毛',
        'source': 'FRPS Vol.61',
    },
    'Oxalis': {
        'leaf_shape': '三出复叶; 小叶倒心形/倒卵形; 纸质; 全缘',
        'leaf_surface': '上面深绿色; 下面淡绿色; 紫叶品种叶紫红色',
        'trichomes': '无毛或疏被柔毛',
        'source': 'FRPS Vol.43(1)',
    },
    'Padus': {
        'leaf_shape': '椭圆形/倒卵形; 纸质; 边缘有细锯齿; 基部有1对腺体',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或下面沿脉有毛',
        'source': 'FRPS Vol.38',
    },
    'Parthenocissus': {
        'leaf_shape': '单叶3裂或掌状复叶; 纸质; 边缘有粗锯齿',
        'leaf_surface': '上面深绿色; 下面淡绿色; 秋季变红',
        'trichomes': '无毛或下面沿脉被柔毛',
        'source': 'FRPS Vol.48(2)',
    },
    'Paulownia': {
        'leaf_shape': '宽卵形/心形; 纸质; 全缘或3浅裂',
        'leaf_surface': '上面深绿色; 下面密被星状绒毛',
        'trichomes': '叶背密被星状绒毛',
        'source': 'FRPS Vol.67(2)',
    },
    'Philodendron': {
        'leaf_shape': '心形/箭形/羽状深裂; 革质; 全缘; 大型叶; 互生',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.13(2)',
    },
    'Phoebe': {
        'leaf_shape': '椭圆形/倒卵状椭圆形; 革质; 全缘',
        'leaf_surface': '上面深绿色有光泽; 下面密被柔毛或灰白色',
        'trichomes': '下面密被柔毛(桢楠)',
        'source': 'FRPS Vol.31',
    },
    'Phoenix': {
        'leaf_shape': '羽状复叶; 小叶线形/狭披针形; 革质; 全缘; 棕榈科',
        'leaf_surface': '上面深绿色; 下面灰白色',
        'trichomes': '无毛; 叶轴基部有刺',
        'source': 'FRPS Vol.13(1)',
    },
    'Photinia': {
        'leaf_shape': '长椭圆形/倒卵状椭圆形/长圆卵形; 革质; 具锯齿近基部全缘',
        'leaf_surface': '多数有光泽; 幼叶有毛后脱落变光滑',
        'trichomes': '无毛→仅中脉有毛→下面密被长柔毛(种间差异大)',
        'source': 'FRPS Vol.36',
    },
    'Phragmites': {
        'leaf_shape': '线形/线状披针形; 禾本科; 扁平; 全缘; 叶舌有毛',
        'leaf_surface': '深绿色; 两面平滑',
        'trichomes': '无毛; 叶舌有毛',
        'source': 'FRPS Vol.9(2)',
    },
    'Picea': {
        'leaf_shape': '针形; 四棱状或扁平; 螺旋状排列; 横切面菱形或扁平',
        'leaf_surface': '深绿色; 各面有气孔线',
        'trichomes': '无毛',
        'source': 'FRPS Vol.7',
    },
    'Pinus': {
        'leaf_shape': '针形; 2-5针一束; 横切面半圆形/三角形',
        'leaf_surface': '深绿色; 有气孔线; 边缘有细锯齿',
        'trichomes': '无毛(裸子植物)',
        'source': 'FRPS Vol.7',
    },
    'Pittosporum': {
        'leaf_shape': '倒卵形/倒卵状披针形; 革质; 全缘干后反卷',
        'leaf_surface': '深绿色发亮; 聚生枝顶呈假轮生状',
        'trichomes': '嫩时两面有柔毛，后变秃净',
        'source': 'FRPS Vol.35(2)',
    },
    'Platanus': {
        'leaf_shape': '掌状3-5裂; 宽卵形; 纸质; 边缘有粗锯齿',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '幼时两面被星状毛; 老时脱落',
        'source': 'FRPS Vol.35(2)',
    },
    'Platycladus': {
        'leaf_shape': '鳞形; 交互对生; 扁平; 常绿',
        'leaf_surface': '深绿色',
        'trichomes': '无毛; 裸子植物',
        'source': 'FRPS Vol.7',
    },
    'Pleioblastus': {
        'leaf_shape': '披针形; 竹亚科; 纸质; 全缘; 平行脉',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.9(1)',
    },
    'Poa': {
        'leaf_shape': '线形; 禾本科; 扁平或对折; 叶舌膜质',
        'leaf_surface': '深绿色; 两面平滑或微粗糙',
        'trichomes': '无毛或叶面微被毛',
        'source': 'FRPS Vol.9(2)',
    },
    'Podocarpus': {
        'leaf_shape': '椭圆形/长椭圆形/披针形; 革质; 全缘',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.7',
    },
    'Populus': {
        'leaf_shape': '卵形/三角状卵形; 纸质; 边缘有锯齿',
        'leaf_surface': '上面深绿色; 下面灰白色',
        'trichomes': '幼叶两面被绒毛或下面被绒毛; 老叶无毛',
        'source': 'FRPS Vol.20(2)',
    },
    'Prunus': {
        'leaf_shape': '卵形/椭圆状披针形; 纸质; 边缘有锯齿',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛或下面沿脉有毛',
        'source': 'FRPS Vol.38',
    },
    'Pterocarpus': {
        'leaf_shape': '奇数羽状复叶; 小叶卵形/椭圆形; 革质; 全缘',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛或下面疏被柔毛',
        'source': 'FRPS Vol.41',
    },
    'Pterocarya': {
        'leaf_shape': '奇数羽状复叶; 小叶椭圆形/卵状披针形; 纸质; 边缘有锯齿',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或下面沿脉有毛',
        'source': 'FRPS Vol.21',
    },
    'Punica': {
        'leaf_shape': '倒卵形/椭圆形; 纸质; 全缘',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.52(2)',
    },
    'Pyracantha': {
        'leaf_shape': '倒卵形/倒卵状长圆形; 革质; 边缘有钝锯齿',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛或幼时被柔毛',
        'source': 'FRPS Vol.36',
    },
    'Pyrus': {
        'leaf_shape': '卵形/椭圆状卵形; 纸质; 边缘有锯齿',
        'leaf_surface': '上面绿色; 下面淡绿色',
        'trichomes': '幼叶两面被绒毛; 老叶无毛或仅下面有毛',
        'source': 'FRPS Vol.36',
    },
    'Quercus': {
        'leaf_shape': '倒卵形/长椭圆形; 革质; 边缘有波状锯齿或羽状裂',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '幼叶两面被柔毛; 老叶无毛或下面有毛',
        'source': 'FRPS Vol.22',
    },
    'Reineckia': {
        'leaf_shape': '线形/狭披针形; 丛生; 全缘',
        'leaf_surface': '深绿色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.15',
    },
    'Rhapis': {
        'leaf_shape': '掌状深裂; 裂片线形/狭披针形; 革质; 棕榈科; 全缘',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛; 叶鞘有网状纤维',
        'source': 'FRPS Vol.13(1)',
    },
    'Rhododendron': {
        'leaf_shape': '卵形/椭圆状卵形/倒卵形/披针形; 革质; 集生枝端; 叶缘微反卷具细齿',
        'leaf_surface': '上面深绿色; 中脉上面凹陷下面凸出',
        'trichomes': '密被扁平糙伏毛(亮棕褐色); 上面疏被下面密被',
        'source': 'FRPS Vol.57(2)',
    },
    'Rhus': {
        'leaf_shape': '奇数羽状复叶; 小叶卵状披针形; 纸质; 边缘有锯齿',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '密被柔毛; 全株有乳汁',
        'source': 'FRPS Vol.45(1)',
    },
    'Robinia': {
        'leaf_shape': '奇数羽状复叶; 小叶卵形/椭圆形; 纸质; 全缘',
        'leaf_surface': '上面深绿色; 下面灰绿色',
        'trichomes': '幼叶两面被柔毛; 老叶无毛; 托叶变态为刺',
        'source': 'FRPS Vol.40',
    },
    'Rosa': {
        'leaf_shape': '奇数羽状复叶; 小叶卵形/椭圆形; 纸质; 边缘有锯齿',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或下面被柔毛; 叶轴常具皮刺',
        'source': 'FRPS Vol.37',
    },
    'Ruellia': {
        'leaf_shape': '披针形/狭披针形; 纸质; 全缘或波状; 对生',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或疏被柔毛',
        'source': 'FRPS Vol.70',
    },
    'Sabina': {
        'leaf_shape': '鳞形/刺形; 交互对生或轮生; 常绿',
        'leaf_surface': '深绿色',
        'trichomes': '无毛; 裸子植物',
        'source': 'FRPS Vol.7',
    },
    'Sagittaria': {
        'leaf_shape': '箭形/戟形; 纸质; 全缘; 挺水叶箭形浮水叶椭圆形',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.8',
    },
    'Salix': {
        'leaf_shape': '披针形/狭披针形; 纸质; 边缘有细锯齿',
        'leaf_surface': '上面绿色; 下面灰白色',
        'trichomes': '幼叶两面被绢毛; 老叶无毛',
        'source': 'FRPS Vol.20(2)',
    },
    'Sambucus': {
        'leaf_shape': '奇数羽状复叶; 小叶卵形/椭圆状披针形; 纸质; 边缘有锯齿',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或下面沿脉被柔毛',
        'source': 'FRPS Vol.72',
    },
    'Sapindus': {
        'leaf_shape': '偶数羽状复叶; 小叶卵形/椭圆状披针形; 纸质; 全缘',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛或下面沿脉有毛',
        'source': 'FRPS Vol.47(1)',
    },
    'Sapium': {
        'leaf_shape': '菱形/菱状卵形; 纸质; 全缘',
        'leaf_surface': '上面绿色; 下面淡绿色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.44(3)',
    },
    'Scirpus': {
        'leaf_shape': '线形/三棱形; 革质; 全缘; 莎草科; 基生或茎生',
        'leaf_surface': '深绿色; 两面无毛',
        'trichomes': '无毛',
        'source': 'FRPS Vol.11',
    },
    'Senna': {
        'leaf_shape': '偶数羽状复叶; 小叶卵形/椭圆状披针形; 纸质; 全缘',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或下面被微柔毛',
        'source': 'FRPS Vol.39',
    },
    'Sophora': {
        'leaf_shape': '奇数羽状复叶; 小叶卵形/卵状披针形; 纸质; 全缘',
        'leaf_surface': '上面深绿色; 下面灰白色',
        'trichomes': '下面疏被柔毛或贴伏毛',
        'source': 'FRPS Vol.40',
    },
    'Sorbaria': {
        'leaf_shape': '奇数羽状复叶; 小叶卵状披针形; 纸质; 边缘有重锯齿',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或下面沿脉被柔毛',
        'source': 'FRPS Vol.36',
    },
    'Sphagneticola': {
        'leaf_shape': '椭圆形/倒卵形; 纸质; 边缘有锯齿或浅裂; 对生',
        'leaf_surface': '上面粗糙; 下面淡绿色',
        'trichomes': '两面被贴伏糙毛',
        'source': 'FRPS Vol.75',
    },
    'Spiraea': {
        'leaf_shape': '卵形/椭圆形/菱状披针形; 纸质; 边缘有锯齿或缺刻',
        'leaf_surface': '上面深绿色; 下面淡绿色或灰白色',
        'trichomes': '无毛或下面被柔毛; 种间差异大',
        'source': 'FRPS Vol.36',
    },
    'Strelitzia': {
        'leaf_shape': '长椭圆形/卵状披针形; 革质; 全缘; 基生排成2列; 平行脉',
        'leaf_surface': '上面深绿色有光泽; 下面灰白色',
        'trichomes': '无毛; 叶柄长',
        'source': 'FRPS Vol.16(2)',
    },
    'Swida': {
        'leaf_shape': '卵形/椭圆形; 纸质; 全缘; 对生; 弧形脉',
        'leaf_surface': '上面深绿色; 下面灰白色',
        'trichomes': '两面被贴伏柔毛; 下面较密',
        'source': 'FRPS Vol.56',
    },
    'Symplocos': {
        'leaf_shape': '椭圆形/倒卵形/卵形; 革质或纸质; 全缘或有锯齿',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛或下面被柔毛',
        'source': 'FRPS Vol.60(2)',
    },
    'Syngonium': {
        'leaf_shape': '箭形/掌状分裂; 革质; 全缘; 幼叶箭形老叶鸟足状深裂',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.13(2)',
    },
    'Syringa': {
        'leaf_shape': '卵形/椭圆状卵形; 纸质; 全缘',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或下面被柔毛',
        'source': 'FRPS Vol.61',
    },
    'Syzygium': {
        'leaf_shape': '椭圆形/卵形/倒卵形; 革质; 全缘',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.53(1)',
    },
    'Taxodium': {
        'leaf_shape': '条形/线形; 螺旋状排列; 落叶性',
        'leaf_surface': '淡绿色; 中脉在上面凹下',
        'trichomes': '无毛',
        'source': 'FRPS Vol.7',
    },
    'Terminalia': {
        'leaf_shape': '倒卵形/匙形; 革质; 全缘; 互生簇生枝端',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛或幼叶被柔毛',
        'source': 'FRPS Vol.53(1)',
    },
    'Thevetia': {
        'leaf_shape': '狭披针形/线状披针形; 革质; 全缘; 互生',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.63',
    },
    'Trachelospermum': {
        'leaf_shape': '椭圆形/倒卵状椭圆形; 革质; 全缘',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛或幼时被微柔毛',
        'source': 'FRPS Vol.63',
    },
    'Trachycarpus': {
        'leaf_shape': '掌状深裂; 裂片线形; 革质; 棕榈科扇形叶',
        'leaf_surface': '上面深绿色; 下面灰白色',
        'trichomes': '无毛',
        'source': 'FRPS Vol.13(1)',
    },
    'Tradescantia': {
        'leaf_shape': '卵形/椭圆状披针形; 肉质; 全缘; 叶鞘抱茎',
        'leaf_surface': '上面深绿色或紫红色; 下面淡绿色或紫红色',
        'trichomes': '无毛或疏被柔毛',
        'source': 'FRPS Vol.13(3)',
    },
    'Trifolium': {
        'leaf_shape': '三出复叶; 小叶倒卵形/倒心形; 纸质; 边缘有细锯齿',
        'leaf_surface': '上面深绿色; 下面淡绿色; 常有V形白色斑',
        'trichomes': '无毛',
        'source': 'FRPS Vol.42(2)',
    },
    'Typha': {
        'leaf_shape': '线形/狭线形; 革质; 全缘; 基生; 平行脉; 海绵质',
        'leaf_surface': '深绿色; 两面无毛',
        'trichomes': '无毛',
        'source': 'FRPS Vol.8',
    },
    'Ulmus': {
        'leaf_shape': '卵形/椭圆状卵形/椭圆状披针形; 纸质; 边缘有重锯齿或单锯齿; 羽状脉直伸叶缘',
        'leaf_surface': '上面深绿色平滑或粗糙; 下面淡绿色',
        'trichomes': '无毛或下面脉腋有簇毛; 幼叶被柔毛后脱落',
        'source': 'FRPS Vol.22',
    },
    'Viburnum': {
        'leaf_shape': '椭圆形/倒卵形/卵形; 革质或纸质; 全缘或有锯齿',
        'leaf_surface': '上面深绿色有光泽; 下面淡绿色',
        'trichomes': '无毛或下面沿脉有星状毛',
        'source': 'FRPS Vol.72',
    },
    'Viola': {
        'leaf_shape': '心形/卵形/戟形; 纸质; 边缘有钝锯齿; 基生丛生',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '无毛或两面被柔毛',
        'source': 'FRPS Vol.51',
    },
    'Weigela': {
        'leaf_shape': '卵形/椭圆形/倒卵形; 纸质; 边缘有锯齿; 对生',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '上面疏被柔毛; 下面密被柔毛或仅沿脉有毛',
        'source': 'FRPS Vol.72',
    },
    'Wisteria': {
        'leaf_shape': '奇数羽状复叶; 小叶卵形/卵状披针形; 纸质; 全缘',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '幼叶两面被柔毛; 老叶近无毛',
        'source': 'FRPS Vol.40',
    },
    'Yulania': {
        'leaf_shape': '倒卵形/倒卵状椭圆形; 纸质; 全缘; 先端急尖',
        'leaf_surface': '上面深绿色; 下面淡绿色',
        'trichomes': '下面沿脉被柔毛或幼叶被毛',
        'source': 'FRPS Vol.30(1)',
    },
    'Zelkova': {
        'leaf_shape': '卵形/椭圆状披针形; 纸质; 边缘有整齐锯齿',
        'leaf_surface': '上面粗糙; 下面淡绿色',
        'trichomes': '上面粗糙有沙纸感; 下面沿脉被柔毛',
        'source': 'FRPS Vol.22',
    },
    'Zephyranthes': {
        'leaf_shape': '线形; 基生丛生; 全缘; 平行脉',
        'leaf_surface': '深绿色; 两面无毛',
        'trichomes': '无毛',
        'source': 'FRPS Vol.16(1)',
    },
    'Zizania': {
        'leaf_shape': '线形/线状披针形; 禾本科; 扁平; 全缘; 大型叶',
        'leaf_surface': '深绿色; 两面平滑',
        'trichomes': '无毛; 叶舌膜质',
        'source': 'FRPS Vol.9(2)',
    },
    'Zoysia': {
        'leaf_shape': '线形/狭披针形; 禾本科; 革质; 全缘',
        'leaf_surface': '深绿色; 两面无毛',
        'trichomes': '无毛',
        'source': 'FRPS Vol.10(1)',
    },
}


# Load dataset
with open('C:/Users/政委/Desktop/2026/plant_dust_v2/dataset.csv', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    cols = reader.fieldnames
    rows = list(reader)

# Ensure new columns
for nc in ['leaf_shape', 'leaf_surface', 'trichomes', 'leaf_db_source']:
    if nc not in cols:
        cols = list(cols) + [nc]

stats = {'backfilled': 0, 'already_had': 0, 'no_genus_match': 0, 'no_latin': 0}
no_match_species = set()

for r in rows:
    latin = r.get('latin_name','').strip()
    if not latin:
        stats['no_latin'] += 1
        continue

    genus = latin.split()[0] if latin.split() else ''
    genus = GENUS_SYNONYMS.get(genus, genus)  # resolve updated classification
    if not genus or genus not in GENUS_TRAITS:
        stats['no_genus_match'] += 1
        no_match_species.add(f"{r['plant_species']} ({latin})")
        continue

    trait = GENUS_TRAITS[genus]

    # Only backfill if field is empty
    if not r.get('leaf_shape','').strip():
        r['leaf_shape'] = trait.get('leaf_shape','')
    if not r.get('leaf_surface','').strip():
        r['leaf_surface'] = trait.get('leaf_surface','')
    if not r.get('trichomes','').strip():
        r['trichomes'] = trait.get('trichomes','')

    r['leaf_db_source'] = trait.get('source','')
    stats['backfilled'] += 1

# Count existing (original paper data, not DB-sourced)
for r in rows:
    has_leaf = r.get('leaf_shape','').strip() or r.get('leaf_surface','').strip() or r.get('trichomes','').strip()
    has_db = r.get('leaf_db_source','').strip()
    if has_leaf and not has_db:
        stats['already_had'] += 1

# Report
with open('C:/Users/政委/plant_dust_analysis/_backfill_report.txt', 'w', encoding='utf-8') as out:
    out.write("=== 叶片因子数据库回补报告 ===\n\n")
    out.write(f"总记录: {len(rows)}\n")
    out.write(f"属级数据库覆盖: {len(GENUS_TRAITS)} 属\n")
    out.write(f"数据库回补记录: {stats['backfilled']}\n")
    out.write(f"原始论文数据(未被覆盖): {stats['already_had']}\n")
    out.write(f"属名未匹配: {stats['no_genus_match']}\n")
    out.write(f"无拉丁名: {stats['no_latin']}\n\n")

    for nc in ['leaf_shape', 'leaf_surface', 'trichomes']:
        has = sum(1 for r in rows if r.get(nc,'').strip())
        out.write(f"{nc}: {has} ({has/len(rows)*100:.0f}%)\n")

    if no_match_species:
        out.write(f"\n未匹配属的物种 ({len(no_match_species)}):\n")
        for s in sorted(no_match_species):
            out.write(f"  {s}\n")

# Save
with open('C:/Users/政委/Desktop/2026/plant_dust_v2/dataset.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=cols)
    writer.writeheader()
    writer.writerows(rows)

print(f"Done: backfilled {stats['backfilled']}, already had {stats['already_had']}, no match {stats['no_genus_match']}, no latin {stats['no_latin']}")
