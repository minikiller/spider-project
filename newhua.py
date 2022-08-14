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
import logging
import log_setup
import requests
from fake_useragent import UserAgent
from base import BaseSpider
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
        if len(element.text) > 0:
            # curId=element.get_attribute("value")
            logging.debug("curId:%s" % element.text)
            return element
        else:
            return False


class HuaCls(BaseSpider):
    def __init__(self) -> None:
        super().__init__()
        log_setup.main()
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
        url = "https://szecp.crc.com.cn/TPBidder/fui/pages/centralframe/evalframe"
        # url = "https://szecp.crc.com.cn/srm/ssrc/supplier-quotation/list"
        self.browser.get(url)
        self.original_window = self.browser.current_window_handle
        self.cookies = util.get_cookies(self.browser)
        self.total_link = []
        self.copy_css()

    def copy_css(self):
        import shutil
        filename = "hzero-ui.css"
        moduleName = config.getModuleName()
        shutil.copyfile(f'hua/{filename}', f'{moduleName}/{filename}')

    # 获得master页面
    def get_pages(self, pageNumber, pageSize, token):
        # cookies = util.get_cookies(browser)
        # https://b2b.crpower.com.cn/ispweb/pcux5PonHeaders/searchWinningList.do

        myurl = "https://szecp.crc.com.cn/srm/api/ssrc/v1/269222/rfx/supplier/list"
        # query='{"sourceMethods":"公开", "sourceStatus":"ACTIVE", "queryAll":"", "sourceTypeTag":"WZ","startDate": "{startDate}", "endDate":"{endDate}"}'.format(startDate=startDate,endDate=endDate)
        # myurl = "https://b2b.crpower.com.cn/ispweb/pcux5PonHeaders/searchWinningList.do"
        query_body = {
            "queryType": "ALL",
            "page": pageNumber,
            "size": pageSize}
        # headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        self.headers = {"User-Agent": self.user_agent,
                        "Authorization": "bearer "+token}

        response = requests.get(myurl, params=query_body,
                                headers=self.headers, cookies=self.cookies)
        # sleep(randint(1,3))
        # logging.info(response.text)
        return response.json()

    def get_details(self, res):
        # logging.debug(res.json())
        # html = etree.HTML(res.text)
        for data in res["content"]:
            rfxHeaderId = data['rfxHeaderId']
            tenantId = data['tenantId']
            attachmentUuid = data['businessAttachmentUuid']

            url = f"https://szecp.crc.com.cn/srm/api/ssrc/v1/{tenantId}/rfx-open/supplier/{rfxHeaderId}/items?page=0&size=10"
            response = requests.get(url,
                                    headers=self.headers, cookies=self.cookies)
            result = response.json()
            # logging.info(result)
            for items in result['content']:
                # 判断是否有报价
                if items['itemName'] != None:
                    logging.info("current items is: "+items['itemName'])
                    if index.indexOfStr(items['itemName'], self.strList):
                        # 保存html
                        logging.warning(f"{items['itemName']} is found")
                        self.get_html(rfxHeaderId, tenantId)
                        self.get_attachment(attachmentUuid, tenantId)
                        break
                else:
                    logging.error("url get error data " + url)
                    # logging.error("get result is "+response.text)

            # self.getData(rfxHeaderId)
    def get_attachment(self, businessAttachmentUuid, tenantId):
        url = f"https://szecp.crc.com.cn/srm/api/hfle/v1/{tenantId}/files/{businessAttachmentUuid}/file?attachmentUUID={businessAttachmentUuid}&bucketName=ssrc-rfx-rfxheader"
        response = requests.get(
            url, headers=self.headers, cookies=self.cookies)
        result = response.json()
        # logging.info(response.text)
        for items in result:
            download_url = items['fileUrl']
            filename = items['fileName']
            logging.info(f"download file {filename} is saved")
            self.download_file(download_url, f'{self.fullpath}/{filename}')

    def download_file(self, url, filename):
        import requests
        logging.info(f"download file {url} is saved")
        r = requests.get(url, allow_redirects=True,headers=self.headers)
        try:
            with open(filename, 'wb') as f:
                f.write(r.content)
            logging.info(f"{filename} 下载成功")
        except Exception as e:
            logging.error(f"{filename} 下载失败,错误是: {e}")

    def get_html(self, id, tenantId):
        url = f"https://szecp.crc.com.cn/srm/ssrc/supplier-quotation/detail/{id}/183203/view?tenantId={tenantId}&sourceMethod=OPEN&quotationHeaderId="
        # response = requests.get(
        #     url, headers=self.headers, cookies=self.cookies)
        self.browser.get(url)

        # sleep(5)
        # data = etree.HTML(self.browser.page_source)
        idPath = '//*[@id="root"]//form/div[1]/div[1]/div/div[2]/div/span'

        # idPath = '//*[@class="min_tablehz"][1]//tr[1]/td[2]'
        # id = data.xpath(idPath)[0].text.strip()
        id = WebDriverWait(self.browser, 10).until(
            element_has_value((By.XPATH, idPath))).text
        logging.info("id is "+id)
        # logging.error(f'id is {id}')

        companyPath = '//*[@id="root"]//form/div[2]/div[1]/div/div[2]/div/span'
        # company = data.xpath(companyPath)[0].text.strip()
        company = WebDriverWait(self.browser, 10).until(
            element_has_value((By.XPATH, companyPath))).text
        logging.info("company is "+company)

        durDatePath = '//*[@id="root"]//form/div[6]/div[1]/div/div[2]/div/span'
        # durDatePath = '//*[@class="min_tablehz"][2]//tr[3]/td[4]'
        result = self.browser.find_element(By.XPATH, durDatePath)
        durDate = result.text
        if durDate == "":
            logging.error("can not find durDate")
            # durDatePath = '(//*[@id="root"]//form)[2]/div[1]/div[1]/div/div[2]/div/span'
            durDatePath = '((//*[@id="root"]//form)[2]//*[@class="ant-form-item-children"])[1]'
            durDate = self.browser.find_element(By.XPATH, durDatePath).text
            logging.info("durDate is "+durDate)
        else:
            logging.info("durDate is "+durDate)

        durDate = util.compDate(durDate)

        # durDate = .text

        self.fullpath = f"./{self.curDate}/{durDate}-{id}-{company}"
        self.resultList.append(self.fullpath)
        self.exportHtml(self.browser.page_source, company)
        self.replace_html(company)

    # 修改html里面的样式
    def replace_html(self, company):
        filename = f'{self.fullpath}/{company}.html'
        source = "/srm/static/css/hzero-ui.07fa7e4b.chunk.css"
        target = "../../hzero-ui.css"
        util.replaceFile(filename, source, target)
        util.replaceFile(
            filename, 'style="max-width: 150px; min-width: 150px;"', "")

    def main(self):
        # totalPage=50
        pageSize = 20
        user_agent = UserAgent(verify_ssl=False).random
        token = self.browser.get_cookie("access_token")["value"]
        res = self.get_pages(1, pageSize, token)
        # print()
        # totalElements = 1
        totalElements = res['totalElements']

        logging.info(f"totalPage is {totalElements}")

        for i in util.getPage(int(totalElements), pageSize):
            logging.warning(
                f"current processing page {i},current no is {i*pageSize}")
            res = self.get_pages(i, pageSize, token)
            self.get_details(res)

        logging.info('#'*50)
        logging.info(f'总共处理记录数：{totalElements}')
        logging.info(f'总共过滤获得的记录数：{len(self.resultList)}')
        use_time = int(time.time()) - int(self.start_time)
        logging.info(f'爬取总计耗时：{use_time}秒')


if __name__ == '__main__':
    data = HuaCls()
    # data.strList.append("计量")
    # data.strList.append("水处理剂")
    data.main()
