import time
import fateadm_api
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MakeSomeTips:
    '''
    3.类的结构：几个类
    4.数据的导出：json，数据导出类
    5.跨平台的应用：最后跑在Linux上，chrome headless对linux的支持
    6.如何判断一条记录是不是新的
    --从web爬取到第一条记录作为缓存，然后如果有时间更前面的，则替换原记录
    --利用python time库
    --数据的结构：城市->车管所->不同类型的车
    7.因为只需要的是新记录，所以现在不要考虑循环的问题了

    现在要解决的事情：
    把所有硬睡眠改掉
    '''


class DataOB:
    def __init__(self, author, sort, num_range, time):
        self.author = author
        self.sort = sort
        self.num_range = num_range
        self.time = time

    def __repr__(self):
        return "车管所: " + self.author + " 汽车种类: " + self.sort + " 牌照号段: " + self.num_range + " 时间: " + self.time


class SpiderSchedule:
    '''
    1. 爬虫调度器
    根据队列中的url来循环或者选取url来给爬虫用

    2.数据格式化并导出
    '''
    def __init__(self):
        self.list = {
            '北京': 'http://bj.122.gov.cn/views/vehxhhdpub.html',
            '天津': 'http://tj.122.gov.cn/views/vehxhhdpub.html',
            '河北': 'http://he.122.gov.cn/views/vehxhhdpub.html',
            '山西': 'http://sx.122.gov.cn/views/vehxhhdpub.html',
            '内蒙古': 'http://nm.122.gov.cn/views/vehxhhdpub.html',
            '辽宁': 'http://ln.122.gov.cn/views/vehxhhdpub.html',
            '吉林': 'http://hl.122.gov.cn/views/vehxhhdpub.html',
            '黑龙江': 'http://sh.122.gov.cn/views/vehxhhdpub.html',
            '南京': 'http://nkg.122.gov.cn/views/vehxhhdpub.html',
            '无锡': 'http://wux.122.gov.cn/views/vehxhhdpub.html',
            '徐州': 'http://xuz.122.gov.cn/views/vehxhhdpub.html',
            '常州': 'http://czx.122.gov.cn/views/vehxhhdpub.html',
            '苏州': 'http://szv.122.gov.cn/views/vehxhhdpub.html',
            '南通': 'http://ntg.122.gov.cn/views/vehxhhdpub.html',
            '连云港': 'http://lyg.122.gov.cn/views/vehxhhdpub.html',
            '淮安': 'http://has.122.gov.cn/views/vehxhhdpub.html',
            '盐城': 'http://ynz.122.gov.cn/views/vehxhhdpub.html',
            '扬州': 'http://yzo.122.gov.cn/views/vehxhhdpub.html',
            '镇江': 'http://zhe.122.gov.cn/views/vehxhhdpub.html',
            '泰州': 'http://tzs.122.gov.cn/views/vehxhhdpub.html',
            '宿迁': 'http://suq.122.gov.cn/views/vehxhhdpub.html',
            '杭州': 'http://hgh.122.gov.cn/views/vehxhhdpub.html',
            '宁波': 'http://ngb.122.gov.cn/views/vehxhhdpub.html',
            '温州': 'http://wnz.122.gov.cn/views/vehxhhdpub.html',
            '嘉兴': 'http://jix.122.gov.cn/views/vehxhhdpub.html',
            '湖州': 'http://hzh.122.gov.cn/views/vehxhhdpub.html',
            '绍兴': 'http://sxg.122.gov.cn/views/vehxhhdpub.html',
            '金华': 'http://jha.122.gov.cn/views/vehxhhdpub.html',
            '衢州': 'http://quz.122.gov.cn/views/vehxhhdpub.html',
            '舟山': 'http://zos.122.gov.cn/views/vehxhhdpub.html',
            '台州': 'http://tzz.122.gov.cn/views/vehxhhdpub.html',
            '丽水': 'http://lss.122.gov.cn/views/vehxhhdpub.html',
            '安徽': 'http://ah.122.gov.cn/views/vehxhhdpub.html',
            '福建': 'http://fj.122.gov.cn/views/vehxhhdpub.html',
            '江西': 'http://jx.122.gov.cn/views/vehxhhdpub.html',
            '山东': 'http://sd.122.gov.cn/views/vehxhhdpub.html',
            '河南': 'http://ha.122.gov.cn/views/vehxhhdpub.html',
            '湖北': 'http://hb.122.gov.cn/views/vehxhhdpub.html',
            '湖南': 'http://hn.122.gov.cn/views/vehxhhdpub.html',
            '广东': 'http://gd.122.gov.cn/views/vehxhhdpub.html',
            '广西': 'http://gx.122.gov.cn/views/vehxhhdpub.html',
            '海南': 'http://hi.122.gov.cn/views/vehxhhdpub.html',
            '重庆': 'http://cq.122.gov.cn/views/vehxhhdpub.html',
            '四川': 'http://sc.122.gov.cn/views/vehxhhdpub.html',
            '贵州': 'http://gz.122.gov.cn/views/vehxhhdpub.html',
            '云南': 'http://yn.122.gov.cn/views/vehxhhdpub.html',
            '西藏': 'http://xz.122.gov.cn/views/vehxhhdpub.html',
            '陕西': 'http://sn.122.gov.cn/views/vehxhhdpub.html',
            '甘肃': 'http://gs.122.gov.cn/views/vehxhhdpub.html',
            '青海': 'http://qh.122.gov.cn/views/vehxhhdpub.html',
            '宁夏': 'http://nx.122.gov.cn/views/vehxhhdpub.html',
            '新疆': 'http://xj.122.gov.cn/views/vehxhhdpub.html'
        }
        for url in self.list:
            Spider(self.list[url])  # 返回的data应该是形如{'xx车管所':[小汽车,投放号段,投放时间],[大汽车,投放号段,投放时间]}


