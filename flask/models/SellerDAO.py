from sqlalchemy import text
from utils.database import get_db_connection
def select_seller_data():
    try:
        with get_db_connection() as connection:
            result = connection.execute(text("SELECT company_name,salary_min, salary_max  FROM jobs"))
            return [{
                "company": row[0],
                "salary_range": f"{row[1]}k-{row[2]}k"
            } for row in result]
    except Exception as e:
        #打印异常信息
        print(f"An error occurred: {e}")
        #可以选择返回一个空列表或自定义错误信息
        return['服务器正忙，请联系管理员']