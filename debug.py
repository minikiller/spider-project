from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

options=Options()
# options = webdriver.ChromeOptions()
from fake_useragent import UserAgent
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

user_agent = UserAgent(verify_ssl=False).random
options.add_experimental_option('debuggerAddress','127.0.0.1:9222')
# options.add_experimental_option("prefs", prefs)
options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 这里去掉window.navigator.webdriver的特性
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f'user-agent={user_agent}')
browser = webdriver.Chrome(options=options)

# print(browser)
url="https://cgsj.1688.com/page/supplier_home.htm"
browser.get(url)
browser.implicitly_wait(10)
btn=browser.find_element(By.XPATH,'//*[@id="right-side-col"]/div[1]/div[1]/div[1]/div/div[1]/div/a')
# print(btn)
btn.click()

browser.implicitly_wait(10)
btn1=browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/div/div/div/div[2]/div[2]/div[1]/ul/li[3]/a')
btn1.click() 



# browser.implicitly_wait(10)
# btn2=browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/div/div/div/div[2]/div[2]/div[1]/ul/li[4]/a')
# # print(btn2)
# btn2.click() 

# browser.implicitly_wait(10)
# btn3=browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/div/div/div/div[2]/div[2]/div[1]/ul/li[5]/a')
# # print(btn3)
# btn3.click() 

# print(browser.get_cookies())
# browser.implicitly_wait(20)
# WebDriverWait(browser, 10).until(
#             EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/div/div/div/div[2]/div[2]/div[1]/ul/li[6][@class='tabs__item actived']')))
#     )

# WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/div/div/div/div[2]/div[2]/div[1]/ul/li[6][@class='tabs__item actived']")))
data=WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,'//*[contains(@class, "tabs__item actived")]/a[@class="tabs__item-block"]')))
print("current data",data.text)
# data=browser.find_elements(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/div/div/div/div[2]/div[2]/div[2]/div[2]/ul')
# for value in data:
#     print(value.text)

data=browser.find_elements(By.XPATH,'//*[contains(@class, "card-item")]')
for value in data:
    print(value.text)

myurl="https://cgsj.1688.com/event/app/sourcing_supplier_opportunity_list/opportunity_list.json?tab=match&pageNum=1&pageSize=10"

secondUrl="https://cgsj.1688.com/event/app/sourcing_supplier_opportunity_list/opportunity_list.json?tab=buyersend&pageNum=1&pageSize=10"

# browser.get(myurl)



def get_cookies():
    cookies = {}
    selenium_cookies = browser.get_cookies()
    for cookie in selenium_cookies:
        cookies[cookie['name']] = cookie['value']
    return cookies

def get_posts():    
    cookies = get_cookies()
    response = requests.get(myurl, headers=cookies)
    return response.text

# data=get_posts()
# print(data)
#获取cookies  
# cookie_list = [item["name"] + "=" + item["value"] for item in browser.get_cookies()]  
  
# cookiestr = ';'.join(item for item in cookie_list)  

# cookies = {'Cookie':cookiestr}
# print(cookies)
           
# response = requests.get(myurl, cookies=cookies)
# print(response.text)
 
# browser.implicitly_wait(20)

# data=browser.find_elements(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/div/div/div/div[2]/div[2]/div[2]/div[3]/div/div/button')
# for value in data:
#     print(value.text)

