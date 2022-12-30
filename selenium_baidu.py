# -*- coding:utf-8 -*-
'''
================================================
    file_name:      selenium_baidu
    Description:
    Author:         gpr
    Date:           2022/12/20
============================================
'''
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
#import xlwt
from selenium.webdriver.chrome.options import Options

#browser = webdriver.PhantomJS()
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('blink-settings=imagesEnabled=false')
chrome_options.add_argument('User-Agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 ')

browser = webdriver.Chrome(options=chrome_options)
WAIT = WebDriverWait(browser, 10)
def test():
    #打开浏览器
    try:
        browser.get('https://www.baidu.com')
        print("begin open baidu")
        #显示等待

        input = WAIT.until(EC.presence_of_element_located((By.XPATH, '//*[@id="kw"]')))
        submit = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="su"]')))

        input.send_keys('蔡徐坤 篮球')
        submit.click()
        #browser.implicit_wait(10) #等10秒，如果解释完页面，就会自动执行下面的，不一定要10秒，此为一个非固定的值
        #wait = WebDriverWait(browser, 10)  #这个很重要，否则就爬不到内容了
        total = WAIT.until(EC.presence_of_element_located((By.XPATH, '//*[@id="page"]/div/a[9]/span')))
        print(int(total.text))
        print(browser.current_url)
        print(browser.get_cookies())


        soup = BeautifulSoup(browser.page_source, 'lxml')

        list = soup.find_all('div', class_=re.compile("result"))
        print("result_len :{} ,type: {}".format(len(list),  type(list)))
            #.find_all(class_='result c-container new-pmd')

        for item in list:

            item_node = item.find('a')
            if item_node:
                item_node = item_node.find(target="_blank")
                item_link = item.find('a').get('href')
                item_title = item.find('a').get_text()
                if item_title and re.match(r'http://www.baidu.com',item_link):
                    print('爬取：{} {}'.format( item_title, item_link))


    except TimeoutException:
        return test()

def main():
    try:
        total = test()
    finally:
        browser.close()

if __name__ == '__main__':
    main()