# Boss 直聘数据分析系统

## 项目简介

Boss 直聘数据分析系统是一个基于 Python 和 Vue.js 的数据分析平台，用于爬取和分析 Boss 直聘网站的招聘数据，提供数据可视化和分析功能。

## 技术栈

- **前端**：Vue 3 + Vite + ECharts
- **后端**：Flask + SQLAlchemy
- **爬虫**：Selenium
- **数据库**：SQLite + MySQL

## 项目结构

```
Bossdata-analysis-main/
├── Boss_data/          # Selenium 爬虫（详细数据）
│   ├── DBManager.py    # 数据库管理类
│   ├── spider.py       # 主要爬虫脚本
│   └── excel_to_sql.py # Excel 数据导入数据库脚本
├── flask/              # 后端 Flask 应用
│   ├── controllers/    # API 控制器
│   ├── models/         # 数据模型
│   ├── utils/          # 工具函数
│   └── views/          # 视图和配置
├── sql_boss/           # SQL 分析脚本
├── vue-project/        # 前端 Vue 项目
│   ├── public/         # 静态资源
│   └── src/            # 前端源代码
└── README.md           # 项目说明文档
```

## 功能模块

### 1. 数据爬取模块

使用 Selenium 模拟浏览器操作，爬取 Boss 直聘网站的招聘数据：
- 支持详细职位信息提取，包括岗位职责、任职要求、加分项等
- 数据保存到 MySQL 数据库和 Excel 文件
- 适合需要交互和动态渲染的复杂页面

### 2. 数据分析模块

使用 SQL 脚本对爬取的数据进行分析，包括：
- 各城市需求分析
- 各行业需求分析
- 各学历需求分析
- 热门职位分析

### 3. 后端 API 模块

提供 RESTful API 接口，包括：
- `/api/getMapData`：获取地图数据，用于可视化展示
- `/api/get_seller_data`：获取销售数据

### 4. 前端可视化模块

使用 Vue 3 和 ECharts 实现数据可视化，包括：
- 地图展示：展示各城市的招聘需求分布
- 趋势分析：展示招聘需求的时间趋势
- 热门职位：展示热门职位排名
- 行业分析：展示各行业的招聘需求
- 综合大屏：展示所有数据的综合视图

## 安装与部署

### 1. 后端安装

```bash
# 进入 flask 目录
cd flask/views

# 安装依赖
pip install -r requirements.txt

# 启动服务器
python run.py
```

### 2. 前端安装

```bash
# 进入 vue-project 目录
cd vue-project

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

### 3. 爬虫运行

```bash
# 进入 Boss_data 目录
cd Boss_data

# 安装依赖
pip install selenium pymysql xlwt

# 运行爬虫
python spider.py
```

## API 接口说明

### 1. 获取地图数据

- **URL**：`/api/getMapData`
- **方法**：GET
- **返回**：JSON 格式的地图数据，包含城市、需求等级和坐标

### 2. 获取销售数据

- **URL**：`/api/get_seller_data`
- **方法**：GET
- **返回**：JSON 格式的销售数据

## 数据可视化页面

- **地图页面**：展示各城市的招聘需求分布
- **趋势页面**：展示招聘需求的时间趋势
- **热门职位页面**：展示热门职位排名
- **行业分析页面**：展示各行业的招聘需求
- **综合大屏**：展示所有数据的综合视图

## 数据分析脚本

- `education_month_analysis.sql`：学历月度分析
- `industry_month_analysis.sql`：行业月度分析
- `java_hot_job.sql`：Java 热门职位分析
- `job_data.sql`：职位数据查询
- `python_hot_job.sql`：Python 热门职位分析
- `region_month_analysis.sql`：区域月度分析
- `rgzn_hot_job.sql`：热门职位分析

## 运行效果

### 地图可视化

![地图可视化](https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=Boss%20直聘数据分析系统地图可视化界面，展示各城市招聘需求分布，使用红色到蓝色的渐变色表示需求热度，中国地图背景，清晰的城市标记&image_size=landscape_16_9)

### 趋势分析

![趋势分析](https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=Boss%20直聘数据分析系统趋势分析界面，展示招聘需求的时间趋势，使用折线图表示，清晰的坐标轴和数据点，蓝色线条&image_size=landscape_16_9)

### 热门职位

![热门职位](https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=Boss%20直聘数据分析系统热门职位界面，展示热门职位排名，使用柱状图表示，职位名称在Y轴，需求数量在X轴，红色柱状图&image_size=landscape_16_9)

## 注意事项

1. 爬虫运行需要配置 Cookies，可在 `spider.py` 中设置
2. 数据库使用 SQLite，默认存储在 `flask/views/database.db`
3. Boss_data 爬虫使用 MySQL 数据库，需要在 `DBManager.py` 中配置连接信息
4. 前端开发服务器默认运行在 `http://localhost:5173`
5. 后端服务器默认运行在 `http://localhost:5000`

## 未来计划

1. 增加更多数据源，如其他招聘网站
2. 优化爬虫性能，提高数据爬取效率
3. 增加更多数据分析维度，如薪资分析、技能要求分析
4. 改进前端界面，提供更好的用户体验
5. 增加用户认证系统，支持多用户使用

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 许可证

MIT License
