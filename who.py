from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

option = webdriver.ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 这里去掉window.navigator.webdriver的特性
option.add_argument("--disable-blink-features=AutomationControlled")   # 屏蔽webdriver特征
browser = webdriver.Chrome(options=option)
browser.get('http://www.taobao.com')
browser.maximize_window()
button = WebDriverWait(browser, timeout=30).until(EC.presence_of_element_located((By.CLASS_NAME, 'h')))
button.click()
username_sender = WebDriverWait(browser, timeout=30).until(EC.presence_of_element_located((By.ID, 'fm-login-id')))
username_sender.send_keys("cc_lili@163.com")
password_sender=WebDriverWait(browser, timeout=30).until(EC.presence_of_element_located((By.ID, 'fm-login-password')))
password_sender.send_keys("ccglyb2931147")
sleep(3)
try:
    browser.switch_to.frame(0)
    # 找到滑块
    slider = browser.find_element_by_xpath("//span[contains(@class, 'btn_slide')]")
    # 判断滑块是否可见
    if slider.is_displayed():
        # 点击并且不松开鼠标
        ActionChains(browser).click_and_hold(on_element=slider).perform()
        # 往右边移动258个位置
        ActionChains(browser).move_by_offset(xoffset=258, yoffset=0).perform()
        # 松开鼠标
        ActionChains(browser).pause(0.5).release().perform()
        browser.switch_to.default_content()
except:
    pass
button = WebDriverWait(browser, timeout=30).until(EC.presence_of_element_located((By.CLASS_NAME, 'password-login')))
button.click()
sleep(3)
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
# /html/body/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/div/div/div/div[2]/div[2]/div[2]/div[2]/ul/li[1]/div/div/header/h3
# WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/div/div/div/div[2]/div[2]/div[1]/ul/li[6][@class='tabs__item actived']")))
# std='/html/body/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/div/div/div/div[2]/div[2]/div[2]/div[2]/ul/li[1]/div/div/header/h3'
# std1="//h3[starts-with(@title,'设备')]"
# data=WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,std1)))
# # data=WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,'//*[contains(@class, "tabs__item actived")]/a[@class="tabs__item-block"]')))
# print("current data",data.text)
# data=browser.find_elements(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/div/div/div/div[2]/div[2]/div[2]/div[2]/ul')
# for value in data:
#     print(value.text)
sleep(3)
# browser.implicitly_wait(20)
data=browser.find_elements(By.XPATH,'//*[contains(@class, "card-item")]')
print("size is ",len(data))
for value in data:
    print(value.text)

data=browser.find_elements(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/div/div/div/div[2]/div[2]/div[2]/div[3]/div/div/button')
for value in data:
    print(value.text)