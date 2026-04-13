from flask import Flask
from sqlalchemy import create_engine

app = Flask(__name__)
app.config.from_object('config.Config')

# 注册所有蓝图
from controllers.SellerController import seller_bp
from controllers.MapController import map_bp  # 新增导入

app.register_blueprint(seller_bp, url_prefix='/api')
app.register_blueprint(map_bp, url_prefix='/api')  # 新增注册

@app.route('/routes')
def list_routes():
    import urllib.parse
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.parse.unquote(f"{rule.endpoint:50s} {methods:20s} {rule}")
        output.append(line)
    return '<br>'.join(sorted(output))
