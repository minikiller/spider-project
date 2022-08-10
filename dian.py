# 华电
import multiprocessing
from multiprocessing.dummy import Process, Pool
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
import requests
from fake_useragent import UserAgent
import log_setup
import sys


class Dian():
    # browser = getDriver()
    def __init__(self, value):
        log_setup.main()
        self.strList = index.getIndex()
        # strList.append("电焊条")
        self.curDate = html.getCurDate()
        self.start_time = time.time()
        self.resultList = []  # 存放结果
        self.cookies = {}
        self.value = value
        self.totalPage = 0
        # curId=""

        options = Options()
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        self.user_agent = UserAgent(verify_ssl=False).random
        options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
        # options.add_argument("--proxy-server=http://127.0.0.1:1087")
        options.add_argument(f'user-agent={self.user_agent}')
        self.browser = webdriver.Chrome(options=options)

        self.url = "https://www.chdtp.com/zbcg/cggl/displayCgbjAction.action"
        # self.url = "https://www.chdtp.com/"
        # url = "https://www.chdtp.com/zbcg/cggl/detailCgbjToAction.action?authField=6442EC39BB4BC38F62C2763DE5CF190A89FDA9FDA9FDA9F8&cgfs=3&cgdh=GJ202207003431"

    # print(cookies)

    # html.exportHtml(browser.page_source, "./dian.html")

    def close_window():
        pass
        # links = []
        # for handle in browser.window_handles:
        #     if handle != original_window:
        #         browser.switch_to.window(handle)
        #         # print(browser.current_url)
        #         links.append(browser.current_url)
        #         browser.close()
        # browser.switch_to.window(original_window)
        # return links

    def getDetail(self, authField, cgfs, cgdh):
        # global totalPage

        # cookies = util.get_cookies(browser)
        myurl = f"https://www.chdtp.com/zbcg/cggl/detailCgbjToAction.action?authField={authField}&cgfs={cgfs}&cgdh={cgdh}"

        headers = {"User-Agent": UserAgent(verify_ssl=False).random,
                   'Content-Type': 'application/x-www-form-urlencoded', }

        response = requests.get(myurl, headers=headers, cookies=self.cookies)
        data = etree.HTML(response.text)

        idPath = '//*[@id = "resultForm"]/div/table/tr[2]/td[2]/table[2]/tr[1]/td[2]'
        id = data.xpath(idPath)[0].text.strip()
        durDatePath = '//*[@id="resultForm"]/div/table/tr[2]/td[2]/table[2]/tr[2]/td[6]'
        value = data.xpath(durDatePath)[0].text.strip()+":00"
        print("vake value", value)
        durDate = util.compDate(value) 
        companyPath = '//*[@id="resultForm"]/div/table/tr[2]/td[2]/table[2]/tr[2]/td[4]'
        company = data.xpath(companyPath)[0].text.strip()
        titlePath = '//*[@id="resultForm"]/div/table/tr[2]/td[2]/table[2]/tr[1]/td[4]'
        title = data.xpath(titlePath)[0].text.strip()

        self.fullpath = f"./{self.curDate}/{durDate}-{company}-{title}-{id}"
        self.exportHtml(response.text, id)
        logging.info(f"{id} 导出成功")
        self.totalPage = self.totalPage+1
        # print(res)

    def exportHtml(self, source,  id):

        import os
        try:
            os.makedirs(self.fullpath, exist_ok=True)
        except OSError as error:
            logging.error(f'create dir error: {error}')
        with open(f'./{self.fullpath}/{id}.html', "w") as f:
            f.write(source)
            logging.info(f"{id} 保存成功")

    def search(self):
        logging.info(f"{self.value} 查询到{self.value}条数据")
        myurl = "https://www.chdtp.com/zbcg/cggl/displaysCgbjAction.action"
        request_body = {"cgdv.cgbt": self.value}
        # import agent
        headers = {"User-Agent": self.user_agent,
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Referer': 'https: // www.chdtp.com/zbcg/cggl/displayCgbjAction.action'}
        response = requests.post(myurl, data=request_body,
                                 headers=headers, cookies=self.cookies)
        # sleep(randint(1, 3))
        res = response.text
        #
        # html.exportHtml(res, f"./{self.curDate}/{self.value}.html")
        print("status_code is ", response.status_code)
        # print(res)
        # return res
        data = etree.HTML(res)
        totalPath = '//*[@id="Totalcount"]'
        total = data.xpath(totalPath)[0].get("value")
        logging.info(f"{self.value} 查询到{total}条数据")
        if int(total) > 0:
            logging.warning(f"'{self.value}'找到记录,共{total}条")
            aPath = '//*[@id="id_table"]/tr/td[2]/a'
            links = data.xpath(aPath)
            for link in links:
                # print(link.text)
                string = link.get('onclick')
                logging.debug(string)
                pattern = re.compile(r"'(\w+)'")  # 提取单引号内的数据
                result = pattern.findall(string)  # 提取到的数据是个列表
                logging.debug(result)
                # ["A61FC431667610A6DC2BD4225A623D295C3671AD2D256322','3','GJ202207007476','','','"]
                authField = result[0]
                cgfs = result[1]
                cgdh = result[2]
                self.getDetail(authField, cgfs, cgdh)
                # return (authField, cgfs, cgdh)
            return True
        else:
            logging.info(f"{self.value} 没有数据")
            return False

    # token = browser.get_cookie("X-AUTH-TOKEN")["value"]
    # print(token)
    # # res = get_posts(1, pageSize)
    # # print()
    # totalPage = 0

    # 通过页面去搜索数据

    def doPage(self, value):
        inputPath = '//*[@id="id_cgbt"]'
        self.browser.find_element(By.XPATH, inputPath).send_keys(value)
        btnPath = '//*[@id="query"]'
        self.browser.find_element(By.XPATH, btnPath).click()
        self.browser.implicitly_wait(10)
        sleep(10)
        # totalPath = '//*[@id="Totalcount"]'
        # WebDriverWait(browser, 10).until(
        #     EC.presence_of_element_located((By.XPATH, totalPath)))
        html.exportHtml(self.browser.page_source,
                        f"./{self.curDate}/{value}.html")
        data = etree.HTML(self.browser.page_source)
        aPath = '//*[@id="id_table"]/tbody/tr/td[2]/a'
        # links=browser.find_elements(By.XPATH, aPath)
        links = data.xpath(aPath)
        for link in links:
            print(link.text)
            # string = link.get('onclick')
            # logging.debug(stri)

    # search("长春锅炉")
    # sleep(4)
    # search("温度计")
    # sleep(5)

    # for value in strList:
    # sleep(randint(1, 3))
    # search(value)

    # totalPage = res['totalCount']

    # for i in util.getPage(int(totalPage), pageSize):
    #     logging.info(f"current processing page {i},current no is {i*pageSize}")
    #     res = get_posts(i, pageSize)
    #     get_details(res)
    # with open('data.txt','w') as f:
    #     for item in total_link:
    #         # write each item on a new line
    #         f.write("%s\n" % item)

    def main(self):
        self.browser.get(self.url)
        self.original_window = self.browser.current_window_handle
        total_link = []

        self.totalPage = 0
        pageSize = 20
        self.user_agent = UserAgent(verify_ssl=False).random
        self.cookies = util.get_cookies(self.browser)
        names = ['长春锅炉', '液位计']
        procs = []
        self.search()
        # doPage("液位计")
        # sleep(10)
        # for name in names:
        #     # print(name)
        #     proc = Process(target=search, args=(name,))
        #     procs.append(proc)
        #     proc.start()

        # for proc in procs:
        #     proc.join()

        logging.info('#'*50)
        logging.info(f'总共处理记录数：{len(self.strList)}')
        logging.info(f'总共过滤获得的记录数：{self.totalPage}')
        use_time = int(time.time()) - int(self.start_time)
        logging.info(f'爬取总计耗时：{use_time}秒')


def begin(value):
    dian = Dian(value)
    dian.main()


def multi():
    # names = ['长春锅炉', '液位计']
    names = ['液位计']
    multiprocessing.freeze_support()
    pool = Pool(processes=len(names))
    results = pool.map(begin, names)
    for result in results:
        print(result)


if __name__ == '__main__':
    begin(sys.argv[1])
    # multi() # 用于单独测试
