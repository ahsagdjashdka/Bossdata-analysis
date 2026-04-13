from flask import Blueprint, Response
import json
from models.SellerDAO import select_seller_data

# 创建Blueprint

seller_bp = Blueprint('seller', __name__)


@seller_bp.route('/get_seller_data', methods=['GET'])
def get_seller_data_route():
    data = select_seller_data()
    response = Response(
        json.dumps(data, ensure_ascii=False),  # 确保中文字符不被转义
        mimetype='application/json;charset=utf-8'  # 设置响应的MIME类型和字符集
    )
    return response
