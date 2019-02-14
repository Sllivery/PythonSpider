import time
import fateadm_api
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MakeSomeTips:
    '''
    1.单例创建一个浏览器实例
    2.想好控制内存占用的方法：每个网页打开之后，设置一个time flag来保证30s之内关闭，释放资源
    3.类的结构：几个类
    4.数据的导出：json，数据导出类
    5.跨平台的应用：最后跑在Linux上，chrome headless对linux的支持
    6.如何判断一条记录是不是新的
    --从web爬取到第一条记录作为缓存，然后如果有时间更前面的，则替换原记录
    --利用python time库
    --数据的结构：城市->车管所->不同类型的车
    7.因为只需要的是新记录，所以现在不要考虑循环的问题了
    '''

class DataOB:
    def __init__(self, author, sort, num_range, time):
        self.author = author
        self.sort = sort
        self.num_range = num_range
        self.time = time

    def __repr__(self):
        return "车管所: " + self.author + " 汽车种类: " + self.sort + " 牌照号段: " + self.num_range + " 时间: " + self.time

class URLSelector:
    '''
    :param name 选择一个模式来获取url 默认不填为全部都爬 填的话参数应当是中文省分，除江苏和浙江。江苏浙江需要具体到每个城市
    :param city_url_maaping 是是城市名作为键的字典，来对应网站的url
    '''
    def __init__(self, name=""):
        self.name = name
        self.city_url_mapping = {

        }
        if self.name == "":
            self.return_list_all()
        if self.name != "":
            self.return_specified_city(self.name)

    def return_list_all(self):
        return self.city_url_mapping

    def return_specified_city(self, name):
        url = self.city_url_mapping[name]
        return url

class Spider:
    '''
    '''
    def test_new_version(self):
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
            sure_butt = firefox.find_element_by_xpath(
                "/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button[1]")
            sure_butt.click()
            # 得到数据界面然后转成html送给bs4解析
            response = firefox.page_source
            soup = BeautifulSoup(response, 'lxml')
            test_tag = soup.find_all('tr')
            print(test_tag)
        finally:
            firefox.close()


def test_new_version():
    def parse(source):
        response = source
        soup = BeautifulSoup(response, 'lxml')
        data_rows = soup.find('table', class_='table table-striped').find('tbody').find_all('tr')
        for data_row in data_rows:
            data_list = data_row.contents
            while ' ' in data_list:
                data_list.remove(' ')
            print(data_list[2])

    def send_request(firefox):
        print("点击查询")
        search_button = firefox.find_element_by_xpath("//*[@id='formsearch']/div[2]/div[4]")
        search_button.click()
        time.sleep(1)
        captcha_image = firefox.find_element_by_xpath(
            "/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td[2]/div/span/img")
        captcha_image.screenshot("/Users/luxness/Desktop/test.png")
        print("正在处理验证码...")
        captcha_result = fateadm_api.TestFunc()
        input_box = firefox.find_element_by_xpath("//*[@id='csessionid']")
        input_box.send_keys(captcha_result)
        sure_butt = firefox.find_element_by_xpath(
            "/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button[1]")
        sure_butt.click()
        return firefox.page_source
    try:
        url = "http://bj.122.gov.cn/views/vehxhhdpub.html"
        # options = webdriver.FirefoxOptions()
        # options.add_argument('-headless')
        # firefox = webdriver.Firefox(options=options)
        # print("浏览器打开")
        firefox = webdriver.Firefox()
        firefox.get(url)
        print("等待ajax加载信息")
        time.sleep(2)
        page_source = send_request(firefox)
        parse(page_source)
    finally:
        firefox.close()

def test():
    result_list = []
    with open('/Users/luxness/Desktop/test.html') as f:
        response = f
        soup = BeautifulSoup(response, 'lxml')
        data_rows = soup.find('table', class_='table table-striped').find('tbody').find_all('tr')
        for data_row in data_rows:
            data_list = data_row.contents
            while ' ' in data_list:
                data_list.remove(' ')
            data = DataOB(data_list[0].get_text(), data_list[1].get_text(), data_list[2].get_text(), data_list[3].get_text())
            result_list.append(data)
    print(result_list)


if __name__ == "__main__":
    test_new_version()