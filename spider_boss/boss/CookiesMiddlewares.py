from scrapy import signals
from selenium import webdriver
import time
from scrapy.http.response.html import HtmlResponse


class CookiesMiddlewares(object):

    def __init__(self):
        print("初始化浏览器")
        self.driver = webdriver.Chrome()

    def process_request(self,request,spider):
        self.driver.get(request.url)
        time.sleep(5)
        # 我们等待5秒钟，让其加载
        source = self.driver.page_source
        #获取页面的源码
        response = HtmlResponse(url=self.driver.current_url,body=source,request=request,encoding='utf-8')
        # Response 对象用来描述一个HTTP响应
        return response
        # 这样我们就获取到了所有的信息，并返回response