# 国能E购
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


class Neep(object):

    def __init__(self) -> None:
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

        user_agent = UserAgent(verify_ssl=False).random
        options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
        options.add_argument(f'user-agent={user_agent}')
        self.browser = webdriver.Chrome(options=options)

        url = "https://www.neep.shop/dist/index.html#/purchaserNoticeIndex"
        self.browser.get(url)
        self.original_window = self.browser.current_window_handle
        self.total_link = []

        self.totalPage = 0
        self.pageSize = 20
        self.user_agent = UserAgent(verify_ssl=False).random
        self.cookies = util.get_cookies(self.browser)

    def close_window(self, inquiryCode):
        links = []
        for handle in self.browser.window_handles:
            if handle != self.original_window:
                self.browser.switch_to.window(handle)
                labelPath = '//*[@id="app"]/div/div[3]/div[2]/div[2]/div/div[1]/div/div/form/div[1]/div/label'
                tablePath = '//*[@id="app"]/div/div[3]/div[2]/div[2]/div/div[3]/div[2]/div/div[2]/table/tbody/tr/td[2]'

                # WebDriverWait(browser, 10).until(
                #     EC.presence_of_element_located((By.XPATH, tablePath)))

                WebDriverWait(self.browser, 20).until(EC.text_to_be_present_in_element(
                    (By.XPATH, labelPath), inquiryCode) and EC.presence_of_element_located((By.XPATH, tablePath)))
                projectNamePath = '//*[@id="app"]/div/div[3]/div[2]/div[2]/div/div[1]/div/div/form/div[2]/div/label'
                projectName = self.browser.find_element(By.XPATH, projectNamePath).text
                durDatePath = '//*[@id="app"]/div/div[3]/div[2]/div[2]/div/div[1]/div/div/form/div[7]/div/label'
                durDate = util.compDate(self.browser.find_element(
                    By.XPATH, durDatePath).text.strip())
                # source=browser.page_source
                self.fullpath = f'{self.curDate}/{durDate}-{projectName}-{inquiryCode}'
                self.exportHtml(self.browser.page_source,inquiryCode)
                # print(browser.current_url)
                links.append(self.browser.current_url)
                self.browser.close()
        self.browser.switch_to.window(self.original_window)
        return links

    def exportHtml(self, source,  inquiryCode):
        
        import os
        try:
            os.makedirs(self.fullpath, exist_ok=True)
        except OSError as error:
            logging.error(f'create dir error: {error}')
        with open(f'./{self.fullpath}/{inquiryCode}.html', "w") as f:
            f.write(source)
            logging.info(f"{inquiryCode} 保存成功")

    def getDetail(self, inquiryId, passkey):
        # cookies = util.get_cookies(browser)
        myurl = "https://www.neep.shop/rest/service/routing/inquiry/quote/encryptSupplierIqrPurchaseNoticeDetail"
        request_body = {"inquiryId": int(inquiryId),
                        "iqrSeq": 1, "purchaseCategory": 1}
        logging.debug(request_body)
        headers = {"User-Agent": self.user_agent, "Referer": "https: // www.neep.shop/dist/index.html",
                   'Content-Type': 'application/x-www-form-urlencoded', 'passkey': passkey}
        logging.debug(headers)
        response = requests.post(myurl, data=request_body,
                                 headers=headers, cookies=self.cookies)
        # sleep(randint(1,3))
        res = response.json()
        # for data in res['data']['attchmentInfo1']:
        #     logging.debug("attchmentInfo1")
        #     print(data['attachmentUrl'])
        #     print(data['attachmentName'])
        for data in res['data']['attchmentInfo2']:
            logging.debug("attchmentInfo2")
            logging.debug(data['attachmentUrl'])
            logging.debug(data['attachmentName'])

            util.downloadFile(data['attachmentUrl'],
                              self.fullpath + "/" + data['attachmentName'])
        # for data in res['data']['attchmentInfo3']:
        #     logging.debug("attchmentInfo3")
        #     print(data['attachmentUrl'])
        #     print(data['attachmentName'])
        # for data in res['data']['attchmentInfo4']:
        #     logging.debug("attchmentInfo4")
        #     print(data['attachmentUrl'])
        #     print(data['attachmentName'])

        # print(res)
    # 按照搜索条件进行搜索
    def search(self, value):
        myurl = "https://www.neep.shop/rest/service/routing/inquiry/quote/encryptSupplierQryIqrPurchaseNoticeList"
        request_body = {"pageNo": 1,
                        "pageSize": 50,
                        "inquiryName": value}
        headers = {"User-Agent": self.user_agent,
                   'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(myurl, data=request_body,
                                 headers=headers, cookies=self.cookies)
        # sleep(randint(1,3))
        res = response.json()
        logging.debug(res)
        count = res['data']['recordsTotal']
        # print(count)
        if count > 0:
            self.totalPage = self.totalPage+count
            logging.warning(f"'{value}'找到记录,共{count}条")
        else:
            logging.info(f"'{value}'没有找到记录")
            return 
        for data in res['data']['rows']:
            inquiryCode = data['inquiryCode']  # 询价单号
            inquiryId = data['inquiryId']
            inquiryName = data['inquiryName']
            if(inquiryName.find(value) > 1):  # 如果包含查询值
                passkey = data['passkey']
                detailUrl = f'https://www.neep.shop/dist/index.html#/purchaserNoticeDetail/1/{inquiryId}/1?backPage=purchaserNoticeIndex&joinable=true&receivedClarify=0&passkey={passkey}'
                # logging.info(f"{inquiryCode} {inquiryName} {detailUrl}")
                str = f"window.open('{detailUrl}');"
                # str = f"window.open('{detailUrl}','_blank');"
                logging.debug(str)
                self.browser.execute_script(str)
                # browser.implicitly_wait(10)
                # browser.tab_new(detailUrl)
                # browser.get(detailUrl)
                self.total_link.append(detailUrl)
                # sleep(3)
                # browser.get("http://sina.com")
                # print(browser.current_url)
                # sleep(3)

                self.close_window(inquiryCode)
                self.getDetail(inquiryId, passkey)
            else:
                self.totalPage = self.totalPage-1
                logging.warning(f"不包括查询值：'{value}'")

    # token = browser.get_cookie("X-AUTH-TOKEN")["value"]
    # print(token)
    # # res = get_posts(1, pageSize)
    # # print()
    # totalPage = 0

    def main(self):
        # self.search("液位计")

        for value in self.strList:
            sleep(randint(1, 3))
            self.search(value)

        # totalPage = res['totalCount']
        # for i in util.getPage(int(totalPage), pageSize):
        #     logging.info(f"current processing page {i},current no is {i*pageSize}")
        #     res = get_posts(i, pageSize)
        #     get_details(res)
        # with open('data.txt', 'w') as f:
        #     for item in total_link:
        #         # write each item on a new line
        #         f.write("%s\n" % item)
        logging.info('#'*50)
        logging.info(f'总共处理记录数：{len(self.strList)}')
        logging.info(f'总共过滤获得的记录数：{self.totalPage}')
        use_time = int(time.time()) - int(self.start_time)
        logging.info(f'爬取总计耗时：{use_time}秒')


if __name__ == '__main__':
    neep = Neep()
    neep.main()
