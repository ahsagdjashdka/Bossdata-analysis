# database.py
import pymysql
from pymysql.cursors import DictCursor

class DBManager:
    def __init__(self, host='localhost', user='root', password='123456',
                 database='spider_db', charset='utf8mb4'):
        """初始化数据库连接"""
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset=charset,
            cursorclass=DictCursor
        )
        self.cursor = self.connection.cursor()
        self.DB_CONFIG = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'charset': charset
        }

    def __enter__(self):
        """支持with语句"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """支持with语句"""
        self.close()

    def close(self):
        """关闭连接"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute(self, sql, args=None):
        """执行SQL语句"""
        try:
            self.cursor.execute(sql, args or ())
            self.connection.commit()
            return self.cursor
        except Exception as e:
            self.connection.rollback()
            raise e

    def fetch_one(self, sql, args=None):
        """查询单条记录"""
        self.execute(sql, args)
        return self.cursor.fetchone()

    def fetch_all(self, sql, args=None):
        """查询多条记录"""
        self.execute(sql, args)
        return self.cursor.fetchall()

    def create_table(self):
        """创建数据表"""
        sql = """
        CREATE TABLE IF NOT EXISTS jobs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100) NOT NULL COMMENT '职位名称',
            area VARCHAR(50) COMMENT '工作地点',
            salary VARCHAR(50) COMMENT '薪资范围',
            education VARCHAR(50) COMMENT '学历要求',
            experience VARCHAR(50) COMMENT '工作经验',
            company VARCHAR(100) COMMENT '公司名称',
            industry VARCHAR(100) COMMENT '行业信息',
            scale VARCHAR(50) COMMENT '公司规模',
            welfare TEXT COMMENT '公司福利',
            responsibilities TEXT COMMENT '岗位职责',
            requirements TEXT COMMENT '任职要求',
            bonuses TEXT COMMENT '加分项',
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            UNIQUE KEY idx_title_company (title, company)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='职位信息表';
        """
        self.execute(sql)
        print("数据表jobs创建成功或已存在")

    def insert_job(self, job_data):
        """插入职位数据"""
        sql = """
        INSERT INTO jobs (title, area, salary, education, experience, 
                         company, industry, scale, welfare)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            area = VALUES(area),
            salary = VALUES(salary),
            education = VALUES(education),
            experience = VALUES(experience),
            industry = VALUES(industry),
            scale = VALUES(scale),
            welfare = VALUES(welfare),
            responsibilities = VALUES(responsibilities),
            requirements = VALUES(requirements),
            bonuses = VALUES(bonuses),
            create_time = IFNULL(create_time, CURRENT_TIMESTAMP),
            update_time = CURRENT_TIMESTAMP
        """
        try:
            self.cursor.execute(sql, job_data)
            self.connection.commit()
            return self.cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            raise e


    def job_exists(self, title, company):
        """检查职位是否已存在"""
        sql = "SELECT id FROM jobs WHERE title = %s AND company = %s LIMIT 1"
        result = self.fetch_one(sql, (title, company))
        return result is not None

    def get_all_jobs(self):
        """获取所有职位"""
        sql = "SELECT * FROM jobs ORDER BY create_time DESC"
        return self.fetch_all(sql)

    def delete_job(self, job_id):
        """删除职位"""
        sql = "DELETE FROM jobs WHERE id = %s"
        self.execute(sql, (job_id,))
        return self.cursor.rowcount

    def update_job(self, job_id, update_data):
        """更新职位信息"""
        set_clause = ", ".join([f"{k} = %s" for k in update_data.keys()])
        sql = f"UPDATE jobs SET {set_clause} WHERE id = %s"
        args = list(update_data.values()) + [job_id]
        self.execute(sql, args)
        return self.cursor.rowcount