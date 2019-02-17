import time
import fateadm_api
from entity.DataEntity import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import *
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 记录中断时的信息
termination_info = TerminationStatusRecord("", "", "")
# 记录重试次数，如果大于5次，跳过本次车辆种类
termination_time = 0

class SpiderSchedule:
    """
    爬虫调度器
    根据队列中的url来循环或者选取url来给爬虫用
    """
    def __init__(self):
        self.firefox = webdriver.Firefox()
        self.firefox.implicitly_wait(3)
        self.list = [
            # 'http://bj.122.gov.cn/views/vehxhhdpub.html',
            # 'http://tj.122.gov.cn/views/vehxhhdpub.html',
            # 'http://he.122.gov.cn/views/vehxhhdpub.html',
            'http://sx.122.gov.cn/views/vehxhhdpub.html',
            'http://nm.122.gov.cn/views/vehxhhdpub.html',
            'http://ln.122.gov.cn/views/vehxhhdpub.html',
            'http://hl.122.gov.cn/views/vehxhhdpub.html',
            'http://sh.122.gov.cn/views/vehxhhdpub.html',
            'http://nkg.122.gov.cn/views/vehxhhdpub.html',
            'http://wux.122.gov.cn/views/vehxhhdpub.html',
            'http://xuz.122.gov.cn/views/vehxhhdpub.html',
            'http://czx.122.gov.cn/views/vehxhhdpub.html',
            'http://szv.122.gov.cn/views/vehxhhdpub.html',
            'http://ntg.122.gov.cn/views/vehxhhdpub.html',
            'http://lyg.122.gov.cn/views/vehxhhdpub.html',
            'http://has.122.gov.cn/views/vehxhhdpub.html',
            'http://ynz.122.gov.cn/views/vehxhhdpub.html',
            'http://yzo.122.gov.cn/views/vehxhhdpub.html',
            'http://zhe.122.gov.cn/views/vehxhhdpub.html',
            'http://tzs.122.gov.cn/views/vehxhhdpub.html',
            'http://suq.122.gov.cn/views/vehxhhdpub.html',
            'http://hgh.122.gov.cn/views/vehxhhdpub.html',
            'http://ngb.122.gov.cn/views/vehxhhdpub.html',
            'http://wnz.122.gov.cn/views/vehxhhdpub.html',
            'http://jix.122.gov.cn/views/vehxhhdpub.html',
            'http://hzh.122.gov.cn/views/vehxhhdpub.html',
            'http://sxg.122.gov.cn/views/vehxhhdpub.html',
            'http://jha.122.gov.cn/views/vehxhhdpub.html',
            'http://quz.122.gov.cn/views/vehxhhdpub.html',
            'http://zos.122.gov.cn/views/vehxhhdpub.html',
            'http://tzz.122.gov.cn/views/vehxhhdpub.html',
            'http://lss.122.gov.cn/views/vehxhhdpub.html',
            'http://ah.122.gov.cn/views/vehxhhdpub.html',
            'http://fj.122.gov.cn/views/vehxhhdpub.html',
            'http://jx.122.gov.cn/views/vehxhhdpub.html',
            'http://sd.122.gov.cn/views/vehxhhdpub.html',
            'http://ha.122.gov.cn/views/vehxhhdpub.html',
            'http://hb.122.gov.cn/views/vehxhhdpub.html',
            'http://hn.122.gov.cn/views/vehxhhdpub.html',
            'http://gd.122.gov.cn/views/vehxhhdpub.html',
            'http://gx.122.gov.cn/views/vehxhhdpub.html',
            'http://hi.122.gov.cn/views/vehxhhdpub.html',
            'http://cq.122.gov.cn/views/vehxhhdpub.html',
            'http://sc.122.gov.cn/views/vehxhhdpub.html',
            'http://gz.122.gov.cn/views/vehxhhdpub.html',
            'http://yn.122.gov.cn/views/vehxhhdpub.html',
            'http://xz.122.gov.cn/views/vehxhhdpub.html',
            'http://sn.122.gov.cn/views/vehxhhdpub.html',
            'http://gs.122.gov.cn/views/vehxhhdpub.html',
            'http://qh.122.gov.cn/views/vehxhhdpub.html',
            'http://nx.122.gov.cn/views/vehxhhdpub.html',
            'http://xj.122.gov.cn/views/vehxhhdpub.html'
        ]

    def __get_right_list(self):
        global termination_info
        if termination_info.url == "":
            return self.list
        if termination_info.url != "":
            new_list = self.list[self.list.index(termination_info.url):len(self.list)]
            return new_list

    def run_spider(self):
        global termination_time
        while True:
            try:
                for url in self.__get_right_list():
                        Spider(url, termination_info.author_num, termination_info.sort_num, self.firefox)
            except Exception as e:
                termination_time += 1
                print(e)
            else:
                print("列表抓取完毕，等待60秒重新开始")
                termination_info.url = ""
                termination_info.author_num = ""
                termination_info.sort_num = ""
                time.sleep(60)


