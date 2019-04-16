import time
import datetime
import fateadm_api
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
from entity.DataEntity import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import *
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 记录中断时的信息
termination_info = TerminationStatusRecord("", "", "")
# 记录重试次数，如果大于5次，跳过本次车辆种类
termination_time = 0
# 最新记录
latest_record = {}
# 前_最新记录
pre_record = {}


def notify(receiver_list, source_data, method=2):
    """
    定制提醒的方法
    receiver_list: 收件人列表
    source_data: 源数据，没有经过格式化
    method: 提醒方法，1 = 短信， 2 = 邮箱， 默认为2
    :return:
    """

    if method == 1:
        send_text = SendNew(receiver_list, source_data)
        send_text.send_text()
    if method == 2:
        send_email = SendNew(receiver_list, source_data)
        send_email.send_email()


def pipeline(receiver_list):
    """
        在每次循环之后，数据的处理
        send_data是作为一个容器，存放latest_record在pre_record里筛选后得到的最新数据
    """
    global pre_record
    global latest_record
    send_data = {}
    if pre_record:
        termination_info.url = ""
        termination_info.author_num = ""
        termination_info.sort_num = ""
        for single_latest_record in latest_record:
            if not (single_latest_record in pre_record):
                send_data[single_latest_record] = latest_record[single_latest_record]
            if single_latest_record in pre_record:
                latest_time = datetime.datetime.strptime(latest_record[single_latest_record][1],
                                                         '%Y-%m-%d %H:%M')
                pre_time = datetime.datetime.strptime(pre_record[single_latest_record][1],
                                                      '%Y-%m-%d %H:%M')
                if latest_time > pre_time:
                    send_data[single_latest_record] = latest_record[single_latest_record]
        if send_data:
            pre_record = latest_record
            notify(receiver_list, send_data)

    if not pre_record:
        termination_info.url = ""
        termination_info.author_num = ""
        termination_info.sort_num = ""
        if latest_record:
            notify(receiver_list, latest_record)
        pre_record = latest_record


class SendNew:
    """
    调用send_text或者send_email时
    发送的self.message是格式化过的

    e.g:
    城市名 车管所名 汽车类型 牌照范围 时间 \n <- 换行符
    ...
    """
    def __init__(self, receiver_list, source_data):
        self.receiver = receiver_list
        self.message = ""
        self.process_message(source_data)

    def process_message(self, source_data):
        for single_data in source_data:
            head = ' '.join(single_data)
            content = ' '.join(source_data[single_data])
            single_full_m = head + ' ' + content + '\n'
            self.message = self.message + single_full_m

    def send_text(self):
        """
        发送短信的方法
        :return:
        """
        pass

    def send_email(self):
        """
        发送邮件的方法
        :return:
        """
        host_server = 'smtp.163.com'
        sender_qq = 'reminder2019@163.com'
        pwd = 'youxiang1'
        sender_qq_mail = 'reminder2019@163.com'
        receivers = self.receiver
        mail_content = self.message
        # 邮件标题
        mail_title = '牌照放号提醒'

        # ssl登录
        smtp = SMTP_SSL(host_server)
        smtp.set_debuglevel(1)
        smtp.ehlo(host_server)
        smtp.login(sender_qq, pwd)

        msg = MIMEText(mail_content, "plain", 'utf-8')
        msg["Subject"] = Header(mail_title, 'utf-8')
        msg["From"] = sender_qq_mail
        if len(receivers) > 1:
            msg["To"] = ','.join(receivers)
        else:
            msg["To"] = receivers[0]
        smtp.sendmail(sender_qq_mail, receivers, msg.as_string())
        smtp.quit()


