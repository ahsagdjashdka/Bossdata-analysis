from flask import Blueprint, jsonify
from sqlalchemy import text
from utils.database import get_db_connection

map_bp = Blueprint('map', __name__)

# 城市坐标映射表（建议存储到数据库或JSON文件中）
CITY_COORDINATES = {
    "北京": [116.4074, 39.9042],
    "上海": [121.4737, 31.2304],
    "广州": [113.2644, 23.1291],
    "深圳": [114.0579, 22.5431],
    "杭州": [120.1551, 30.2741],
    "成都": [104.0665, 30.5728],
    "武汉": [114.3055, 30.5931],
    "重庆": [106.5516, 29.5630],
    "西安": [108.9398, 34.3416],
    "天津": [117.1902, 39.1256],
    "南京": [118.7969, 32.0603],
    "苏州": [120.6199, 31.2993],
    "青岛": [120.3826, 36.0671],
    "郑州": [113.6654, 34.7579],
    "长沙": [112.9388, 28.2282],
    "合肥": [117.2830, 31.8612],
    "济南": [117.0009, 36.6758],
    "哈尔滨": [126.6425, 45.7567],
    "沈阳": [123.4291, 41.7968],
    "大连": [121.6147, 38.9140],
    "昆明": [102.7123, 25.0406],
    "南昌": [115.8582, 28.6820],
    "福州": [119.3062, 26.0753],
    "厦门": [118.0894, 24.4798],
    "石家庄": [114.5025, 38.0456],
    "太原": [112.5490, 37.8570],
    "贵阳": [106.7135, 26.5783],
    "兰州": [103.8235, 36.0580],
    "西宁": [101.7780, 36.6171],
    "乌鲁木齐": [87.6168, 43.8256],
    "拉萨": [91.1322, 29.6604],
    "海口": [110.3312, 20.0319],
    "南宁": [108.3200, 22.8240],
    "银川": [106.2782, 38.4664],
    "长春": [125.3245, 43.8868],
    "唐山": [118.1754, 39.6351],
    "温州": [120.6994, 28.0028],
    "珠海": [113.5767, 22.2707],
    "佛山": [113.1214, 23.0215],
    "东莞": [113.7518, 23.0207],
    "中山": [113.3824, 22.5229],
    "惠州": [114.4126, 23.1135],
    "江门": [113.0814, 22.5786],
    "汕头": [116.7084, 23.3710],
    "三亚": [109.5119, 18.2528],
    "临沂": [118.3564, 35.1042],
    "丹东": [124.3830, 40.1244],
    "包头": [109.8402, 40.6574],
    "丽水": [119.9226, 28.4514]
}


@map_bp.route('/getMapData')
def get_map_data():
    try:
        with get_db_connection() as connection:
            # 查询每个城市及其需求等级（假设region_month_analysis表中有region和demand_level字段）
            query = text("""
                SELECT region, demand_level 
                FROM region_month_analysis 
                WHERE region IS NOT NULL AND demand_level IS NOT NULL
            """)
            result = connection.execute(query)

            # 构建响应数据：包含城市、需求等级和坐标
            map_data = []
            for row in result:
                region = row[0]
                demand_level = row[1]
                if region in CITY_COORDINATES:
                    map_data.append({
                        "region": region,
                        "demand_level": demand_level,
                        "coordinates": CITY_COORDINATES[region]
                    })

            return jsonify({"data": map_data}), 200, {'Content-Type': 'application/json; charset=utf-8'}

    except Exception as e:
        return jsonify({"error": f"数据库查询失败: {str(e)}"}), 500