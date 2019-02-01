import time
import fateadm_api
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from PIL import Image
from selenium.webdriver.common.keys import Keys


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
    chrome = webdriver.Chrome()
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
        location = (1120, 316, 1120+175, 316+58)
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


if __name__ == "__main__":
    get_captcha()
