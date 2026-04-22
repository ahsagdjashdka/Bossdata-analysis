# -- coding: utf-8 --
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import xlwt
from DBManager import DBManager

def init_database():
    """Initialize database and create table"""
    with DBManager() as db:
        db.create_table()

def save_to_database(job_data):
    """Save job data to database"""
    with DBManager() as db:
        # Prepare complete job data (12 fields)
        sql = """
        INSERT INTO jobs (
            title, area, salary, education, experience,
            company, industry, scale, welfare,
            responsibilities, requirements, bonuses
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            update_time = CURRENT_TIMESTAMP
        """
        try:
            db.execute(sql, job_data)
            print(f"数据已保存到数据库")
            return db.cursor.lastrowid
        except Exception as e:
            print(f"保存数据到数据库时出错: {str(e)}")
            return None
def main():
    init_database()
    baseurl = "https://www.zhipin.com/c100010000/?query=产品助理&page="
    savePath = "test1.xls"

    # 浏览器配置
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)

    try:
        # 先访问首页获取必要cookies
        driver.get("https://www.zhipin.com/")
        time.sleep(3)

        dataList = []
        for i in range(1, 30):
            url = baseurl + str(i)
            print(f"正在处理第{i}页: {url}")

            driver.get(url)
            time.sleep(3)

            # 检查是否被重定向到验证页面
            if "verify" in driver.current_url:
                input("请手动完成验证后按回车继续...")
                driver.get(url)
                time.sleep(3)

            # 多种方式尝试定位职位元素
            job_links = []
            locators = [
                (By.CSS_SELECTOR, 'div.job-card-wrap a.job-name'),
                (By.CSS_SELECTOR, 'li.job-card-box a.job-name'),
                (By.XPATH, '//a[contains(@class, "job-name")]')
            ]

            for locator in locators:
                try:
                    job_links = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located(locator)
                    )
                    if job_links:
                        print(f"使用定位器 {locator} 找到 {len(job_links)} 个职位链接")
                        break
                except:
                    continue

            if not job_links:
                print("警告：未找到职位信息！")
                continue

            # 处理职位数据
            for link in job_links[:20]:
                try:
                    # 获取职位详情页URL
                    job_url = link.get_attribute('href')
                    if not job_url.startswith('http'):
                        job_url = "https://www.zhipin.com" + job_url

                    print(f"正在访问职位详情页: {job_url}")

                    # 新标签页打开职位详情页
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(job_url)
                    time.sleep(3)

                    # 从详情页提取数据
                    data = extract_job_detail_data(driver)
                    if data:
                        save_to_database(data)
                        dataList.append(data)
                        # 修改输出格式：职位名称、学历要求、工作地点
                        print(f"已提取: {data[0]} | {data[3]} | {data[1]}")

                    # 关闭详情页标签，返回列表页
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(1)

                except Exception as e:
                    print(f"处理职位时出错: {str(e)}")
                    # 确保回到列表页
                    if len(driver.window_handles) > 1:
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                    continue

        if dataList:
            saveData(dataList, savePath)
        else:
            print("未获取到有效数据！")

    finally:
        driver.quit()
        print("爬取任务完成！")

