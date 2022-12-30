# -*- coding:utf-8 -*-
'''
================================================
    file_name:      用request爬取数据
    Description:
    Author:         gpr
    Date:           2022/12/16
============================================
'''
from lxml import etree
import requests
import time

def main():
    start = time.time()  # 开始计时⏲
    url = 'https://www.qidian.com/rank/yuepiao?style=1&page=1'
    headers = { 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36' }
    page = requests.get(url,headers=headers)
    html = etree.HTML(page.content.decode('utf-8'))
    books = html.xpath("//div[@class='book-img-text']/ul/li")
    for book in books:
        print(book.xpath('// *[ @ id = "book-img-text"] / ul / li[1] / div[1] / a/@href')[0])

        imglink = 'https:' + book.xpath("./div[1]/a/@href")[0] # 其它信息xpath提取，这里省略 ....
        #title = book.xpath("//*[@id="book-img-text"]/ul/li[1]/div[2]/h2/a")
        update = book.xpath("./div[2]/p[3]/a/text()")[0]
        print(imglink, update)
        #print(imglink,title,author,intro,update)
    end = time.time() # 结束计时⏲
    print(end-start)

if __name__ == '__main__':
    main()
