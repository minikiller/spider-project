# totalPage=305
# # pageSize=50

# # data=totalPage//pageSize
# # if (totalPage%pageSize)>0:
# #     data=data+1
# # for i in range(1,data+1):
# #     print(i)
# # import requests

# # myurl="https://b2b.crpower.com.cn/ispweb/pcux5PonHeaders/searchWinningList.do"
# # request_body= {"data":
# #                 '{"sourceMethods":"公开", "sourceStatus":"ACTIVE", "queryAll":"", "sourceTypeTag":"WZ","startDate":"2022-07-16", "endDate":"2022-07-18"}',
# #                 "take": 20,
# #                 "skip": 0,
# #                 "page": 1,
# #                 "pageSize": 20}
# # from fake_useragent import UserAgent
# # user_agent = UserAgent(verify_ssl=False).random
# # headers = {"User-Agent": user_agent,'Content-Type': 'application/x-www-form-urlencoded'}
# # response = requests.post(myurl, data=request_body,headers=headers)
# # print(response.json())

# import html
# import json
# endDate = html.getToDate()
# startDate = html.getYesDate()
# print(endDate)
# print(startDate)
# query = {"sourceMethods": "公开",
#          "sourceStatus": "ACTIVE",
#          "queryAll": "",
#          "sourceTypeTag": "WZ",
#          "startDate":  startDate,
#          "endDate": endDate}

# str = json.dumps(query)

# # query='{"sourceMethods":"公开", "sourceStatus":"ACTIVE", "queryAll":"", "sourceTypeTag":"WZ","startDate":'+ startDate+', "endDate":'+'endDate'

# print(str)

# import logger
# logger.info('#'*50)

# import requests
# url = 'https://ebid.espic.com.cn/bidprocurement/common-tools/tools/commonUpload/readImageRoot?imagePath=service_procurement_bulletin/bulletin_template_pdf_base/2022-07/fe5cfef85ae94ddbaa303df5cf111b37/e7db7a7323d74bd9ae984cc3bd189f1c.pdf'
# r = requests.get(url, allow_redirects=True)
# open('facebook.pdf', 'wb').write(r.content)

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



file1 = open('./data.txt', 'r')
Lines = file1.readlines()
# print(Lines)

options = Options()
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

# user_agent = UserAgent(verify_ssl=False).random
options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
# options.add_argument(f'user-agent={user_agent}')
browser = webdriver.Chrome(options=options)
original_window = browser.current_window_handle

def close_window():
    links = []
    index=0
    for handle in browser.window_handles:
        if handle != original_window:
            browser.switch_to.window(handle)
            sleep(3)
            index=index+1
            # print(browser.current_url)
            # tablePath = '//*[@id="app"]/div/div[3]/div[2]/div[2]/div/div[3]/div[2]/div/div[2]/table/tbody/tr/td[2]'

            # WebDriverWait(browser, 20).until(
            #     EC.presence_of_element_located((By.XPATH, tablePath)))
            # browser.close()
            with open(f'./{curDate}/{curDate}{index}.html', "w") as f:
                f.write(browser.page_source)
            # logger.info(f"{inquiryCode}保存成功")
            browser.close()
    browser.switch_to.window(original_window)
    return links
import html
curDate = html.getCurDate()
for index,list in enumerate(Lines):
    # print(list)
    str1 = list.strip()
    str = f"window.open('{str1}');"
    print(str)
    browser.execute_script(str)
    # browser.get(list)
    browser.implicitly_wait(10)
    # sleep(10)
close_window()
    
