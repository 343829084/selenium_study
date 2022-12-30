# -*- coding:utf-8 -*-
'''
================================================
    file_name:      multi_process get data
    Description:
    Author:         gpr
    Date:           2022/12/21
============================================
'''
from lxml import etree
from multiprocessing import Pool
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import wget
import os
import re

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('blink-settings=imagesEnabled=false')
chrome_options.add_argument('User-Agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 ')
chrome_options.add_argument('Cookie=_uab_collina=165787356227684108331801; _ga=GA1.2.137805932.1621932895; __yadk_uid=c7XWXGObaTnEw5o6l71nlvgRGZi53wZe; UM_distinctid=1819ef2c3c94e3-0a5c99301962fe-c4f7526-e1000-1819ef2c3cab6c; __bid_n=1843caffb20f7d61544207; FPTOKEN=30$lWR1oc8e8I9/MV7aSXgVRmf9jLbmUwAif6wSxGQLnQXwxUYC2P5K0TgU1K2D6Uv2E7u5ts6eqGQk6U/gvit4i3hyQJrG7+9KQRMl3eiMUs53VCa35feQZV2x5w/UV4fNRpC5RsnqjdoPsUTT15QhynCjPdGvM6Nl4JMdwLw4j7+E2W5SY56RXmWkVGY31fhdXg4R4oJjhF2FnZ1r8zfv5xcY1sVmf8x3LDOeWOHQ9naPGE4jT1at4FuQyOI+Clcs87Yvcc7k2+i/DbS4xkpzyzw6utq4O4oQz0M+hgrUC3a2VQ3bQKifqReRNcmXssk9SAUm5rof6V/yi2mdfAxGhOLjKBvyG3ChRd2z27O/gwoT/VRRvc+NvIrmZwI3lCcA|fdDNIIV11d7pc/4VOeWQv/051ob3Kr9uBbsKDtBrdMc=|10|27fa18cec1d62015c35ad75c268896b2; ssxmod_itna=QqmxnDyD2QDtqDKGHKpWxjxwQ7i=oz7rWDgCx0v+veGzDAxn40iDtoPknQrDrBxEx4WD5Ch0tWYSE4oe+YK/C+PDHxY=DUaibqoD4fKGwD0eG+DD4DWDmWFDnxAQDjxGPnUpNH=DEDm48DWPDYxDrAoKDRxi7DDydHx07DQ58Pza+2PgkqWA43GKD9=oDsgxEiGFwpz3eya7vsS53+x0kc40OuP5zOPoDUjFzngve5GRxb0wHzARD3nioKD2D77DPsFD4Fq2e4rioiB2Dz0+PWEQDiEwRHYD; ssxmod_itna2=QqmxnDyD2QDtqDKGHKpWxjxwQ7i=oz7rWDgDn9EYeDsPKDL0ADXR4xqn4hlDLrwz28G20=7o0Gm02b0KB2qdzOmhB7aPHEr7Gcwe4IhP6xnnznTEGr/CC0SvLZhq5xIBG5mDwLB9xTH5pq==QBO3Cet37YhSipWVgP8b3qKqbpsN/cs2igIwZ5N50+wDFbElmwvHgB+6bqGh4uLpKdaH8y1cePOcG0TK2wbwE3UUAqLjBhtDNKugBe8trY2HEntWOAHMQgp7s0HDTAnHFctQwFQgijWxh/HGVSoDQFdDjKD+xhDD; CNZZDATA1279807957=2039719285-1621931300-https%3A%2F%2Fwww.baidu.com%2F|1669008145; Hm_lvt_1c6cd6a9fd5f687d8040b44bebe5d395=1667465479,1669011587; read_mode=day; default_font=font2; locale=zh-CN; _m7e_session_core=91d7d157c3a669879896573d2a87c68e; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1671178213,1671458694,1671506308,1671777426; sensorsdata2015jssdkcross={"distinct_id":"179a2bbea88558-0979aec337de53-38654702-921600-179a2bbea89878","first_id":"","props":{"$latest_traffic_source_type":"直接流量","$latest_search_keyword":"未取到值_直接打开","$latest_referrer":"","$latest_utm_source":"recommendation","$latest_utm_medium":"seo_notes","$latest_utm_campaign":"maleskine","$latest_utm_content":"note"},"$device_id":"179a2bbea88558-0979aec337de53-38654702-921600-179a2bbea89878"}; FEID=v10-b97a818be2b4eb836f4f08a64ec540c0dd6e9c99; __xaf_fpstarttimer__=1671777426625; SL_G_WPT_TO=zh-CN; __xaf_ths__={"data":{"0":1,"1":43200,"2":60},"id":"3c55040f-4b10-416a-a04c-acbe46c4b80d"}; __xaf_thstime__=1671777427139; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; FPTOKEN=tfM2oKC04gUMbB5HNU21NYbD6qNkpkYJGEFDr7siEUqSokgX0d3tUWh4y/23Wp+FDYi0CRqIj3iYtLbtaqjgOHM5ShsB+QEHOja/B6PmK6VMOeB2boxSM9XCoytlxArTakyRew8Q/LarXlxFD4893VWd7rrKfJHQL3lRIfm5Rj4/Dfa8XbGE+kvMYMCw9PlVvM9HuEN5wQI9p7YUu7lPtXGVY97kqDuucRO3qBI9/Z9JkuvFhHl5CO8avL9lypvFsxxZVk/1DLGIR53Gq4vn7NvQDbIoD+Ls3+0jdkdF7Hbxf1u9s7BQeY7V63TjbHeVrCCwvGFD72gbTgRGZ2KNQ/QTgAuqJz+Jh+ZelQAVOox4rZXAHxhKwbidY154at4dAkYKTIcOR6YVqjGncYyPdQ==|nwyK7zgAdJbBCCfjyjLWQoQ+4uCI/mztjB2ouTjgko8=|10|b606817a39494acbeec5ca736e8df45e; __xaf_fptokentimer__=1671777427264; Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1671777469; signin_redirect=https://www.jianshu.com/c/bDHhpK')
browser = webdriver.Chrome(options=chrome_options)
WAIT = WebDriverWait(browser, 10)


