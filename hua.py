# 华润
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

options = Options()
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

user_agent = UserAgent(verify_ssl=False).random
options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
options.add_argument(f'user-agent={user_agent}')
browser = webdriver.Chrome(options=options)

url = "https://b2b.crpower.com.cn/ispweb/pcux5PonHeaders/souringIndex.do?sourcetag=WZ"
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


def getData(id):
    # cookies = util.get_cookies(browser)
    url = 'https://b2b.crpower.com.cn/ispweb/pcux5PonHeaders/souringdetail.do?sourceId={}'
    headers = {"User-Agent": user_agent}
    str = url.format(id)
    print("#############################", str)
    browser.get(str)
    # sleep(randint(1,3))
    WebDriverWait(browser, 20).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="detail_info_grid"]/div[2]/table/tbody/tr/td[3]')))

    import html
    fileName = id+".html"
    # html.exportTempHtml(browser.page_source,fileName)
    # sleep(randint(1,3))
    # print(res.text)
    # _html = etree.HTML(res.text)
    # //*[@id="gform"]/div[1]/div[3]/div/table/tbody/tr[2]/td[2]
    tree = etree.HTML(browser.page_source)
    # # print(tree)
    # path='/html/body/div'//*[@id="detail_info_grid"]/div[2]/table/tbody/tr/td[3]
    path = '//*[@id="detail_info_grid"]/div[2]/table/tbody/tr/td[3]'
    datas = tree.xpath(path)
    # datas= getResultData("./tmp/"+fileName)
    # print(len(datas),"#############")
    for data in datas:
        title = data.text
        logger.info("get data is "+title)
        if index.indexOfStr(data.text, strList):
            filename = f'./{curDate}/{id}.html'
            html.exportHtml(browser.page_source, filename)
            resultList.append(filename)
            break


# 获得master页面
def get_posts(pageNumber, pageSize):
    # cookies = util.get_cookies(browser)
    # https://b2b.crpower.com.cn/ispweb/pcux5PonHeaders/searchWinningList.do
    endDate = html.getToDate()
    startDate = html.getYesDate()
    query = '{"sourceMethods":"公开", "sourceStatus":"ACTIVE", "queryAll":"", "sourceTypeTag":"WZ","startDate": "' + \
        startDate+'", "endDate":"'+endDate+'"}'

    # query='{"sourceMethods":"公开", "sourceStatus":"ACTIVE", "queryAll":"", "sourceTypeTag":"WZ","startDate": "{startDate}", "endDate":"{endDate}"}'.format(startDate=startDate,endDate=endDate)
    myurl = "https://b2b.crpower.com.cn/ispweb/pcux5PonHeaders/searchWinningList.do"
    request_body = {"data": query,
                    "take": 20,
                    "skip": 0,
                    "page": pageNumber,
                    "pageSize": pageSize}
    # headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    headers = {"User-Agent": user_agent,
               'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(myurl, data=request_body, headers=headers)
    # sleep(randint(1,3))
    return response.json()


def get_details(res):
    # logger.debug(res.json())
    # html = etree.HTML(res.text)
    for data in res["data"]:

        # linkPath='/html/body/div[4]/div/div[2]/div[2]/table/tbody/tr/td[3]/a'
        # path='//*[@class="bluefont"]'
        # buttons=html.xpath(path)
        # buttons=browser.find_elements(By.XPATH,linkPath)
        # print(len(buttons),"size is ")
        # logger.debug(f"size is {len(buttons)}")
        # href=button.get("href")
        id = data['attribute5']
        # str=curUrl.format(id)
        logger.debug(id)
        getData(id)


# totalPage=50
pageSize = 20
user_agent = UserAgent(verify_ssl=False).random
res = get_posts(1, pageSize)
# print()
totalPage = res['totalCount']

for i in util.getPage(int(totalPage), pageSize):
    logger.info(f"current processing page {i},current no is {i*pageSize}")
    res = get_posts(i, pageSize)
    get_details(res)


logger.info(f'总共处理记录数：{totalPage}')
logger.info(f'总共过滤获得的记录数：{len(resultList)}')
use_time = int(time.time()) - int(start_time)
logger.info(f'爬取总计耗时：{use_time}秒')
