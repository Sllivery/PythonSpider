import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import time


def get_one_page(url):
    try:
        response = requests.get(url, headers={'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'})
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def get_html_target(html):
    soup = BeautifulSoup(html,'lxml')
    target_div = soup.find_all('dd')
    for single_target in target_div:
        movie_index = single_target.find('i').get_text().strip()
        movie_img = single_target.find('img', class_='board-img')['data-src']
        movie_name = single_target.find('p',class_='name').a['title'] #or single_target.find('a').get('title')
                                                    #就是获取一个标签属性可以用中括号，或者用get方法
        movie_actors = single_target.find('p', attrs={'class': 'star'}).get_text().strip()
        movie_time = single_target.find('p', attrs={'class': 'releasetime'}).get_text().strip()
        score_integer = single_target.find(class_='integer').get_text().strip()
        score_fraction = single_target.find(class_='fraction').get_text().strip()
        full_score = score_integer + score_fraction
        yield {
            '排名':movie_index,
            '图片地址':movie_img,
            '电影名':movie_name,
            '主演':movie_actors,
            '上映时间':movie_time,
            '电影评分':full_score
        }


def write_to_file(content):
    for item in content:
        with open('猫眼Top100', 'a', encoding='utf-8') as f:
            f.write(str(item) + '\n')
            f.close()



def main(offset):
    url = 'http://www.maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    content = get_html_target(html)
    write_to_file(content)


if __name__ == "__main__":
    for i in range(10):
        main(i*10)
        time.sleep(1)
    print("program complete")