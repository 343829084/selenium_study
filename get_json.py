# -*- coding:utf-8 -*-
'''
================================================
    file_name:      get_json
    Description:
    Author:         gpr
    Date:           2022/12/21
============================================
'''
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from selenium.webdriver.chrome.options import Options

#browser = webdriver.PhantomJS()
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('blink-settings=imagesEnabled=false')
chrome_options.add_argument('User-Agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 ')
chrome_options.add_argument('Cookie=PSTM=1621852481; BIDUPSID=BFE5655A305F6E3B205161371B4CE7D1; __yjs_duid=1_ac04bbb8b6f1e0aa5846a85f6cbf0a911621856151165; BD_UPN=12314753; BDUSS=nVQWTY1UWVYRVgxTk9Ja1RvMDRScDJPNkpGa0RtTzJEeUhLWEtxS2NHbnVrRDVpSVFBQUFBJCQAAAAAAAAAAAEAAAAAtNwPZ3ByYmQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO4DF2LuAxdid; BDUSS_BFESS=nVQWTY1UWVYRVgxTk9Ja1RvMDRScDJPNkpGa0RtTzJEeUhLWEtxS2NHbnVrRDVpSVFBQUFBJCQAAAAAAAAAAAEAAAAAtNwPZ3ByYmQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO4DF2LuAxdid; BAIDUID=CD32D9BE2B8182A137A98107A24F14B7:SL=0:NR=10:FG=1; MCITY=-:; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; newlogin=1; BA_HECTOR=a00g0gala40g0gal0g2g86dr1hq31u81j; ZFY=V84PTId:A8PFxk7gWauRHI4hMlLeYZN7of3GECNitZoc:C; BAIDUID_BFESS=CD32D9BE2B8182A137A98107A24F14B7:SL=0:NR=10:FG=1; ab_sr=1.0.1_ZTUwZTE0NmU2YWFiM2Y5ZTczOWI2NzVmY2JmNjI5Zjc3NTg5MTA0ZWEzMzNhNTg1NGMwZThhZjYwYjk1NjY3YWRlNTk1NDA5NjUwYzk4MjdmOGRmZGEwMzZiMjA2Yjg2NDVjODNlYWMzOThjOGQ5ZGFmODY1ZGM1M2JhYjkyYmI2Mzk1MDBjZmFkYWQ1ZmZiY2QzYzBlNzc0ZWRhNTY4ZA==; baikeVisitId=7ebd30f4-29cb-40ea-b47c-daa835a2c9fe; __bid_n=18515cdd1f5d4356534207; COOKIE_SESSION=4_1_9_9_10_36_1_1_8_9_1_4_41801_0_22_0_1671584277_1671527834_1671584255|9#438786_36_1671527822|8; BD_HOME=1; H_PS_PSSID=37784_36557_37647_37518_37689_37906_36804_37949_37933_37901_26350_37959_37789_37881; sug=3; sugstore=0; ORIGIN=0; bdime=0; SL_G_WPT_TO=zh-CN; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1')
browser = webdriver.Chrome(options=chrome_options)
WAIT = WebDriverWait(browser, 10)
def test():
    #打开浏览器
    try:
        browser.('url = https://www.icourse163.org/web/j/mocCourseV2RpcBean.getCourseEvaluatePaginationByCourseIdOrTermId.rpc?csrfKey=f53df406309946cc9be63bde7ca98dc5')
        print("begin open baidu")
        #显示等待