class Spider:
    def __init__(self, url, t_author_num, t_sort_num, firefox):
        global termination_info
        global termination_time
        self.url = url
        self.city_name = ""
        self.t_author_num = t_author_num
        self.t_sort_num = t_sort_num
        self.firefox = firefox
        self.firefox.get(self.url)
        termination_info.url = self.url
        try:
            self.firefox.find_element_by_xpath('//*[@id="hpzl"]/option[1]')
        except NoSuchElementException:
            self.firefox.find_element_by_xpath('//*[@id="hpzl"]/option')
        soup = BeautifulSoup(self.firefox.page_source, 'lxml')
        author_tag_list = soup.find('select', id='glbm').contents
        author_list = []
        for author_tag in author_tag_list:
            author_list.append(author_tag.get('value'))
        if termination_info.author_num != "":
            try:
                author_list = author_list[author_list.index(termination_info.author_num):len(author_list)]
            except ValueError as e:
                author_list = author_list
        # 这里加个bs4 find城市名,给self.city_name
        self.city_name = soup.find('span', class_='header-logo-top fL').get_text()[0:2]
        for option in author_list:
            termination_info.author_num = option
            author_value = option
            Select(self.firefox.find_element_by_xpath('//*[@id="glbm"]')).select_by_value(author_value)
            soup2 = BeautifulSoup(self.firefox.page_source, 'lxml')
            sort_list = soup2.find('select', id='hpzl').contents
            for option_tag2 in sort_list:
                sort_num = option_tag2.get('value')
                termination_info.sort_num = sort_num
                Select(self.firefox.find_element_by_xpath('//*[@id="hpzl"]')).select_by_value(sort_num)
                data_html = self.send_request(author_value, sort_num)
                data_ob = self.html_parser(data_html)

    def send_request(self,author_num, sort_num):
        # 保存当前循环的状态信息
        self.firefox.delete_all_cookies()
        author_num = author_num
        sort_num = sort_num
        Select(self.firefox.find_element_by_xpath('//*[@id="glbm"]')).select_by_value(author_num)
        Select(self.firefox.find_element_by_xpath('//*[@id="hpzl"]')).select_by_value(sort_num)
        # 找到查询的按钮点一下
        self.firefox.find_element_by_xpath("//*[@id='formsearch']/div[2]/div[4]").click()
        captcha_image = self.firefox.find_element_by_xpath(
            "/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td[2]/div/span/img")
        time.sleep(0.5)
        captcha_image.screenshot("/Users/luxness/Desktop/test.png")
        # while test.png == failed.png:
        #     # 点击刷新，截图，记录次数，>5次
        captcha_result = fateadm_api.TestFunc()
        input_box = self.firefox.find_element_by_xpath("//*[@id='csessionid']")
        input_box.send_keys(captcha_result)
        # 找到确定按钮
        sure_butt = self.firefox.find_element_by_xpath(
            "/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button[1]")
        sure_butt.click()
        # 判断是否出现Alert
        if self.check_alert():
            self.check_alert().accept()
            # 停顿0.5让页面黑幕div消失
            time.sleep(0.5)
            return self.send_request(author_num, sort_num)
        time.sleep(1)
        self.firefox.delete_all_cookies()
        return self.firefox.page_source

    def html_parser(self, source):
        soup = BeautifulSoup(source, 'lxml')
        latest_info = soup.find('table', class_='table table-striped').find('tbody').find('tr').contents
        while ' ' in latest_info:
            latest_info.remove(' ')
        if latest_info[0].get_text() == '暂无数据':
            return None
        dataob = DataOB(self.city_name, latest_info[0].get_text(), latest_info[1].get_text().strip(), latest_info[2].get_text(),
                        latest_info[3].get_text())
        print(dataob)
        return dataob

    def check_alert(self):
        try:
            alert = self.firefox.switch_to.alert
            return alert
        except Exception:
            return False


'''
测试的函数，不用管
'''
def get_instance():
    pass


def test():
    list1 = ["hey", "you"]
    print(list1.index("you"))


if __name__ == "__main__":
    spider = SpiderSchedule()
    spider.run_spider()
    # test()