def extract_job_detail_data(driver):
    """从职位详情页提取数据"""
    data = []

    # 1. 职位名称
    try:
        title = driver.find_element(By.CSS_SELECTOR, 'div.namediv[title]').text
    except:
        try:
            title = driver.find_element(By.CSS_SELECTOR, 'div.name').text
        except:
            title = "未知职位"
    data.append(title)

    # 2. 工作地点
    try:
        area = driver.find_element(By.CSS_SELECTOR, 'a.text-city').text.strip()
    except:
        area = "未知地区"
    data.append(area)

    # 3. 薪资范围
    try:
        salary = driver.find_element(By.CSS_SELECTOR, 'span.salary').text
    except:
        salary = "面议"
    data.append(salary)

    # 4. 学历要求
    try:
        edu = driver.find_element(By.XPATH, '//span[contains(@class, "text-degree")]').get_attribute('textContent').strip()
        if '::before' in edu:
            edu = edu.replace('::before', '').strip()
    except:
        edu = "学历不限"
    data.append(edu)

    # 5. 工作经验
    try:
        experience = driver.find_element(By.CSS_SELECTOR, 'span.text-experiece').text.strip()
    except:
        experience = "经验不限"
    data.append(experience)

    # 6. 公司名称
    try:
        company = driver.find_element(By.CSS_SELECTOR, 'a[ka="job-detail-company_custompage"]').text.strip('* ').strip()
    except:
        company = "未知公司"
    data.append(company)

    # 7. 行业信息
    try:
        industry = driver.find_element(By.CSS_SELECTOR, 'a[ka="job-detail-brandindustry"]').text.strip()
    except:
        industry = "未知行业"
    data.append(industry)

    # 8. 公司规模
    try:
        scale = driver.find_element(By.XPATH, '//p[contains(.//i[@class="icon-scale"])]').text.replace('"', '').strip()
    except:
        scale = "未知规模"
    data.append(scale)

    # 9. 公司福利
    try:
        welfare_tags = driver.find_elements(By.CSS_SELECTOR, 'div.job-tags span')
        welfare = "，".join([tag.text for tag in welfare_tags if tag.text])
        if not welfare:
            welfare = "无特别福利"
    except:
        welfare = "无特别福利"
    data.append(welfare)

    # 10. 岗位职责
    try:
        responsibilities = []
        job_sec = driver.find_element(By.CSS_SELECTOR, 'div.job-sec-text')
        lines = job_sec.text.split('\n')
        found_responsibilities = False

        for line in lines:
            line = line.strip()
            if "岗位职责：" in line:
                found_responsibilities = True
                continue
            if "任职要求：" in line:
                break
            if found_responsibilities and line:
                responsibilities.append(line)

        responsibilities_text = "\n".join(responsibilities) if responsibilities else "未提供"
    except:
        responsibilities_text = "未提供"
    data.append(responsibilities_text)

    # 11. 任职要求
    try:
        requirements = []
        job_sec = driver.find_element(By.CSS_SELECTOR, 'div.job-sec-text')
        lines = job_sec.text.split('\n')
        found_requirements = False

        for line in lines:
            line = line.strip()
            if "任职要求：" in line:
                found_requirements = True
                continue
            if "加分项：" in line or "加分项" in line:
                break
            if found_requirements and line:
                requirements.append(line)

        requirements_text = "\n".join(requirements) if requirements else "未提供"
    except:
        requirements_text = "未提供"
    data.append(requirements_text)

    # 12. 加分项
    try:
        bonuses = []
        job_sec = driver.find_element(By.CSS_SELECTOR, 'div.job-sec-text')
        lines = job_sec.text.split('\n')
        found_bonuses = False

        for line in lines:
            line = line.strip()
            if "加分项：" in line or "加分项" in line:
                found_bonuses = True
                continue
            if found_bonuses and line:
                bonuses.append(line)

        bonuses_text = "\n".join(bonuses) if bonuses else "无"
    except:
        bonuses_text = "无"
    data.append(bonuses_text)
    return data

def saveData(dataList, savePath):
    """保存数据到Excel"""
    if not dataList:
        return

    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet('test')

    # 设置列名（按新顺序）
    headers = [
        "职位名称", "工作地点", "薪资范围", "学历要求", "工作经验",
        "公司名称", "行业信息", "公司规模", "公司福利", "岗位职责",
        "任职要求", "加分项"
    ]

    for col, header in enumerate(headers):
        sheet.write(0, col, header)
        sheet.col(col).width = 256 * 20  # 设置列宽

    for row, data in enumerate(dataList, 1):
        for col, value in enumerate(data):
            sheet.write(row, col, value)

    book.save(savePath)
    print(f"数据已保存到 {savePath}")

if __name__ == "__main__":
    main()