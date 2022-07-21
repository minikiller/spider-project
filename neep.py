# 国家电投
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
import logger
import requests
from fake_useragent import UserAgent

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

url = "https://www.neep.shop/dist/index.html#/purchaserNoticeIndex"
browser.get(url)
original_window = browser.current_window_handle
total_link = []

totalPage = 0
pageSize = 20
user_agent = UserAgent(verify_ssl=False).random
cookies = util.get_cookies(browser)


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


def getDetail(inquiryId, passkey):
    # cookies = util.get_cookies(browser)
    myurl = "https://www.neep.shop/rest/service/routing/inquiry/quote/encryptSupplierIqrPurchaseNoticeDetail"
    request_body = {"inquiryId": int(inquiryId),
                    "iqrSeq": 1, "purchaseCategory": 1}
    logger.debug(request_body)
    headers = {"User-Agent": user_agent, "Referer": "https: // www.neep.shop/dist/index.html",
               'Content-Type': 'application/x-www-form-urlencoded', 'passkey': passkey}
    logger.debug(headers)
    response = requests.post(myurl, data=request_body,
                             headers=headers, cookies=cookies)
    # sleep(randint(1,3))
    res = response.json()
    for data in res['data']['attchmentInfo1']:
        logger.debug("attchmentInfo1")
        print(data['attachmentUrl'])
        print(data['attachmentName'])
    for data in res['data']['attchmentInfo2']:
        logger.debug("attchmentInfo2")
        print(data['attachmentUrl'])
        print(data['attachmentName'])
    for data in res['data']['attchmentInfo3']:
        logger.debug("attchmentInfo3")
        print(data['attachmentUrl'])
        print(data['attachmentName'])
    for data in res['data']['attchmentInfo4']:
        logger.debug("attchmentInfo4")
        print(data['attachmentUrl'])
        print(data['attachmentName'])

    # print(res)


def search(value):
    global totalPage
    myurl = "https://www.neep.shop/rest/service/routing/inquiry/quote/encryptSupplierQryIqrPurchaseNoticeList"
    request_body = {"pageNo": 1,
                    "pageSize": 50,
                    "inquiryName": value}
    headers = {"User-Agent": user_agent,
               'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(myurl, data=request_body,
                             headers=headers, cookies=cookies)
    # sleep(randint(1,3))
    res = response.json()
    print(res)
    count = res['data']['recordsTotal']
    # print(count)
    if count > 0:
        totalPage = totalPage+count
        logger.warning(f"'{value}'找到记录,共{count}条")
    else:
        logger.info(f"'{value}'没有找到记录")
    for data in res['data']['rows']:
        inquiryCode = data['inquiryCode']  # 询价单号
        inquiryId = data['inquiryId']
        inquiryName = data['inquiryName']
        if(inquiryName.find(value) > 1):  # 如果包含查询值
            passkey = data['passkey']
            detailUrl = f'https://www.neep.shop/dist/index.html#/purchaserNoticeDetail/1/{inquiryId}/1?backPage=purchaserNoticeIndex&joinable=true&receivedClarify=0&passkey={passkey}'
            # logger.info(f"{inquiryCode} {inquiryName} {detailUrl}")
            str = f"window.open('{detailUrl}');"
            # str = f"window.open('{detailUrl}','_blank');"
            print(str)
            browser.execute_script(str)
            browser.implicitly_wait(10)
            # browser.tab_new(detailUrl)
            # browser.get(detailUrl)
            total_link.append(detailUrl)
            # sleep(3)
            # browser.get("http://sina.com")
            # print(browser.current_url)
            # sleep(3)
            labelPath = '//*[@id="app"]/div/div[3]/div[2]/div[2]/div/div[1]/div/div/form/div[1]/div/label'
            tablePath = '//*[@id="app"]/div/div[3]/div[2]/div[2]/div/div[3]/div[2]/div/div[2]/table/tbody/tr/td[2]'

            WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.XPATH, tablePath)))

            # WebDriverWait(browser, 20).until(EC.text_to_be_present_in_element(
            #     (By.XPATH, labelPath), inquiryCode) and EC.presence_of_element_located((By.XPATH, tablePath)))

            # source=browser.page_source
            # html.exportHtml(source,)
            with open(f'./{curDate}/{inquiryCode}.html', "w") as f:
                f.write(browser.page_source)
                logger.info(f"{inquiryCode}保存成功")
            # close_window()
            # getDetail(inquiryId, passkey)
        else:
            totalPage = totalPage-1
            logger.warning(f"不包括查询值：'{value}'")


# token = browser.get_cookie("X-AUTH-TOKEN")["value"]
# print(token)
# # res = get_posts(1, pageSize)
# # print()
# totalPage = 0
search("液位计")

# for value in strList:
#     search(value)


# totalPage = res['totalCount']

# for i in util.getPage(int(totalPage), pageSize):
#     logger.info(f"current processing page {i},current no is {i*pageSize}")
#     res = get_posts(i, pageSize)
#     get_details(res)
with open('data.txt','w') as f:
    for item in total_link:
        # write each item on a new line
        f.write("%s\n" % item)
logger.info('#'*50)
logger.info(f'总共处理记录数：{len(strList)}')
logger.info(f'总共过滤获得的记录数：{totalPage}')
use_time = int(time.time()) - int(start_time)
logger.info(f'爬取总计耗时：{use_time}秒')
