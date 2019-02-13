import time
import fateadm_api
import requests
import urllib.request
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from PIL import Image
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GetBrowserInstance:
    '''
    1.单例创建一个浏览器实例
    2.想好控制内存占用的方法：每个网页打开之后，设置一个time flag来保证30s之内关闭，释放资源
    3.类的结构：几个类
    4.数据的导出：json，数据导出类
    5.跨平台的应用：最后跑在Linux上，chrome headless对linux的支持
    '''

def get_captcha():
    print("选择抓取")
    # 定义一个表头
    headers = {'User-Agent':
                   'Mozilla/5.0 (Macintosh; '
                   'Intel Mac OS X 10_13_6) '
                   'AppleWebKit/537.36 (KHTML, '
                   'like Gecko) Chrome/68.0.3440.106 '
                   'Safari/537.36'
               }
    # 打开网页
    url = "http://xuz.122.gov.cn/"
    chrome = webdriver.Firefox()
    chrome.get(url)
    try:
        search_tag_a = chrome.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[2]/div[1]/ul/li[4]/a")
        search_tag_a.click()
        time.sleep(2)

        # 切换到目标标签页,点击查询按钮
        new_window = chrome.window_handles[1]
        chrome.switch_to.window(new_window)
        time.sleep(2)

        # 因为直接到button点击事件无法完成，所以从父节点开始找
        f_tag_target = chrome.find_element_by_xpath("//*[@id='formsearch']/div[2]/div[4]").click()
        search_tag_target = chrome.find_element_by_xpath("//*[@id='btnSearch']")
        search_tag_target.click()
        time.sleep(2)
        captcah_img = chrome.find_element_by_xpath("/html/body/div[1]/div/table/tbody/tr[2]/"
                                                   "td[2]/div/table/tbody/tr[2]/td[2]/div/span/img")

        # 先保存整个页面的截图
        location = (1120, 316, 1120 + 175, 316 + 58)
        chrome.save_screenshot("/Users/luxness/Desktop/test.png")

        # 然后对元素进行截图
        picture = Image.open("/Users/luxness/Desktop/test.png")
        picture = picture.crop(location)
        picture.save("/Users/luxness/Desktop/test.png")

        # 调用网站API
        result = fateadm_api.TestFunc()
        input_box = chrome.find_element_by_xpath("//*[@id='csessionid']")
        input_box.send_keys(result)
        input_box.send_keys(Keys.RETURN)
        time.sleep(100)
    except Exception as e:
        print(e)
    finally:
        chrome.close()


def test():
    url = "http://nkg.122.gov.cn/m/tmri/captcha/math"
    urllib.request
    # csessionid = fateadm_api.TestFunc()
    headers = {'User-Agent':
                   'Mozilla/5.0 (Macintosh; '
                   'Intel Mac OS X 10_13_6) '
                   'AppleWebKit/537.36 (KHTML, '
                   'like Gecko) Chrome/68.0.3440.106 '
                   'Safari/537.36'
               }
    data = {"page": "0",
            "glbm": "320100000400",
            "hpzl": "02",
            "type": "0",
            "startTime": "2018-12-02",
            "endTime": "2019-02-02",
            "csessionid": ""}
    result = requests.post("http://nkg.122.gov.cn/m/mvehxh/getTfhdList", headers=headers)
    print(result.text)

def test_new_version():
    try:
        url = "http://nkg.122.gov.cn/views/vehxhhdpub.html"
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')
        firefox = webdriver.Firefox(options=options)
        # firefox = webdriver.Firefox()
        firefox.get(url)
        time.sleep(2)
        search_button = firefox.find_element_by_xpath("//*[@id='formsearch']/div[2]/div[4]")
        search_button.click()
        time.sleep(1)
        captcha_image = firefox.find_element_by_xpath(
            "/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td[2]/div/span/img")
        captcha_image.screenshot("/Users/luxness/Desktop/test.png")
        captcha_result = fateadm_api.TestFunc()
        input_box = firefox.find_element_by_xpath("//*[@id='csessionid']")
        input_box.send_keys(captcha_result)
        sure_butt = firefox.find_element_by_xpath("/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button[1]")
        sure_butt.click()
        # 得到数据界面然后转成html送给bs4解析
        response = firefox.page_source
        soup = BeautifulSoup(response, 'lxml')
        test_tag = soup.find_all('tr')
        print(test_tag)
        # all_target = soup.find('tbody').find_all('tr')
        # for item in all_target:
        #     for single_tr in item:
        #         author = single_tr.get_text()
        #         sort = single_tr.get_text()
        #         range = single_tr.get_text()
        #         time_range = single_tr.get_text()
        #         print(author + sort + range + time_range)
    finally:
        firefox.close()

def app():
    url = "https://www.122.gov.cn/m/index/"
    response = requests.get(url)
    print(response.text)
    soup = BeautifulSoup(response.text, 'lxml')
    target = soup.find_all("a", _class="_blank")
    for targets in target:
        print(targets['href'])

if __name__ == "__main__":
    test_new_version()
