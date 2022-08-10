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
import logging
import log_setup
import requests
from fake_useragent import UserAgent
# from base import BaseSpider


class Center():
    def __init__(self):
        log_setup.main()
        self.strList = index.getIndex()
        self.curDate = html.getCurDate()
        self.start_time = time.time()
        self.cookies = {}
        self.resultList = []  # 存放结果

        options = Options()
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        self.user_agent = UserAgent(verify_ssl=False).random
        options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
        options.add_argument(f'user-agent={self.user_agent}')
        self.browser = webdriver.Chrome(options=options)

    def getResultData(self, fileName):
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

    def getData(self, url, id):
        cookies = util.get_cookies(self.browser)
        res = requests.get(url, cookies=cookies)
        import html
        fileName = id+".html"
        # html.exportTempHtml(res.text,fileName)
        # sleep(randint(1,3))
        logging.debug(res.text)
        # _html = etree.HTML(res.text)
        # //*[@id="gform"]/div[1]/div[3]/div/table/tbody/tr[2]/td[2]
        tree = etree.HTML(res.text)
        # # print(tree)
        # path='/html/body/div'
        path = '/html/body/div[2]/form/div[1]/div[3]/div/table/tr/td[2]'
        datas = tree.xpath(path)
        durDatePath = '//*[@id="gform"]/div[1]/div[2]/table/tr[3]/td[2]'
        durDate = tree.xpath(durDatePath)[0].text.strip()[:10]
        titlePath = '//*[@id="gform"]/div[1]/div[2]/table/tr[1]/td[2]'
        mytitle = tree.xpath(titlePath)[0].text.strip()
        # datas= getResultData("./tmp/"+fileName)
        # print(len(datas), "#############")
        logging.info(f"{durDate} {mytitle} {id}")
        for data in datas:
            title = data.get('title')
            logging.debug(title)
            if index.indexOfStr(title, self.strList):
                # filename = f'./{self.curDate}/{id}.html'
                self.fullpath = f'{self.curDate}/{durDate}-{id}-{mytitle}'
                logging.info(self.fullpath)
                self.exportHtml(res.text, id)
                self.resultList.append(id)
                break

    # 获得master页面

    def get_posts(self, pageNumber, pageSize):
        cookies = util.get_cookies(self.browser)
        myurl = "http://td.ebuy.csemc.com/exp/querybusiness/process/sell/list.do"
        request_body = {"pageNumber": pageNumber, "pageSize": pageSize}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(myurl, data=request_body,
                                 headers=headers, cookies=cookies)
        # sleep(randint(1,3))
        return response

    def get_details(self, res):
        logging.debug(res.text)
        html = etree.HTML(res.text)

        curUrl = 'http://td.ebuy.csemc.com/exp/querybusiness/process/sell/showTd.do?fphm={}'
        # linkPath='/html/body/div[4]/div/div[2]/div[2]/table/tbody/tr/td[3]/a'
        path = '//*[@class="bluefont"]'
        buttons = html.xpath(path)
        # buttons=browser.find_elements(By.XPATH,linkPath)
        # print(len(buttons),"size is ")
        logging.debug(f"size is {len(buttons)}")
        for button in buttons:
            # href=button.get("href")
            id = button.text
            str = curUrl.format(id)
            logging.debug(str)
            self.getData(str, id)

    def main(self):
        url = "http://td.ebuy.csemc.com/exp/querybusiness/process/sell/list.do"
        self.browser.get(url)
        self.original_window = self.browser.current_window_handle
        self.total_link = []
        totalPageSpan = self.browser.find_element(
            By.XPATH, '//*[@class="buttonLabel"]')
        # totalPage=50
        totalPage = util.getNumber(totalPageSpan.text)
        logging.info(f"totalPage {totalPage}")
        pageSize = 50
        for i in util.getPage(int(totalPage), pageSize):
            logging.info(
                f"current processing page {i},current no is {i*pageSize}")
            res = self.get_posts(i, pageSize)
            self.get_details(res)
        # res=get_posts(1)

        logging.info(f'总共处理记录数：{totalPage}')
        use_time = int(time.time()) - int(self.start_time)
        logging.info(f'总共过滤获得的记录数：{len(self.resultList)}')
        logging.info(f'爬取总计耗时：{use_time}秒')

    def exportHtml(self, source, fileName):

        import os
        try:
            os.makedirs(self.fullpath, exist_ok=True)
        except OSError as error:
            logging.error(f'create dir error: {error}')
        with open(f'./{self.fullpath}/{fileName}.html', "w", encoding="utf-8") as f:
            f.write(source)
            logging.info(f"{fileName} 保存成功")
        # self.changeFile(f'./{self.fullpath}/{fileName}.html')

    def changeFile(self, source):
        with open(source, "r", encoding="gb2312") as f:
            contents = f.readlines()

        data = '<meta http-equiv="Content-Type" content="text/html;charset=gb2312">'
        contents.insert(8, data)

        with open(source, "w", encoding="gb2312") as f:
            for item in contents:
                # write each item on a new line
                f.write(item)


if __name__ == '__main__':
    data = Center()
    data.main()
    # changeFile("./XJ022080500778.html")
