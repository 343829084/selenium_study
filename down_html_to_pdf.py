# -*- coding:utf-8 -*-
'''
================================================
    file_name:      down_html_to_pdf
    Description:   从网站上下载培训教程或书籍，并将它转为pdf
    Author:         gpr
    Date:           2022/12/30
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
import requests
import wget
import os
import re
import pdfkit
from PyPDF2 import PdfReader, PdfWriter
from bs4 import BeautifulSoup

config = pdfkit.configuration(wkhtmltopdf=r'E:\wkhtmltopdf\bin\wkhtmltopdf.exe')


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('blink-settings=imagesEnabled=false')
chrome_options.add_argument('User-Agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 ')
chrome_options.add_argument('Cookie=_uab_collina=165787356227684108331801; _ga=GA1.2.137805932.1621932895; __yadk_uid=c7XWXGObaTnEw5o6l71nlvgRGZi53wZe; UM_distinctid=1819ef2c3c94e3-0a5c99301962fe-c4f7526-e1000-1819ef2c3cab6c; __bid_n=1843caffb20f7d61544207; FPTOKEN=30$lWR1oc8e8I9/MV7aSXgVRmf9jLbmUwAif6wSxGQLnQXwxUYC2P5K0TgU1K2D6Uv2E7u5ts6eqGQk6U/gvit4i3hyQJrG7+9KQRMl3eiMUs53VCa35feQZV2x5w/UV4fNRpC5RsnqjdoPsUTT15QhynCjPdGvM6Nl4JMdwLw4j7+E2W5SY56RXmWkVGY31fhdXg4R4oJjhF2FnZ1r8zfv5xcY1sVmf8x3LDOeWOHQ9naPGE4jT1at4FuQyOI+Clcs87Yvcc7k2+i/DbS4xkpzyzw6utq4O4oQz0M+hgrUC3a2VQ3bQKifqReRNcmXssk9SAUm5rof6V/yi2mdfAxGhOLjKBvyG3ChRd2z27O/gwoT/VRRvc+NvIrmZwI3lCcA|fdDNIIV11d7pc/4VOeWQv/051ob3Kr9uBbsKDtBrdMc=|10|27fa18cec1d62015c35ad75c268896b2; ssxmod_itna=QqmxnDyD2QDtqDKGHKpWxjxwQ7i=oz7rWDgCx0v+veGzDAxn40iDtoPknQrDrBxEx4WD5Ch0tWYSE4oe+YK/C+PDHxY=DUaibqoD4fKGwD0eG+DD4DWDmWFDnxAQDjxGPnUpNH=DEDm48DWPDYxDrAoKDRxi7DDydHx07DQ58Pza+2PgkqWA43GKD9=oDsgxEiGFwpz3eya7vsS53+x0kc40OuP5zOPoDUjFzngve5GRxb0wHzARD3nioKD2D77DPsFD4Fq2e4rioiB2Dz0+PWEQDiEwRHYD; ssxmod_itna2=QqmxnDyD2QDtqDKGHKpWxjxwQ7i=oz7rWDgDn9EYeDsPKDL0ADXR4xqn4hlDLrwz28G20=7o0Gm02b0KB2qdzOmhB7aPHEr7Gcwe4IhP6xnnznTEGr/CC0SvLZhq5xIBG5mDwLB9xTH5pq==QBO3Cet37YhSipWVgP8b3qKqbpsN/cs2igIwZ5N50+wDFbElmwvHgB+6bqGh4uLpKdaH8y1cePOcG0TK2wbwE3UUAqLjBhtDNKugBe8trY2HEntWOAHMQgp7s0HDTAnHFctQwFQgijWxh/HGVSoDQFdDjKD+xhDD; CNZZDATA1279807957=2039719285-1621931300-https%3A%2F%2Fwww.baidu.com%2F|1669008145; Hm_lvt_1c6cd6a9fd5f687d8040b44bebe5d395=1667465479,1669011587; read_mode=day; default_font=font2; locale=zh-CN; _m7e_session_core=91d7d157c3a669879896573d2a87c68e; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1671178213,1671458694,1671506308,1671777426; sensorsdata2015jssdkcross={"distinct_id":"179a2bbea88558-0979aec337de53-38654702-921600-179a2bbea89878","first_id":"","props":{"$latest_traffic_source_type":"直接流量","$latest_search_keyword":"未取到值_直接打开","$latest_referrer":"","$latest_utm_source":"recommendation","$latest_utm_medium":"seo_notes","$latest_utm_campaign":"maleskine","$latest_utm_content":"note"},"$device_id":"179a2bbea88558-0979aec337de53-38654702-921600-179a2bbea89878"}; FEID=v10-b97a818be2b4eb836f4f08a64ec540c0dd6e9c99; __xaf_fpstarttimer__=1671777426625; SL_G_WPT_TO=zh-CN; __xaf_ths__={"data":{"0":1,"1":43200,"2":60},"id":"3c55040f-4b10-416a-a04c-acbe46c4b80d"}; __xaf_thstime__=1671777427139; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; FPTOKEN=tfM2oKC04gUMbB5HNU21NYbD6qNkpkYJGEFDr7siEUqSokgX0d3tUWh4y/23Wp+FDYi0CRqIj3iYtLbtaqjgOHM5ShsB+QEHOja/B6PmK6VMOeB2boxSM9XCoytlxArTakyRew8Q/LarXlxFD4893VWd7rrKfJHQL3lRIfm5Rj4/Dfa8XbGE+kvMYMCw9PlVvM9HuEN5wQI9p7YUu7lPtXGVY97kqDuucRO3qBI9/Z9JkuvFhHl5CO8avL9lypvFsxxZVk/1DLGIR53Gq4vn7NvQDbIoD+Ls3+0jdkdF7Hbxf1u9s7BQeY7V63TjbHeVrCCwvGFD72gbTgRGZ2KNQ/QTgAuqJz+Jh+ZelQAVOox4rZXAHxhKwbidY154at4dAkYKTIcOR6YVqjGncYyPdQ==|nwyK7zgAdJbBCCfjyjLWQoQ+4uCI/mztjB2ouTjgko8=|10|b606817a39494acbeec5ca736e8df45e; __xaf_fptokentimer__=1671777427264; Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1671777469; signin_redirect=https://www.jianshu.com/c/bDHhpK')
browser = webdriver.Chrome(options=chrome_options)
WAIT = WebDriverWait(browser, 10)
base_url="https://www.osgeo.cn/scrapy/"
chapter_info = []
chapter_names = []

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
</head>
<body>
{content}
</body>
</html>
"""
def parse_title_url(url):
    # 用lxml来解释网页，这个速度更快

    browser.get(url)
    WebDriverWait(browser, 10)  # 这个很重要，否则就爬不到内容了
    selector = etree.HTML(browser.page_source)

    book_name = selector.xpath('/html/body/div[1]/nav/div/div[1]/a/text()')[0]
    print(book_name)

    charpers = selector.xpath('//div[@class="wy-menu wy-menu-vertical"]/descendant::li[@class ="toctree-l1"]')
    for charper in charpers:
        info = {}

        # 获取某章节的title及url
        info['title'] = charper.xpath('a/text()')[0]
        url = charper.xpath('a/@href')[0]
        if re.search('\.\./', url):
            url = url.replace('../', '')
        else:
            url = 'intro/' + url
        info['url'] = base_url + url

        chapter_info.append(info)

def get_content(url):
    browser.get(url)
    WebDriverWait(browser, 10)  # 这个很重要，否则就爬不到内容了
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    content = soup.find('div', attrs={'itemprop': 'articleBody'})
    #print(url, "content:",content)
    html = html_template.format(content=content)
    return html
'''
'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-bottom':'0.75in',
        'margin-left':'0.75in',
        'margin-right':'0.75in',
        '''
def save_pdf(html, file_name):
    options = {
        'encoding': 'UTF-8',
        'custom-header': [
            ('Accept-Encoding', 'gzip'),
        ],
        "enable-local-file-access": True,
        'outline-depth': 10,
    }
    #print(f"{file_name}")
    #print(html)
    pdfkit.from_string(html,file_name, options=options, configuration=config)

def download_to_pdf(info):
    html = get_content(info['url'])
    save_pdf(html, os.path.join(os.getcwd(), info['title'] + '.pdf'))
    chapter_names.append((info['title'], os.path.join(os.getcwd(), info['title'] + '.pdf')))


def merge_pdf(out_pdf):
    '''
    合并pdf,输出为一个pdf
    pdf_list 输入多个待合并的pdf
    out_pdf 输出pdf
    :return:
    '''
    page_num = 0
    pdf_output = PdfWriter()

    for pdf in chapter_names:
        #先合并一级目录内容
        first_level_title = pdf[0]
        pdf_input = PdfReader(open(pdf[1], 'rb'))
        page_count = len(pdf_input.pages)
        for i in range(page_count):
            pdf_output.add_page(pdf_input.pages[i])
            
        #添加书签
        pdf_output.add_outline_item(first_level_title, page_number=page_count)
        
        #页数增加
        page_num += page_count
        
        #存在子章节
        
        
    #合并
    pdf_output.write(open(out_pdf, 'wb'))
    #shutil.rmtree(os.path.join(os.path.dirname(__file__), 'gen'))


def main():
    '''
    url = "https://www.osgeo.cn/scrapy/intro/overview.html"
    parse_title_url(url)
    pool = Pool(processes=5)
    pool.map(download_to_pdf, chapter_info)
    print(chapter_names)
    '''
    #将pdf文件
    path_list = os.listdir(os.getcwd())
    for file in path_list:
        if file.endswith(".pdf"):
            chapter_names.append((os.path.splitext(file)[0], file))

    out_file = os.path.join(os.getcwd(), 'gen/scrapy_2.5.pdf')
    print("cur_path: {}".format(out_file))
    merge_pdf(out_file)
if __name__ == '__main__':
    main()