def beautiful_decode(url):
    #用beautiful来解网页， 打开浏览器
    browser.get(url)
    print("begin open ", url)
    wait = WebDriverWait(browser, 10)  # 这个很重要，否则就爬不到内容了
    #print(browser.page_source)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    infos = soup.find_all('div', class_="content")
    #print("type:{} len {}".format(type(infos), len(infos)))
    for info in infos:
        author = info.find('a').get_text()
        print('{}'.format(author))


def lxml_decode(url):
    #用lxml来解释网页，这个速度更快
    browser.get(url)
    print("begin open ", url)
    wait = WebDriverWait(browser, 10)  # 这个很重要，否则就爬不到内容了
    # print(browser.page_source)
    selector = etree.HTML(browser.page_source)
    infos = selector.xpath("//ul[@class='note-list']/li")
    print('{} len {}'.format(len(infos), type(infos)))

    for info in infos:
        author = info.xpath("div/a/text()")[0]   #text()显示content
        print('{}'.format(author))

def async_load_ajax():
    urls=['https://www.jianshu.com/u/9104ebf5e177?order_by=shared_at&page={}'.format(str(i)) for i in range(1,4) ]
    pool = Pool(processes=4)
    pool.map(lxml_decode, urls)

def selenium_load_ajax():
    #它的异步加载url为https://www.jianshu.com/u/9104ebf5e177?order_by=shared_at&page=，但是通过selenium模拟用户操作并不需要通过浏览器中的网络
    #逆向分析出它的异步加载url，也能进行解析
    urls = ['https://www.jianshu.com/u/9104ebf5e177']
    pool = Pool(processes=1)
    pool.map(lxml_decode, urls)

