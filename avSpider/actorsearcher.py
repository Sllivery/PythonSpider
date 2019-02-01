import requests
import os
from bs4 import BeautifulSoup
import urllib.request
import ssl
import time
import re


ssl._create_default_https_context = ssl._create_unverified_context


class GetOuterPage:
    def __init__(self, url):
        self.url = url
        self.av_amount = 0
        self.headers = {'User-Agent':
                        'Mozilla/5.0 (Macintosh; '
                        'Intel Mac OS X 10_13_6) '
                        'AppleWebKit/537.36 (KHTML, '
                        'like Gecko) Chrome/68.0.3440.106 '
                        'Safari/537.36'
                        }

    def force_one_by_one(self, url_f, begin, end):
        bango_dict = {}
        for i in range(begin, end + 1):
            print('正在爬取第 ' + str(i) + '页')
            response = requests.get(url_f + '&page=' + str(i), headers=self.headers)
            soup = BeautifulSoup(response.text, 'lxml')
            lists = soup.find_all(class_='video')
            for list_ in lists:
                part = list_.find('a').get('href')
                full = part.replace('.', 'http://www.d21b.com/cn')
                inner = requests.get(full, self.headers)
                inner_soup = BeautifulSoup(inner.text, 'lxml')
                id_ = inner_soup.find('div', id='video_id').find(class_='text').get_text()
                time_ = inner_soup.find('div', id='video_date').find(class_='text').get_text()
                pic_url = 'http:' + inner_soup.find('img', id='video_jacket_img').get('src')
                bango_dict[pic_url] = (id_, time_)
        return bango_dict

    def get_one_page(self, begin_num, end_num):
        soup_list = []
        for i in range(begin_num, end_num + 1):
            print('正在爬取' + str(i) + '页')
            response = requests.get(self.url + '&page=' + str(i), headers=self.headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                bango_list = soup.find_all(class_='video')
                for bango in bango_list:
                    soup_list.append(bango)
        return soup_list

    def get_inner_page(self, full_next_url):
        inner_response = requests.get(full_next_url, headers=self.headers)
        soup = BeautifulSoup(inner_response.text, 'lxml')
        return soup

    @staticmethod
    def download_pic(av_bango_dict, dir_name):
        amount = 0
        print('=====一共有' + str(len(av_bango_dict)) + '张=====')
        if not dir_name.startswith('/'):
            raise TypeError('请以  / + 文件夹名  命名')
        now_path = os.getcwd()
        if not os.path.exists(now_path + dir_name):
                os.mkdir(now_path + dir_name)
        for each_bango in av_bango_dict:
            filename = now_path + dir_name + '/' + each_bango
            urllib.request.urlretrieve(av_bango_dict[each_bango], filename + '.jpg')
            amount += 1
            print('第' + str(amount) + '张')

    @staticmethod
    def force_download(av_dict, dir_name):
        amount = 0
        print('=====一共有' + str(len(av_dict)) + '张=====')
        if not dir_name.startswith('/'):
            raise TypeError('请以  / + 文件夹名  命名')
        now_path = os.getcwd()
        if not os.path.exists(now_path + dir_name):
            os.mkdir(now_path + dir_name)
        for each_url in av_dict:
            filename = now_path + dir_name + '/' + " ".join(av_dict[each_url])
            urllib.request.urlretrieve(each_url, filename + '.jpg')
            amount += 1
            print('第' + str(amount) + '张')


class GetVRPage(GetOuterPage):
    def get_vr_info(self):
        bango_list = self.get_one_page()
        for vr_bango in bango_list:
            target_bango = vr_bango.find(class_='id').get_text()
            if target_bango:
                self.av_amount += 1
            if 'VR' in target_bango:
                part_url = vr_bango.find('a').get('href')
                full_next_url = part_url.replace('.', 'http://www.d21b.com/cn')
                soup = self.get_inner_page(full_next_url)
                pic_src = soup.find('img', id='video_jacket_img').get('src')


class BaseCategorySearcher(GetOuterPage):
    def get_category_info(self, begin, end, categroy):
        av_bango_dict = {}
        bango_list = self.get_one_page(begin, end)
        print('====一共有' + str(len(bango_list)) + '部片====')
        for i, each_bango in enumerate(bango_list):
            print('正在解析第' + str(i) + '部影片')
            tag_list = []
            part_url = each_bango.find('a').get('href')
            full_next_url = part_url.replace('.', 'http://www.d21b.com/cn')
            soup = self.get_inner_page(full_next_url)
            span_list = soup.find_all('span', class_='genre')
            for category_tag in span_list:
                tag_content = category_tag.find('a').get_text()
                tag_list.append(tag_content)
            if categroy in tag_list:
                pic_url = 'http:' + soup.find('img', id='video_jacket_img').get('src')
                time_ = soup.find('div', id='video_date').find(class_='text').get_text()
                av_bango = soup.find('div', id='video_id').find(class_='text').get_text()
                av_bango_dict[pic_url] = (av_bango, time_)
        return av_bango_dict


class BaseNameSearcher(GetOuterPage):
    def get_schoolstocking_info(self, begin, end, keyword):
        av_bango_dir = {}
        soup_list = self.get_one_page(begin, end)
        for each_bango in soup_list:
            av_title = each_bango.find('div', class_='title').get_text()
            if keyword in av_title:
                    part_url = each_bango.find('a').get('href')
                    full_next_url = part_url.replace('.', 'http://www.d21b.com/cn')
                    soup = self.get_inner_page(full_next_url)
                    time_ = soup.find('div', id='video_date').find(class_='text').get_text()
                    av_bango = soup.find('div', id='video_id').find(class_='text').get_text()
                    pic_url = 'http:' + soup.find('img', id='video_jacket_img').get('src')
                    av_bango_dir[pic_url] = (av_bango, time_)
        return av_bango_dir


if __name__ == '__main__':
    '''初始功能 测试用'''
    # url = 'http://www.d21b.com/cn/vl_genre.php?&mode=&g=aqda'
    # school = BaseNameSearcher(url)
    # bango = school.get_schoolstocking_info(1, 30)
    # GetOuterPage.download_pic(bango, '/美脚系列')

    # '''爬取全部'''
    # url = 'http://www.d21b.com/cn/vl_genre.php?&mode=2&g=i4'
    # force_spider = GetOuterPage(url)
    # test = force_spider.force_one_by_one(url, 1, 30)
    # GetOuterPage.force_download(test, '/教师AV')

    '''基于片名字符搜索'''
    # url = 'http://www.d21b.com/cn/vl_star.php?s=azbay'
    # name_searcher = BaseNameSearcher(url)
    # bango_dict = name_searcher.get_schoolstocking_info(1, 5, 'VR')
    # GetOuterPage.force_download(bango_dict, '/旬果VR')

    '''基于影片分类搜索'''
    # url = 'http://www.d21b.com/cn/vl_star.php?&mode=2&s=amka'
    # cate_searcher = BaseCategorySearcher(url)
    # bango_info = cate_searcher.get_category_info(1, 30, 'VR')
    # GetOuterPage.force_download(bango_info, '/篠田VR')



