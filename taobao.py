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


class Login:
    def __init__(self, username, password):

        """

        Initialize browser configuration and login information

        """

        self.url ='https://login.taobao.com/member/login.jhtml'

        # Initialize browser options

        options = webdriver.ChromeOptions()

        # Prohibit loading pictures

        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

        # Set to developer mode

        options.add_experimental_option('excludeSwitches', ['enable-automation'])

        # Load browser options

        self.browser = webdriver.Chrome(options=options)

        # Set explicit waiting time 40s

        self.wait = WebDriverWait(self.browser, 40)

        self.username = username # username

        self.password = password # password


    def original(self):

        """

        Log in directly with Taobao account


        :return: None

        """

        self.browser.get(url=self.url)

        try:

            input_username = self.wait.until(EC.presence_of_element_located((

                By.CSS_SELECTOR,'div.fm-field> div.input-plain-wrap.input-wrap-loginid> input'

            )))

            input_password = self.wait.until(EC.presence_of_element_located((

                By.CSS_SELECTOR,'div.fm-field> div.input-plain-wrap.input-wrap-password> input'

            )))

            # Wait for the slider button to load

            div = self.wait.until(EC.presence_of_element_located((

                By.ID,'nc_1__bg'

            )))

            input_username.send_keys(self.username)

            input_password.send_keys(self.password)

            # Sleep for 2s, wait for the slider button to load

            time.sleep(2)

            # Click and hold the slider

            ActionChains(self.browser).click_and_hold(div).perform()

            # Move the slider

            ActionChains(self.browser).move_by_offset(xoffset=300, yoffset=0).perform()

            # Waiting for verification

            self.wait.until(EC.text_to_be_present_in_element((

                By.CSS_SELECTOR,'div#nc_1__scale_text> span.nc-lang-cnt> b'),'Verification passed'

            ))

            # log in

            input_password.send_keys(Keys.ENTER)

            print('Successful !')

        except TimeoutException as e:

            print('Error:', e.args)

            self.original()


    def sina(self):

        """

        Log in with Sina Weibo account (bind Sina account in advance)


        :return: None

        """

        self.browser.get(url=self.url)

        try:

            # Wait for Sina login link to load

            weibo_login = self.wait.until(EC.element_to_be_clickable((

                By.CSS_SELECTOR,'#login-form a.weibo-login'

            )))

            weibo_login.click()

            input_username = self.wait.until(EC.presence_of_element_located((

                By.CSS_SELECTOR,'div.info_list> div.inp.username> input.W_input'

            )))

            input_password = self.wait.until(EC.presence_of_element_located((

                By.CSS_SELECTOR,'div.info_list> div.inp.password> input.W_input'

            )))

            input_username.send_keys(self.username)

            input_password.send_keys(self.password)

            input_password.send_keys(Keys.ENTER)

            # Wait for the browser to save our information, if the network speed is not good, you can set a longer

            time.sleep(5)

            # refresh page

            self.browser.refresh()

            # Wait for the quick login button to load

            quick_login = self.wait.until(EC.element_to_be_clickable((

                By.CSS_SELECTOR,'div.info_list> div.btn_tip> a.W_btn_g'

            )))

            quick_login.click()

            print('login successful !')

        except TimeoutException as e:

            print('Error:', e.args)

            self.sina()

if __name__ == '__main__':
    username ='cc_lili@163.com' # Account"
    # _password=""
    password ='ccglyb2931147' # Password
    # Initialize the Login class
    login = Login(username, password)
    # Use Taobao account or mobile phone number to log in
    login.original()
# Login with Sina Weibo account
# login.sina()