# 国家电投
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
import config


class element_has_value(object):
    """An expectation for checking that an element has a particular css class.

    locator - used to find the element
    returns the WebElement once it has the particular css class
    """

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        # Finding the referenced element
        element = driver.find_element(*self.locator)
        if len(element.get_attribute("value")) > 0:
            # curId=element.get_attribute("value")
            # logging.info("curId:%s" % curId)
            return element
        else:
            return False

class Ebid():
    def __init__(self) -> None:
         
        log_setup.main("info")

        self.strList = index.getIndex()
        # strList.append("电焊条")
        self.curDate = html.getCurDate()
        self.start_time = time.time()
        self.resultList = []  # 存放结果
        self.cookies = {}
        # curId=""

        options = Options()
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        self.user_agent = UserAgent(verify_ssl=False).random
        options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
        options.add_argument(f'user-agent={self.user_agent}')
        self.browser = webdriver.Chrome(options=options)

        url = "https://ebid.espic.com.cn/bidweb/#/procurement/enquiryPaticipation"
        self.browser.get(url)
        self.original_window = self.browser.current_window_handle
        self.total_link = []

    def downloadPdf(self, url, filename):
        import os
        try:
            os.makedirs(self.fullpath, exist_ok=True)
        except OSError as error:
            logging.error(f'create dir error: {error}')
        pdfUrl = 'https://ebid.espic.com.cn/bidprocurement/common-tools/tools/commonUpload/readImageRoot?imagePath={}'.format(
            url)
        logging.debug(pdfUrl)
        import requests
        r = requests.get(pdfUrl, allow_redirects=True)
        self.total_link.append(f'{self.fullpath}/{filename}.pdf')
        open(f'{self.fullpath}/{filename}.pdf', 'wb').write(r.content)

    def getFileInfo(self, token, bizId):
        url = "https://ebid.espic.com.cn/bidprocurement/common-tools/tools/commonUpload/getFileDetail?bizId={}&fileType=bulletin_template_pdf_base&t=1658210556127".format(
            bizId)
        # Headers = { "X-AUTH-TOKEN" : token, "Content-Type": "application/json"}
        Headers = {"X-AUTH-TOKEN": token, "Content-Type": "application/json",
                   "User-Agent": str(self.user_agent)}
        res = requests.get(url, headers=Headers, timeout=120)

        return res.json()

    def callData(self, token, value, pageNo):
        import requests
        url = "https://ebid.espic.com.cn/bidprocurement/procurement-protproject/procurementProject/canParticipateInTheProjectPage"
        # Headers = { "X-AUTH-TOKEN" : token, "Content-Type": "application/json"}
        Headers = {"X-AUTH-TOKEN": token, "Content-Type": "application/json",
                   "User-Agent": str(self.user_agent)}

        data = {"tenderName": value,
                "tenderMethod": "11",
                "pageNo": pageNo,
                "pageSize": 50,
                "state": "01"}
        res = requests.post(url, json=data, headers=Headers, timeout=120)

        return res.json()

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


    def getData(self, id):
        # cookies = util.get_cookies(browser)
        url = 'https://b2b.crpower.com.cn/ispweb/pcux5PonHeaders/souringdetail.do?sourceId={}'
        headers = {"User-Agent": self.user_agent}
        str = url.format(id)
        print("#############################", str)
        self.browser.get(str)
        # sleep(randint(1,3))
        idPath = '//*[@id="souDeatilNum"]'
        dataPath = '//*[@id="detail_info_grid"]/div[2]/table/tbody/tr/td[3]'
        input = WebDriverWait(self.browser, 20).until(
            element_has_value((By.XPATH, idPath)))
        curId = input.get_attribute("value")
        # print("curId:%s" % curId)

        # WebDriverWait(browser, 20).until(EC.presence_of_element_located(
        #     (By.XPATH, idPath)) and len(browser.find_element(By.XPATH, dataPath).get_attribute("value")) > 0
        # )
        # WebDriverWait(browser, 20).until(EC.presence_of_element_located(
        #     (By.XPATH, '//*[@id="detail_info_grid"]/div[2]/table/tbody/tr/td[3]')))
        #
        import html
        fileName = id+".html"
        # html.exportTempHtml(browser.page_source,fileName)
        # sleep(3)
        # print(res.text)
        # _html = etree.HTML(res.text)
        # //*[@id="gform"]/div[1]/div[3]/div/table/tbody/tr[2]/td[2]
        tree = etree.HTML(self.browser.page_source)
        ids = tree.xpath(idPath)
        # print("*"*50)
        # print(len(ids),"#############")
        # print(ids[0].get("data-bind"))
        # print(ids[0].text)
        # path='/html/body/div'//*[@id="detail_info_grid"]/div[2]/table/tbody/tr/td[3]
        path = '//*[@id="detail_info_grid"]/div[2]/table/tbody/tr/td[3]'
        datas = tree.xpath(path)
        # datas= getResultData("./tmp/"+fileName)
        # print(len(datas),"#############")
        for data in datas:
            title = data.text
            logging.info("get data is "+title)
            if index.indexOfStr(data.text, self.strList):
                filename = f'./{self.curDate}/{curId}.html'
                imgfilename = f'./{self.curDate}/{curId}.png'
                html.exportHtml(self.browser.page_source, filename)
                self.browser.save_screenshot(imgfilename)
                self.resultList.append(filename)
                break


    # 获得master页面

    def get_posts(self, pageNumber, pageSize):
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

        headers = {"User-Agent": self.user_agent,
                'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.post(myurl, data=request_body, headers=headers)
        # sleep(randint(1,3))
        return response.json()


    def get_details(self,res):
        # logging.debug(res.json())
        # html = etree.HTML(res.text)
        for data in res["data"]:

            # linkPath='/html/body/div[4]/div/div[2]/div[2]/table/tbody/tr/td[3]/a'
            # path='//*[@class="bluefont"]'
            # buttons=html.xpath(path)
            # buttons=browser.find_elements(By.XPATH,linkPath)
            # print(len(buttons),"size is ")
            # logging.debug(f"size is {len(buttons)}")
            # href=button.get("href")
            id = data['attribute5']
            # str=curUrl.format(id)
            logging.debug(id)
            self.getData(id)
    def test(self,value):
        self.totalPage = 0
        token = self.browser.get_cookie("X-AUTH-TOKEN")["value"]
        
        datas = self.callData(token, value, 1)
        # print(datas)
        count = datas['data']['total']
        if count > 0:
            logging.info(f"'{value}'找到{count}记录")
        else:
            logging.warning(f"'{value}'没有找到记录")
        self.totalPage = self.totalPage+count
        for data in datas['data']['records']:
            bizId = data['bizId']
            tenderNo = data['tenderNo']
            projectBuyersName = data['projectBuyersName']
            tenderName = data['tenderName']
            quoteEndTime = util.compDate(data['quoteEndTime'][:19])
            self.fullpath = f"{self.curDate}/{quoteEndTime}-{projectBuyersName}-{tenderName}-{tenderNo}"
            logging.info(f"Tender Name is {tenderName}")
            logging.debug(bizId)
            result = self.getFileInfo(token, bizId)
            if len(result['data']) > 0:
                path = result['data'][0]['path']
                logging.debug(path)
                self.downloadPdf(path, tenderNo)

        # totalPage = res['totalCount']

        # for i in util.getPage(int(totalPage), pageSize):
        #     logging.info(f"current processing page {i},current no is {i*pageSize}")
        #     res = get_posts(i, pageSize)
        #     get_details(res)

        logging.info('#'*50)
        logging.info(f'总共处理记录数：{len(self.strList)}')
        logging.info(f'总共过滤获得的记录数：{self.totalPage}')
        use_time = int(time.time()) - int(self.start_time)
        logging.info(f'爬取总计耗时：{use_time}秒')

    def main(self):
        # totalPage=50
        pageSize = 20
        token = self.browser.get_cookie("X-AUTH-TOKEN")["value"]
        # print(token)
        # res = get_posts(1, pageSize)
        # print()
        self.totalPage = 0
        for value in self.strList:
            datas = self.callData(token, value, 1)
            # print(datas)
            count = datas['data']['total']
            if count > 0:
                logging.info(f"'{value}'找到{count}记录")
            else:
                logging.warning(f"'{value}'没有找到记录")
            self.totalPage = self.totalPage+count
            for data in datas['data']['records']:
                bizId = data['bizId']
                tenderNo = data['tenderNo']
                projectBuyersName = data['projectBuyersName']
                tenderName = data['tenderName']
                quoteEndTime = util.compDate(data['quoteEndTime'][:19])
                self.fullpath = f"{self.curDate}/{quoteEndTime}-{projectBuyersName}-{tenderName}-{tenderNo}"
                logging.info(f"Tender Name is {tenderName}")
                logging.debug(bizId)
                result = self.getFileInfo(token, bizId)
                if len(result['data']) > 0:
                    path = result['data'][0]['path']
                    logging.debug(path)
                    self.downloadPdf(path, tenderNo)


        # totalPage = res['totalCount']

        # for i in util.getPage(int(totalPage), pageSize):
        #     logging.info(f"current processing page {i},current no is {i*pageSize}")
        #     res = get_posts(i, pageSize)
        #     get_details(res)

        logging.info('#'*50)
        logging.info(f'总共处理记录数：{len(self.strList)}')
        logging.info(f'总共过滤获得的记录数：{self.totalPage}')
        use_time = int(time.time()) - int(self.start_time)
        logging.info(f'爬取总计耗时：{use_time}秒')


if __name__ == '__main__':
    ebid = Ebid()
    ebid.test('孔板')
    # ebid.main()
