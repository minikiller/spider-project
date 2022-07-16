# -*- coding: utf-8 -*-
"""
@author:Pineapple

@contact:cppjavapython@foxmail.com

@time:2020/7/28 9:09

@file:login.py

@desc: login taobao.
"""

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
import time

browser = webdriver.Chrome()

url = "https://login.taobao.com/member/login.jhtml"
browser.get(url)
browser.maximize_window()  # 最大化

# 填写用户名密码
user = 'cc_lili@163.com'
password = 'ccglyb2931147'
# username ='' # Account"
# _password=""
# password ='' # Password
time.sleep(8)

iframe = browser.find_element(By.XPATH,'//div[@class="bokmXvaDlH"]//iframe')
print(iframe)
browser.switch_to.frame(iframe)
browser.find_element(By.XPATH,'//*[@id="fm-login-id"]').send_keys(id)
browser.find_element(By.XPATH,'//*[@id="fm-login-password"]').send_keys(password)
time.sleep(2)
# 获取滑块的大小
span_background = browser.find_element(By.XPATH,'//*[@id="nc_1__scale_text"]/span')
span_background_size = span_background.size
print(span_background_size)

# 获取滑块的位置
button = browser.find_element(By.XPATH,'//*[@id="nc_1_n1z"]')
button_location = button.location
print(button_location)

# 拖动操作：drag_and_drop_by_offset
# 将滑块的位置由初始位置，右移一个滑动条长度（即为x坐标在滑块位置基础上，加上滑动条的长度，y坐标保持滑块的坐标位置）
x_location = span_background_size["width"]
y_location = button_location["y"]
print(x_location, y_location)
action = ActionChains(browser)
source = browser.find_element(By.XPATH,'//*[@id="nc_1_n1z"]')
action.click_and_hold(source).perform()
action.move_by_offset(300, 0)
action.release().perform()
time.sleep(1)

# 登录
browser.find_element(By.XPATH,'//*[@id="login-form"]/div[4]/button').click()
print('登录成功\n')