class Spider:
    def __init__(self, url):
        self.url = url
        self.firefox = webdriver.Firefox()
        self.firefox.implicitly_wait(10)
        try:
            # options = webdriver.FirefoxOptions()
            # options.add_argument('-headless')
            # firefox = webdriver.Firefox(options=options)
            # print("浏览器打开")
            self.firefox.get(self.url)
            soup = BeautifulSoup(self.firefox.page_source, 'lxml')
            author_list = soup.find('select', id='glbm').contents
            for option_tag in author_list:
                author_value = option_tag.get('value')
                Select(self.firefox.find_element_by_xpath('//*[@id="glbm"]')).select_by_value(author_value)
                soup2 = BeautifulSoup(self.firefox.page_source, 'lxml')
                sort_list = soup2.find('select', id='hpzl').contents
                for option_tag2 in sort_list:
                    sort_num = option_tag2.get('value')
                    Select(self.firefox.find_element_by_xpath('//*[@id="hpzl"]')).select_by_value(sort_num)
                    data_html = self.send_request(author_value, sort_num)
                    data_ob = self.html_parser(data_html)
                    print(data_ob)
        finally:
            self.firefox.close()

    def html_parser(self, source):
        soup = BeautifulSoup(source, 'lxml')
        latest_info = soup.find('table', class_='table table-striped').find('tbody').find('tr').contents
        while ' ' in latest_info:
            latest_info.remove(' ')
        if latest_info[0].get_text() == '暂无数据':
            return '暂无数据'
        dataob = DataOB(latest_info[0].get_text(), latest_info[1].get_text().strip(), latest_info[2].get_text(),
                        latest_info[3].get_text())
        return dataob

    def check_alert(self):
        try:
            alert = self.firefox.switch_to.alert
            return True
        except Exception:
            return False

    def send_request(self,author_num, sort_num):
        # 保存当前循环的状态信息
        author_num = author_num
        sort_num = sort_num
        Select(self.firefox.find_element_by_xpath('//*[@id="glbm"]')).select_by_value(author_num)
        Select(self.firefox.find_element_by_xpath('//*[@id="hpzl"]')).select_by_value(sort_num)
        # 找到查询的按钮点一下
        self.firefox.find_element_by_xpath("//*[@id='formsearch']/div[2]/div[4]").click()
        # 判断是不是滑动验证
        try:
            self.firefox.find_element_by_xpath('//*[@id="nc_1__scale_text"]/span')
            self.firefox.close()
            self.firefox = webdriver.Firefox()
            self.firefox.implicitly_wait(1000)
            self.firefox.get(self.url)
            return self.send_request(author_num, sort_num)
        except Exception:
            pass
        # 等待验证码加载出来
        captcha_image = self.firefox.find_element_by_xpath(
            "/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td[2]/div/span/img")
        captcha_image.screenshot("/Users/luxness/Desktop/test.png")
        # captcha_result = fateadm_api.TestFunc()
        input_box = self.firefox.find_element_by_xpath("//*[@id='csessionid']")
        input_box.send_keys('1')
        sure_butt = self.firefox.find_element_by_xpath(
            "/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button[1]")
        sure_butt.click()
        # 判断alert框是否出现
        if self.check_alert():
            Alert(self.firefox).accept()
            return self.send_request(author_num, sort_num)
        return self.firefox.page_source

'''
测试的函数，不用管
'''
def get_instance():
    firefox = webdriver.Firefox()
    firefox.implicitly_wait(20)
    firefox.get('http://bj.122.gov.cn/views/vehxhhdpub.html')
    firefox.quit()


def test():
    pass


if __name__ == "__main__":
    get_instance()