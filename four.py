# -*- coding: utf-8 -*-
# 大唐集团公司 http://www.cdt-ec.com，账号密码：ccglyb/ccglyb2931147

from email import header
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time, re
from lxml import etree
from selenium.webdriver.chrome.options import Options

class Four():
    def callData(self,token,  pageNo):
        import requests
        url="https://buy.cdt-ec.com/bidprocurement/procurement-protproject/procurementProject/canParticipateInTheProjectPage"
        # Headers = { "X-AUTH-TOKEN" : token, "Content-Type": "application/json"}
        Headers = { "X-AUTH-TOKEN" : token, "Content-Type": "application/json","User-Agent": str(self.user_agent)}

        data={
            "tenderMethod": "11",
            "pageNo": pageNo,
            "pageSize": 10,
            "state": "01"
        }
        res=requests.post(url,json=data,headers=Headers)
        
        return res.json()

    def getInfo(self,token):
        import html,index
        date=html.getCurDate()
        strList=index.getIndex()
        res=self.callData(token,1)
        # print(res["data"])
        # total=res.data.total 
        pages=res["data"]["pages"]
        # pages=2

        for i in range(1,pages):
            res=self.callData(token,i)
            for j in res["data"]["records"]:
                packId=j["packId"]
                tenderNo=j["tenderNo"]
                print("packId is: ",packId)
                result=self.getDetail(token,packId)
                content=result["data"]["contentText"]
                print("content is: ",content)
                fileName=f"{date}/{tenderNo}.html"
                data=html.getResultContent(content) 
                for item in data:
                    print("开始处理字符串：",item.text)
                    if index.indexOfStr(item.text,strList):
                        html.exportHtml(content,fileName) 
                        html.outResultData(fileName)
                        break  
                time.sleep(1)

    def getDetail(self,token,packId):
        import requests
        url=f"https://buy.cdt-ec.com/bidprocurement/procurement-bulletin/procurementBulletin/viewProcurementBulletin?packId={packId}"
        Headers = { "X-AUTH-TOKEN" : token, "Content-Type": "application/json","User-Agent": str(self.user_agent)}
        
        res=requests.post(url,headers=Headers)
        # print(res.json())
        return res.json()

    def __init__(self):
        # options.add_argument("window-size=1400,600")
        from fake_useragent import UserAgent
        self.user_agent = UserAgent(verify_ssl=False).random
        self.header = {"User-Agent": {self.user_agent}}
        # self.agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        # header = {"User-Agent": str(self.user_agent)}
        print(self.user_agent)

    def main(self):
        # 开始时间
        start_time = time.time()
        _username="ccglyb"
        _password="ccglyb2931147"
        url="http://www.cdt-ec.com"
        # url="https://www.cdt-ec.com/cpu-portal-fe/login1.html"
        # ，账号密码：ccglyb/
        options = Options()
        
        options.add_argument(f'user-agent={self.user_agent}')
        options.add_experimental_option("detach", True)
        browser = webdriver.Chrome(options=options)
        # browser = webdriver.Chrome()
        try:
            browser.get(url)
            # nextBt = browser.find_element(By.XPATH,'//*[@id="ywmk"]/div[1]/div[2]')
            # nextBt.click()
            # /html/body/div[3]/div[2]/ul[2]/button[3]
            login=browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/ul[2]/button[3]')
            login.click()
            # login=browser.find_element(By
            # .CSS_SELECTOR,'button.loginloginapply').click()
            # first = browser.find_element(By.ID,'z-1495258397423').click()
            # //*[@id="uid"]
            # browser.implicitly_wait(10)
            original_window = browser.current_window_handle

            username = browser.find_element(By.ID,'username')
            # username = browser.find_element((By.XPATH,'//*[@id="uid"]'))
            password = browser.find_element(By.ID,'password')
            # password = browser.find_element((By.XPATH,'//*[@id="kl"]'))
            # code = browser.find_element(By.ID,'checkCode')  //*[@id="kl"]
            # code=input("please input:")
            username.send_keys(_username)  
            password.send_keys(_password)  
            # print(code)
            
            # inputCode = browser.find_element(By.ID,'randCode')
            # inputCode.send_keys(code)  
            loginBt = browser.find_element(By.XPATH,'//*[@id="submit_btn_login"]')
        # //*[@id="submit_btn_login"]
            loginBt.click()
            # time.sleep(1)
            # browser.implicitly_wait(10)
            # print(browser.get_cookies())

            # js = 'window.scrollTo(0, document.body.scrollHeight)'
            # browser.execute_script(js)
            # time.sleep(1)

            # https://buy.cdt-ec.com/bidweb/#/procurement/procurementDesktopSupplier
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ywmk"]/div[1]/div[2]/a')))
        # //*[@id="ywmk"]/div[1]/div[2]/a
        # //*[@id="ywmk"]/div[1]/div[2]
        # //*[@id="ywmk"]/div[1]/div[2]
            # nextBt = browser.find_element(By.XPATH,'//*[@id="ywmk"]/div[1]/div[2]/a/div/div')
            browser.execute_script("window.open(document.location.protocol+'//buy.cdt-ec.com/bidprocurement/datacenter-dangtfz/dtLoginCenterController/ssoRedirectUrl?loginType=USER','_blank')")

            # nextBt = browser.find_element(By.XPATH,'//*[@id="ywmk"]/div[1]/div[2]/a')
            # //*[@id="ywmk"]/div[1]/div[2]/a
            # nextBt.click()
            # nextBt.send_keys(Keys.CONTROL + Keys.RETURN)
            # handles = browser.window_handles
            # browser.switch_to.window(handles[1])
            # browser.implicitly_wait(10)
            # .send_keys(Keys.ENTER)
            # wait = WebDriverWait(browser, 10)
            # # wait.until(EC.presence_of_element_located((By.CLASS_NAME, ' projectNo')))
            # wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr[1]/td[1]')))
            # print(browser.current_url)
            # print(browser.get_cookies())
            # print(browser.page_source)
            # curUrl="https://buy.cdt-ec.com/bidweb/#/procurement/procurementDesktopSupplier"
            # browser.get(curUrl)
            # 大唐电子商务平台非招标采购平台 lambda x: 'Page 1' in driver.title
            # Wait for the new window or tab
            # Store the ID of the original window
            WebDriverWait(browser, 10).until(EC.number_of_windows_to_be(2))

            # Loop through until we find a new window handle
            for window_handle in browser.window_handles:
                if window_handle != original_window:
                    browser.switch_to.window(window_handle)
                    break
            wait = WebDriverWait(browser, 10).until( lambda x:  "大唐电子商务平台非招标采购平台" in browser.title)
            # wait = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr[1]/td[1]')))
            # EC.title_contains("Page 1")
            # href = html.xpath('//*[@class="wrap m-test5-wrap f-pr f-cb"]/a/@href')
            # print(href)    
            # url="https://buy.cdt-ec.com/bidweb/#/procurement/enquiryPaticipation"
            # browser.get(url)
            # browser.implicitly_wait(10)
            page_text = browser.page_source
            # print(browser.get_cookies())
            html = etree.HTML(page_text)
            token=browser.get_cookie("X-AUTH-TOKEN")["value"]
            print(token)
            print(browser.current_url)
            # data=callData(token,10)
            self.getInfo(token)
            # print(data)
        finally:
            browser.close()
            use_time = int(time.time()) - int(start_time)
            print(f'爬取总计耗时：{use_time}秒')
            pass
if __name__ == '__main__':
    data=Four()
    data.main()
    # pass
