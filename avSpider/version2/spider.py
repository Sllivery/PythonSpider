import requests
import ssl
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context

class Spider:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Macintosh; '
                'Intel Mac OS X 10_13_6) '
                'AppleWebKit/537.36 (KHTML, '
                'like Gecko) Chrome/68.0.3440.106 '
                'Safari/537.36'
        }

    def send_requests(self):
        request = requests.get(self.url)
        parsed_html = request.text
        if 'protected by xxx' in parsed_html:
            firefox = webdriver.Firefox # 另一个类处理浏览器这种情况
        else:
            return parsed_html
        pass

    def browser_parse_html(self):
        pass

    def parse_html(self, html_text):
        soup = BeautifulSoup(html_text)
        # 返回的是原生数据
        pass