# Boss_data 爬虫模块

## 项目简介

Boss_data 是 Boss 直聘数据分析系统的爬虫模块，使用 Selenium 模拟浏览器操作，爬取 Boss 直聘网站的招聘数据，并进行数据清洗和存储。

## 目录结构

```
Boss_data/
├── BossData_all.csv     # 爬取的职位数据（CSV格式）
├── DBManager.py         # 数据库管理类
├── excel_to_sql.py      # Excel 数据导入数据库脚本
├── spider.py            # 主要爬虫脚本
├── test.py              # 测试脚本
└── test1.xls            # 爬取的职位数据（Excel格式）
```

## 技术栈

- **Python 3**：主要开发语言
- **Selenium**：模拟浏览器操作，处理动态页面
- **ChromeDriver**：Chrome 浏览器驱动
- **pymysql**：连接 MySQL 数据库
- **xlwt**：写入 Excel 文件
- **openpyxl**：读取 Excel 文件
- **csv**：处理 CSV 文件

## 核心功能

### 1. 数据爬取
- 使用 Selenium 模拟浏览器操作，爬取 Boss 直聘网站的职位信息
- 支持多页数据爬取（默认爬取 29 页）
- 自动处理验证码（需要手动完成）
- 提取详细的职位信息，包括：
  - 职位名称、工作地点、薪资范围
  - 学历要求、工作经验
  - 公司名称、行业信息、公司规模
  - 公司福利
  - 岗位职责、任职要求、加分项

### 2. 数据清洗

#### 2.1 爬虫数据清洗（spider.py）

- **职位名称处理**：
  - 尝试多种方式定位职位名称元素
  - 当无法获取时，设置默认值 "未知职位"

- **学历要求处理**：
  - 从元素中提取文本内容
  - 移除多余的 "::before" 字符串
  - 当无法获取时，设置默认值 "学历不限"

- **公司福利处理**：
  - 提取所有福利标签
  - 将多个福利标签合并为一个字符串
  - 当没有福利信息时，设置默认值 "无特别福利"

- **岗位职责、任职要求和加分项处理**：
  - 从职位详情文本中提取相关内容
  - 通过关键词分割和过滤，提取结构化信息
  - 当无法获取时，设置默认值 "未提供" 或 "无"

#### 2.2 数据导入清洗（excel_to_sql.py）

- **数据类型转换**：
  - 将薪资数据转换为浮点数类型
  - 当薪资数据为空时，设置默认值 0

- **数据验证**：
  - 检查文件表头是否符合预期
  - 确保数据格式正确，避免导入错误

### 3. 数据存储
- 将爬取的数据保存到 MySQL 数据库
- 将爬取的数据保存到 Excel 文件
- 将爬取的数据保存到 CSV 文件

## 安装与运行

### 1. 安装依赖

```bash
# 安装所需依赖
pip install selenium pymysql xlwt openpyxl
```

### 2. 运行爬虫

```bash
# 运行爬虫
python spider.py
```

### 3. 导入数据到数据库

```bash
# 导入数据到数据库
python excel_to_sql.py
```

## 数据库配置

在 `DBManager.py` 中配置数据库连接信息：

```python
def __init__(self, host='localhost', user='root', password='123456',
             database='job_data', charset='utf8mb4'):
    # 数据库连接配置
```

## 注意事项

1. 爬虫运行需要配置 Cookies，可在 `spider.py` 中设置
2. 需要下载对应版本的 ChromeDriver，并将其添加到系统路径中
3. 爬虫运行过程中可能需要手动完成验证码验证
4. 数据导入需要确保 MySQL 服务正在运行

## 数据结构

### 爬虫提取的数据结构

| 字段 | 描述 | 示例 |
|------|------|------|
| 职位名称 | 招聘职位的名称 | 产品助理 |
| 工作地点 | 职位的工作地点 | 北京市朝阳区 |
| 薪资范围 | 职位的薪资范围 | 10K-15K |
| 学历要求 | 职位的学历要求 | 本科 |
| 工作经验 | 职位的工作经验要求 | 1-3年 |
| 公司名称 | 招聘公司的名称 | 某某科技有限公司 |
| 行业信息 | 公司所属行业 | 互联网 |
| 公司规模 | 公司的规模 | 100-500人 |
| 公司福利 | 公司提供的福利 | 五险一金，带薪年假 |
| 岗位职责 | 职位的工作内容 | 负责产品需求分析，产品设计等 |
| 任职要求 | 职位的应聘要求 | 本科及以上学历，1-3年相关经验 |
| 加分项 | 职位的加分条件 | 有互联网产品经验优先 |

### 数据库表结构

```sql
CREATE TABLE IF NOT EXISTS jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_name VARCHAR(100) NOT NULL COMMENT '职位名称',
    company_add VARCHAR(200) COMMENT '公司地址',
    month VARCHAR(20) COMMENT '招聘月份',
    salary_min DECIMAL(10,2) COMMENT '最低薪资(千)',
    salary_max DECIMAL(10,2) COMMENT '最高薪资(千)',
    record VARCHAR(50) COMMENT '学历要求',
    company_name VARCHAR(100) COMMENT '公司名称',
    company_type VARCHAR(100) COMMENT '公司类型',
    scope VARCHAR(100) COMMENT '公司规模',
    tag VARCHAR(200) COMMENT '职位标签',
    welfare TEXT COMMENT '公司福利',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='职位信息表';
```

## 总结

Boss_data 模块是一个完整的数据采集和处理系统，通过 Selenium 模拟浏览器操作爬取 Boss 直聘网站的详细职位信息，并进行数据清洗和存储。该模块为整个 Boss 直聘数据分析系统提供了可靠的数据基础，支持后续的数据分析和可视化功能。