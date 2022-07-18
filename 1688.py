from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from lxml import etree
import codecs
from random import randint
import index,html,time

strList=index.getIndex()
curDate=html.getCurDate()
start_time = time.time()

options=Options()
# options = webdriver.ChromeOptions()
from fake_useragent import UserAgent
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

user_agent = UserAgent(verify_ssl=False).random
options.add_experimental_option('debuggerAddress','127.0.0.1:9222')
options.add_argument('window-size=1920x1080')
# options.add_experimental_option("prefs", prefs)
# options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 这里去掉window.navigator.webdriver的特性
# options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f'user-agent={user_agent}')
browser = webdriver.Chrome(options=options)

# print(browser)
url="https://cgsj.1688.com/page/supplier_home.htm"
browser.get(url)
browser.implicitly_wait(10)
btn=browser.find_element(By.XPATH,'//*[@id="right-side-col"]/div[1]/div[1]/div[1]/div/div[1]/div/a')
# print(btn)
btn.click()

original_window = browser.current_window_handle
total_link=[]

sleep(3)

# 平台优选 (103)
# btn1_path='/html/body/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/div/div/div/div[2]/div[2]/div[1]/ul/li[3]/a'
# btn1=WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, btn1_path)))
# btn1.click()

# 采购商邀请 (21)
# btn2_path='/html/body/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/div/div/div/div[2]/div[2]/div[1]/ul/li[4]/a'
# btn2=WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, btn2_path)))
# btn2.click()

# 自主订阅 (16)
btn3_path='/html/body/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/div/div/div/div[2]/div[2]/div[1]/ul/li[5]/a'
btn3=WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, btn3_path)))
btn3.click() 

data=WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,'//*[contains(@class, "tabs__item actived")]/a[@class="tabs__item-block"]')))
print("current data",data.text)
# data=browser.find_elements(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/div/div/div/div[2]/div[2]/div[2]/div[2]/ul')
# for value in data:
#     print(value.text)
sleep(3)
# page_text = browser.page_source
# html = etree.HTML(page_text)
# data=html.xpath('//*[@class="card-item"]')
# for value in data:
#     # print(value.text)
#     a_link = value.xpath('./div/div/header/h3/a')[0]
#     # print(class_title)
#     a_link.click()
def saveit(fileName ,html):
    file = codecs.open(fileName, "w", "utf−8")
    #obtain page source
    
    #write page source content to file
    file.write(html)

def saveImg(filename):
    browser.save_screenshot(filename+".png")

def get_material():
    # 物料名称
    vd='//*[@id="__react_content"]/div/div/div/div/section[1]/section/div/div[2]/div[2]/div/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div/div[3]/div/div[1]/div'
    sleep(randint(1,3))
    page_text = browser.page_source
    html = etree.HTML(page_text)
    title=html.xpath('//*[@id="__react_content"]/div/div/div/div/section[1]/header/div/div[1]/h1')
    if len(title)>0:
        print("##################",title[0].text)
        id=html.xpath('//*[@id="id"]/div/div')
        print("*************",id[0].text)
        datas=html.xpath(vd)
        for data in datas:
            print(data.text)
            if index.indexOfStr(data.text,strList):
                # js = 'window.scrollTo(0, document.body.scrollHeight)'
                # browser.execute_script(js)
                # sleep(1)
                filename=f'./{curDate}/{id[0].text}.html' # 创建文件
                # saveImg(filename)
                saveit(filename,page_text)
                break
    else:
        print("##################","没有标题")

def close_window():
    links=[]
    for handle in browser.window_handles:
        if handle != original_window:
            browser.switch_to.window(handle)
            # print(browser.current_url)
            get_material()
            links.append(browser.current_url)
            browser.close()
    browser.switch_to.window(original_window)
    return links

# 找到所有的a标签
def find_a_tags():
    # js = 'window.scrollTo(0, document.body.scrollHeight)'
    # browser.execute_script(js)
    # sleep(1)
    path='/html/body/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/div/div/div/div[2]/div[2]/div[2]/div[2]/ul/li/div/div/header/h3/a'

    data=browser.find_elements(By.XPATH,path)

    for d in data:
        d.click()
        sleep(1)
        link=close_window()
        total_link.extend(link)
    


def find_next_page(string):
    import re
    num=re.findall(r"\d+\.?\d*",string)
    count=int(num[0])//10   #获得总页数
    for i in range(count):
        path='/html/body/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/div/div/div/div[2]/div[2]/div[2]/div[3]/div/button[2]/span'
        page=browser.find_element(By.XPATH,path)
        print(i,"click it times")
        page.click()
        sleep(10)
        find_a_tags()
        # link=close_window()
        # total_link.extend(link)


find_a_tags()
link=close_window()
total_link.extend(link)
find_next_page(data.text)

print('总共处理记录数：',len(total_link))
use_time = int(time.time()) - int(start_time)
print("\n")
print(f'爬取总计耗时：{use_time}秒')

def saveHtml(fileName,my_tree):
    with open(fileName, 'wb') as f:
        f.write(etree.tostring(my_tree))

# lists=close_window()

def find_material():
    # 物料名称
    vd='//*[@id="__react_content"]/div/div/div/div/section[1]/section/div/div[2]/div[2]/div/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div/div[3]/div/div[1]/div'

    for index,list in enumerate(total_link):
        browser.get(list)
        sleep(randint(1,3))
        page_text = browser.page_source
        html = etree.HTML(page_text)
        datas=html.xpath(vd)
        for data in datas:
            print(data.text)
        filename='./'+str(index) 
        # saveit(filename,page_text)
        saveImg(filename)

# if __name__ == '__main__':
#     main()

