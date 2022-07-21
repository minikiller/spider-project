# 华能
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

from lxml import etree
# from lxml import  html as myhtml
import codecs
from random import randint
import index
import html
import time
import util
import logging
import log_setup
import requests
from fake_useragent import UserAgent


# browser = getDriver()
log_setup.main("info")
strList = index.getIndex()
# strList.append("电焊条")
curDate = html.getCurDate()
start_time = time.time()
resultList = []  # 存放结果
cookies = {}
# curId=""

options = Options()
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

user_agent = UserAgent(verify_ssl=False).random
options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
options.add_argument(f'user-agent={user_agent}')
browser = webdriver.Chrome(options=options)

url = "http://ec.chng.com.cn/ecmall/morelogin.do?type=107"
# url = "https://www.chdtp.com/zbcg/cggl/detailCgbjToAction.action?authField=6442EC39BB4BC38F62C2763DE5CF190A89FDA9FDA9FDA9F8&cgfs=3&cgdh=GJ202207003431"

browser.get(url)
original_window = browser.current_window_handle
total_link = []

totalPage = 0
pageSize = 20
user_agent = UserAgent(verify_ssl=False).random
cookies = util.get_cookies(browser)
# print(cookies)

# html.exportHtml(browser.page_source, "./dian.html")


def close_window():
    links = []
    for handle in browser.window_handles:
        if handle != original_window:
            browser.switch_to.window(handle)
            # print(browser.current_url)
            links.append(browser.current_url)
            browser.close()
    browser.switch_to.window(original_window)
    return links


def getDetail(announcementId):
    global totalPage

    # cookies = util.get_cookies(browser)
    myurl = f"http://ec.chng.com.cn/ecmall/announcement/announcementDetail.do?announcementId={announcementId}"

    headers = {"User-Agent": UserAgent(verify_ssl=False).random,
               'Content-Type': 'text/html;charset=UTF-8', }

    response = requests.get(myurl, headers=headers, cookies=cookies)
    idPath = '/html/body/div[4]/div/div[4]/div/div/div[1]/div[1]'

    data = etree.HTML(response.text)
    id = data.xpath(idPath)[0].text
    filename = f"./{curDate}/{id}.html"
    html.exportHtml(response.text, filename)
    logging.info(f"{filename} 导出成功")
    attachPath = '/html/body/div[4]/div/div[4]/div/div/div[1]/div[4]/p/a'
    attachs = data.xpath(attachPath) # 获取附件
    if len(attachs)>0:
        logging.info(f"附件个数：{len(attachs)}")
        for attach in attachs:
            attachUrl = attach.get("href")
            attachName = attach.text
            if attachUrl is not None:
                attachUrl = f"http://ec.chng.com.cn{attachUrl}"
                attachName = f"{curDate}/{id}_{attachName}"
                import util
                util.downloadFile(attachUrl, attachName)
                logging.info(f"附件{attachName} 导出成功")
    else:
        logging.info(f"附件为空")
    totalPage = totalPage+1
    # print(res)


def search(value):
    logging.info(f"{value} 查询到{value}条数据")
    myurl = "http://ec.chng.com.cn/ecmall/more.do"
    request_body = {"type": 107,
                    "searchWay": "onTitle",
                    "search": value,
                    "ifend": "in",
                    "start": 0,
                    "limit": 10,
                    }
    import agent
    headers = {"User-Agent": agent.getHeader(),
               'Content-Type': 'application/x-www-form-urlencoded',
               'Referer': 'https: // www.chdtp.com/zbcg/cggl/displayCgbjAction.action'}
    response = requests.post(myurl, data=request_body,
                             headers=headers, cookies=cookies)
    # sleep(randint(1, 3))
    res = response.text
    # print(res)
    import html
    # html.exportHtml(res, f"./{curDate}/{value}.html")
    data = etree.HTML(response.text)
    totalPath = '//*[@id="viewPageSize"]'
    total = 10 #data.xpath(totalPath)[0].text
    logging.info(f"{value} 查询到{total}条数据")
    if int(total) > 0:
        logging.warning(f"'{value}'找到记录,共{total}条")
        aPath = '//*[@id="pageForm"]/ul/li/a'
        links = data.xpath(aPath)
        for link in links:
            string = link.get('href')
            logging.debug(f'href string is: {string}')

            # logging.debug(string)
            pattern = re.compile(r"'(\w+)'")  # 提取单引号内的数据
            result = pattern.findall(string)  # 提取到的数据是个列表
            logging.debug(f'express value is : {result}')
            # # ["A61FC431667610A6DC2BD4225A623D295C3671AD2D256322','3','GJ202207007476','','','"]
            authField = result[0]
            # cgfs = result[1]
            # cgdh = result[2]
            getDetail(authField)
    else:
        logging.info(f"{value} 没有数据")


# token = browser.get_cookie("X-AUTH-TOKEN")["value"]
# print(token)
# # res = get_posts(1, pageSize)
# # print()
# totalPage = 0

# search("吉林")
# sleep(10)
# search("温度计")
# sleep(8)
# search("云母")
# search("液位计")
# sleep(10)

for value in strList:
    # sleep(randint(1, 3))
    search(value)


# totalPage = res['totalCount']

# for i in util.getPage(int(totalPage), pageSize):
#     logging.info(f"current processing page {i},current no is {i*pageSize}")
#     res = get_posts(i, pageSize)
#     get_details(res)
# with open('data.txt','w') as f:
#     for item in total_link:
#         # write each item on a new line
#         f.write("%s\n" % item)
logging.info('#'*50)
logging.info(f'总共处理记录数：{len(strList)}')
logging.info(f'总共过滤获得的记录数：{totalPage}')
use_time = int(time.time()) - int(start_time)
logging.info(f'爬取总计耗时：{use_time}秒')
