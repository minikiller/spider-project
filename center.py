# 中船重工电子采购平台
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
curDate = html.getCurDate()
start_time = time.time()
cookies = {}
resultList = []  # 存放结果

options = Options()
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

user_agent = UserAgent(verify_ssl=False).random
options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
options.add_argument(f'user-agent={user_agent}')
browser = webdriver.Chrome(options=options)

url = "http://td.ebuy.csemc.com/exp/querybusiness/process/sell/list.do"
browser.get(url)
original_window = browser.current_window_handle
total_link = []


def getResultData(fileName):
    # import index
    with open(fileName, "r") as f:
        page = f.read()
    # tree = html.parse(r'./sales.html')
    # print(page)
    tree = etree.HTML(page)
    # # print(tree)
    # path='/html/body/div'
    path = '/html/body/div[2]/form/div[1]/div[3]/div/table/tr/td[2]'
    href = tree.xpath(path)
    # /html/body/div/div/table/tbody/tr[1]/td[2]
    # for value in href:
    #     # print(value.text)
    #     index.getIndex
    return href

# 获得详细页面


def getData(url, id):
    cookies = util.get_cookies(browser)
    res = requests.get(url, cookies=cookies)
    import html
    fileName = id+".html"
    # html.exportTempHtml(res.text,fileName)
    # sleep(randint(1,3))
    print(res.text)
    # _html = etree.HTML(res.text)
    # //*[@id="gform"]/div[1]/div[3]/div/table/tbody/tr[2]/td[2]
    tree = etree.HTML(res.text)
    # # print(tree)
    # path='/html/body/div'
    path = '/html/body/div[2]/form/div[1]/div[3]/div/table/tr/td[2]'
    datas = tree.xpath(path)
    # datas= getResultData("./tmp/"+fileName)
    print(len(datas), "#############")
    for data in datas:
        title = data.get('title')
        logger.debug(title)
        if index.indexOfStr(data.text, strList):
            filename = f'./{curDate}/{id}.html'
            html.exportHtml(res.text, filename)
            resultList.append(filename)
            break


# 获得master页面
def get_posts(pageNumber, pageSize):
    cookies = util.get_cookies(browser)
    myurl = "http://td.ebuy.csemc.com/exp/querybusiness/process/sell/list.do"
    request_body = {"pageNumber": pageNumber, "pageSize": pageSize}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(myurl, data=request_body,
                             headers=headers, cookies=cookies)
    # sleep(randint(1,3))
    return response


def get_details(res):
    logger.debug(res.text)
    html = etree.HTML(res.text)

    curUrl = 'http://td.ebuy.csemc.com/exp/querybusiness/process/sell/showTd.do?fphm={}'
    # linkPath='/html/body/div[4]/div/div[2]/div[2]/table/tbody/tr/td[3]/a'
    path = '//*[@class="bluefont"]'
    buttons = html.xpath(path)
    # buttons=browser.find_elements(By.XPATH,linkPath)
    # print(len(buttons),"size is ")
    logger.debug(f"size is {len(buttons)}")
    for button in buttons:
        # href=button.get("href")
        id = button.text
        str = curUrl.format(id)
        logger.debug(str)
        getData(str, id)


totalPageSpan = browser.find_element(By.XPATH, '//*[@class="buttonLabel"]')
# totalPage=50
totalPage = util.getNumber(totalPageSpan.text)
logger.info(f"totalPage {totalPage}")
pageSize = 50
for i in util.getPage(int(totalPage), pageSize):
    logger.info(f"current processing page {i},current no is {i*pageSize}")
    res = get_posts(i, pageSize)
    get_details(res)
# res=get_posts(1)


logger.info(f'总共处理记录数：{totalPage}')
use_time = int(time.time()) - int(start_time)
logger.info(f'总共过滤获得的记录数：{len(resultList)}')
logger.info(f'爬取总计耗时：{use_time}秒')