class SpiderSchedule:
    """
    爬虫调度器
    根据队列中的url来循环或者选取url来给爬虫用
    """
    def __init__(self, receiver_list):
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')
        self.firefox = webdriver.Firefox()
        self.firefox.implicitly_wait(10)
        self.receiver_list = receiver_list
        self.list = [
            'http://bj.122.gov.cn/views/vehxhhdpub.html',
            'http://tj.122.gov.cn/views/vehxhhdpub.html',
            'http://he.122.gov.cn/views/vehxhhdpub.html',
            'https://sx.122.gov.cn/views/vehxhhdpub.html',
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
        """
        发生中断时，能够接着上次中断的url接着爬取
        :return:
        """
        global termination_info
        if termination_info.url == "":
            return self.list
        if termination_info.url != "":
            new_list = self.list[self.list.index(termination_info.url):]
            return new_list

    def run_spider(self):
        """
        迭代全国交警url，交给Spider处理
        :return:
        """
        global termination_time
        global pre_record
        global latest_record
        while True:
            try:
                # 在这里迭代
                for url in self.__get_right_list():
                        Spider(url, termination_info.author_num, termination_info.sort_num, self.firefox)
            except Exception as e:
                print(e)
                pass
            else:
                # 每次循环结束后，进入这里处理数据
                # 传一个空列表是因为在
                print('循环一次')
                pipeline(self.receiver_list)


class Spider:
    def __init__(self, url, t_author_num, t_sort_num, firefox):
        """
        :param url: 当前城市的url
        :param t_author_num: 如果中断，记录中断时车管所名字
        :param t_sort_num: 记录中断时汽车类型
        :param firefox: 浏览器对象
        """
        global termination_info
        global termination_time
        global latest_record
        self.url = url
        self.city_name = ""
        self.t_author_num = t_author_num
        self.t_sort_num = t_sort_num
        self.firefox = firefox
        self.firefox.get(self.url)
        termination_info.url = self.url
        self.firefox.find_element_by_xpath('//*[@id="hpzl"]/option[1]')
        soup = BeautifulSoup(self.firefox.page_source, 'lxml')

        # 得到这个省/城市的车管所的标签列表
        author_tag_list = soup.find('select', id='glbm').contents
        author_list = []

        # 这个循环从每个标签提取车管所名字，并判断前面是否有中断，如果有中断，生成新的车管所列表。之前爬过的不要了
        for author_tag in author_tag_list:
            author_list.append(author_tag.get_text())
        if termination_info.author_num != "":
            try:
                author_list = author_list[author_list.index(termination_info.author_num):]
            except ValueError as e:
                author_list = author_list

        # 得到当前省/城市名
        self.city_name = soup.find('span', class_='header-logo-top fL').get_text()[0:2]

        # 在车管所、汽车型号循环里，迭代爬取信息
        for option in author_list:
            termination_info.author_num = option
            Select(self.firefox.find_element_by_xpath('//*[@id="glbm"]')).select_by_visible_text(option)
            soup2 = BeautifulSoup(self.firefox.page_source, 'lxml')
            sort_list = soup2.find('select', id='hpzl').contents
            sort_content = []
            for sort_tag in sort_list:
                sort_content.append(sort_tag.get_text())
            if termination_info.sort_num != "":
                try:
                    sort_content = sort_content[sort_content.index(termination_info.sort_num):]
                except ValueError as e:
                    sort_content = sort_content
            for option_tag2 in sort_content:
                termination_info.sort_num = option_tag2
                Select(self.firefox.find_element_by_xpath('//*[@id="hpzl"]')).select_by_visible_text(option_tag2)
                data_html = self.send_request(option, option_tag2)
                data_ob = self.html_parser(data_html)
                if data_ob:
                    print(time.strftime('%Y-%m-%d', time.localtime()))
                    if data_ob.time[0:10] == time.strftime('%Y-%m-%d', time.localtime()):
                        latest_record[(data_ob.city_name, data_ob.author, data_ob.sort)] = [data_ob.num_range, data_ob.time]
                termination_info.sort_num = ""

    def send_request(self, author_num, sort_num):
        """

        :param author_num: 需要点击的车管所名字
        :param sort_num: 需要点击的汽车类型名字
        :return: 目标网页的html
        """
        if self.url == 'https://sx.122.gov.cn/views/vehxhhdpub.html':
            self.firefox.refresh()
        author_num = author_num
        sort_num = sort_num
        Select(self.firefox.find_element_by_xpath('//*[@id="glbm"]')).select_by_visible_text(author_num)
        Select(self.firefox.find_element_by_xpath('//*[@id="hpzl"]')).select_by_visible_text(sort_num)
        # 找到查询的按钮点一下
        search_butt = self.firefox.find_element_by_xpath('//*[@id="formsearch"]/div[2]/div[4]')
        search_butt.click()
        try:
            captcha_image = self.firefox.find_element_by_xpath("/html/body/div[1]/div/table/tbod"
                                                               "y/tr[2]/td[2]/div/table/tbody/tr[2]/td[2]/div/span/img")
            time.sleep(1)
            captcha_image.screenshot("/root/test.png")
        except NoSuchElementException as e:
            self.firefox.delete_all_cookies()
            self.firefox.refresh()
            return self.send_request(author_num, sort_num)
        captcha_result = fateadm_api.TestFunc()
        input_box = self.firefox.find_element_by_xpath("//*[@id='csessionid']")
        input_box.send_keys(captcha_result)
        # 找到确定按钮
        sure_butt = self.firefox.find_element_by_xpath(
            "/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button[1]")
        sure_butt.click()
        time.sleep(0.6)
        # 判断是否出现Alert
        if self.check_alert():
            self.check_alert().accept()
            # 停顿3s,防止请求过多出现滑动验证
            time.sleep(3)
            return self.send_request(author_num, sort_num)
        # 网站的反爬虫是通过cookie的，每次请求完要清除一下cookie，就只会出现验证码
        self.firefox.delete_all_cookies()
        return self.firefox.page_source

    def html_parser(self, source):
        """
        用beautifulsoup解析页面，提取数据
        :param source: 目标网页的html
        :return: DataOB对象，保存着提取的数据
        """
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
        """
        有时候验证码识别错误，弹出一个alert
        这个函数来处理这个alert
        :return:
        """
        try:
            alert = self.firefox.switch_to.alert
            return alert
        except Exception:
            return False


if __name__ == "__main__":
    # new SpiderSchedule时，要传入收信人的列表
    spider = SpiderSchedule(['luxness.int@gmail.com'])
    spider.run_spider()

