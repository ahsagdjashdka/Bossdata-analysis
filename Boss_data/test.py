from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time


def scrape_job_list(driver):
    """从左侧列表页提取基础信息（优化版）"""
    jobs = []

    # 等待列表容器加载
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.rec-job-list'))
        )
    except:
        print("列表页加载超时")
        return jobs

    # 卡片选择器（根据最新结构调整）
    card_selectors = [
        'div.rec-job-list div.card-area li.job-card-box',  # 基础选择器
        'div.rec-job-list div.card-area.is-seen li.job-card-box',
        'div.rec-job-list div.card-area.has-flag li.job-card-box'
    ]
    # 或者使用更简洁的通用选择器
    universal_selector = 'ul.rec-job-list div[class*="card-area"] li.job-card-box'

    for selector in card_selectors:
        try:
            cards = driver.find_elements(By.CSS_SELECTOR, universal_selector)
            if not cards:
                print("通用选择器未找到卡片，尝试备用选择器")
                for selector in card_selectors:
                    try:
                        cards = driver.find_elements(By.CSS_SELECTOR, selector)
                        if cards:
                            break
                    except:
                        continue
            if not cards:
                print("所有选择器均未找到卡片")
                return jobs
            print(f"找到 {len(cards)} 个职位")

            for card in cards:
                try:
                    job = {
                        'title': card.find_element(By.CSS_SELECTOR, '.job-title').text.strip(),
                        'company': card.find_element(By.CSS_SELECTOR, '.boss-info').get_attribute('innerText').strip(),
                        'location': card.find_element(By.CSS_SELECTOR, '.company-location').text.replace('·','-').strip(),
                        'tags': [tag.text for tag in card.find_elements(By.CSS_SELECTOR, '.tag-list li')],
                        'detail_url': card.find_element(By.CSS_SELECTOR, 'a.job-name').get_attribute('href')
                    }

                    # 从tags提取经验和学历
                    for tag in job['tags']:
                        if '年' in tag:
                            job['experience'] = tag
                        elif any(edu in tag for edu in ['本科', '硕士', '博士', '大专', '学历不限']):
                            job['education'] = tag

                    jobs.append(job)
                except Exception as e:
                    print(f"提取职位失败: {str(e)}")
                    continue
        except Exception as e:
            print(f"选择器 {selector} 失败: {str(e)}")

    return jobs


def scrape_job_detail(driver, detail_url):
    result = {
        'salary': '薪资未公开',
        'labels': [],
        'description': '无描述信息'
    }

    original_window = driver.current_window_handle
    try:
        # 新标签页打开详情页
        driver.execute_script(f"window.open('{detail_url}');")
        driver.switch_to.window(driver.window_handles[-1])

        # 1. 提取薪资（多种选择器尝试）
        salary_selectors = ['.salary', '.salary-text', '.job-salary', '.salary-content']
        for selector in salary_selectors:
            try:
                salary_element = WebDriverWait(driver, 2).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
                result['salary'] = salary_element.text.strip()
                break
            except:
                continue

        # 2. 提取标签
        label_selectors = [
            'ul.job-label-list li',
            'div.job-detail-body.ul li',
            'div.job-detail-operate.ul li',
        ]

        for selector in label_selectors:
            try:
                labels = driver.find_elements(By.CSS_SELECTOR, selector)
                if labels:
                    result['labels'] = [label.text.strip() for label in labels if label.text.strip()]
                    break
            except:
                continue

        # 3. 提取描述（处理p.desc及其内容）
        try:
            # 方法1：直接获取p.desc
            desc_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'p.desc')))

            # 方法2：如果为空，尝试获取职位描述标题后的第一个p标签
            if not desc_element.text.strip():
                desc_element = driver.find_element(By.XPATH,
                                                   '//h3[contains(text(), "职位描述")]/following-sibling::p[1]')

            # 反混淆处理（移除span保留文本）
            driver.execute_script("""
                    const desc = arguments[0];
                    const spans = desc.querySelectorAll('span');
                    spans.forEach(span => {
                        span.replaceWith(document.createTextNode(span.textContent));
                    });
                """, desc_element)

            result['description'] = desc_element.text.strip()

        except Exception as e:
            print(f"提取描述失败: {str(e)}")
            # 最终回退方案：获取整个job-detail-body的文本
            try:
                fallback_desc = driver.find_element(By.CSS_SELECTOR, 'div.job-detail-body').text
                result['description'] = "\n".join(
                    [line.strip() for line in fallback_desc.split('\n') if line.strip()])
            except:
                pass

    except Exception as e:
        print(f"详情页处理异常: {str(e)}")
    finally:
        # 确保返回原窗口
        if len(driver.window_handles) > 1:
            driver.close()
        driver.switch_to.window(original_window)
        time.sleep(random.uniform(1.5, 3))  # 更自然的延迟

    return result


def scrape_all_jobs(driver, base_url, max_jobs=5):
    """完整的混合爬取流程"""
    print(f"开始爬取: {base_url}")
    driver.get(base_url)
    time.sleep(3)

    # 1. 爬取列表页基础信息
    jobs = scrape_job_list(driver)
    print(f"获取到 {len(jobs)} 个职位基础信息")

    # 2. 补全详情信息（限制数量）
    for i, job in enumerate(jobs[:max_jobs]):
        if not job.get('detail_url'):
            continue

        print(f"\n处理进度: {i + 1}/{min(len(jobs), max_jobs)}")
        print(f"职位: {job['title']}")

        detail = scrape_job_detail(driver, job['detail_url'])
        job.update(detail)

        # 打印当前结果
        print(f"薪资: {job.get('salary')}")
        print(f"标签: {job.get('labels')}")

    return jobs[:max_jobs]


# 使用示例
if __name__ == "__main__":
    from selenium import webdriver

    # 浏览器配置
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(3)

    try:
        jobs = scrape_all_jobs(
            driver,
            "https://www.zhipin.com/web/geek/job?query=产品经理",
            max_jobs=3  # 限制爬取数量
        )

        # 最终输出
        print("\n=== 最终结果 ===")
        for i, job in enumerate(jobs):
            print(f"\n【职位{i + 1}】{job['title']}")
            print(f"公司: {job['company']}")
            print(f"薪资: {job['salary']}")
            print(f"经验: {job.get('experience', '无')}")
            print(f"学历: {job.get('education', '无')}")
            print(f"地点: {job['location']}")
            print(f"标签: {', '.join(job['labels'])}")
            print(f"描述摘要: {job['description'][:50]}...")
    finally:
        driver.quit()