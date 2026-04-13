# utils/database.py
from sqlalchemy import create_engine
from views.config import Config # 直接读取配置，避免依赖 app.py

# 独立初始化 engine
engine = create_engine(
    f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@"
    f"{Config.MYSQL_HOST}/{Config.MYSQL_DB}"
)

def get_db_connection():
    return engine.connect()