def load_four_grade_english_next_semester():
    # 下载7年级下册英语听力mp3,url地址有有效期的，所以需要到sogo中查新的ip
    media_url_path = "https://res.wx.qq.com/voice/getvoice?mediaid="
    url = "https://mp.weixin.qq.com/s?src=11&timestamp=1672285998&ver=4255&signature=YPPA5GfU7z2pUP49*E7a0-XJktQqDvtMfachpwJC8uLuEMMbKuJZxRgRUCQc2v9OVTLIxjXr*I5drG1n0ONgLu7ygyAImatzDB3LQizN51*QTnYeKTDPkCbcE-kShqdQ&new=1"
    browser.get(url)
    WebDriverWait(browser, 10)
    selector = etree.HTML(browser.page_source)
    # descendant::a 表示子孙中所有标签为a的
    links = selector.xpath('//*[@id="js_content"]/descendant::a/@href')
    print('{} len:{}'.format(len(links), links))

    for jump_url in links:
        browser.get(jump_url)
        # print(jump_url)
        WebDriverWait(browser, 10)
        selector = etree.HTML(browser.page_source)
        #WebDriverWait(browser, 10)
        file_node = WAIT.until(EC.presence_of_element_located((By.XPATH, '//*[@class="audio_card_title"]')))

        # file_name = selector.xpath('//*[@class="audio_card_title"]/text()')[0]
        file_name = file_node.text.replace(' ', '_')

        mediaid = selector.xpath('//mpvoice/@voice_encode_fileid')[0]
        print(file_name, mediaid)
        # mediaid_list = WAIT.until(EC.presence_of_element_located((By.XPATH, '//*[@id="js_content"]/p[3]/mpvoice"]')))
        # print(mediaid_list)
        # mediaid = mediaid_list.attr('voice_encode_fileid')

        media_url = f"{media_url_path}{mediaid}"
        file_name_path = os.path.join(os.getcwd(), file_name)
        # print(file_name_path)
        wget.download(media_url, file_name_path)
    browser.close()

def load_english_listening():
    #下载7年级下册英语听力mp3,url地址有有效期的，所以需要到sogo中查新的ip
    media_url_path = "https://res.wx.qq.com/voice/getvoice?mediaid="
    url="https://mp.weixin.qq.com/s?src=11&timestamp=1672278970&ver=4255&signature=YPPA5GfU7z2pUP49*E7a0-XJktQqDvtMfachpwJC8uIunD-7GcXTv1G-Hg6LmR0I5knaiS*8jDQzaco2pHlmPC6t2sgGaGbVRCwhYC8wfkgLQbbSUDNM-z6id1r3mR3Q&new=1"
    browser.get(url)
    WebDriverWait(browser, 10)
    selector = etree.HTML(browser.page_source)
    links = selector.xpath('//*[@id="js_content"]/table/tbody/tr/descendant::a/@href')
    print('{} len:{}'.format(len(links),links))

    for jump_url in links:
        browser.get(jump_url)
        #print(jump_url)
        WebDriverWait(browser, 10)
        selector = etree.HTML(browser.page_source)
        WebDriverWait(browser, 10)
        file_node = WAIT.until(EC.presence_of_element_located((By.XPATH, '//*[@class="audio_card_title"]')))

        #file_name = selector.xpath('//*[@class="audio_card_title"]/text()')[0]
        file_name = file_node.text.replace(' ', '_')

        mediaid = selector.xpath('//mpvoice/@voice_encode_fileid')[0]
        print(file_name, mediaid)
        #mediaid_list = WAIT.until(EC.presence_of_element_located((By.XPATH, '//*[@id="js_content"]/p[3]/mpvoice"]')))
        #print(mediaid_list)
        #mediaid = mediaid_list.attr('voice_encode_fileid')



        media_url = f"{media_url_path}{mediaid}"
        file_name_path = os.path.join(os.getcwd(), file_name)
        #print(file_name_path)
        wget.download(media_url, file_name_path)
    browser.close()

if __name__ == '__main__':
    #urls = ['https://www.jianshu.com/c/bDHhpK?order_by=added_at&page={}'.format(str(i)) for i in range(2) ]
    #pool = Pool(processes=4)
    #pool.map(beautiful_decode, urls)


    #url = 'https://www.jianshu.com/c/bDHhpK?order_by=added_at&page=0'
    #lxml_decode(url)

    #async_load_ajax()

    #selenium_load_ajax()

    #load_english_listening()

    load_four_grade_english_next_semester()