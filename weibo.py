# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author:小民 2019/6/29 20:41

# 用火狐selenium来登入微博
import time
from selenium import webdriver


opfs = webdriver.FirefoxProfile()
# 设置无头
# opts = webdriver.FirefoxOptions()
# opts.headless = True

# 关闭获取浏览器通知
opfs.set_preference("dom.webnotifications.enabled",False)

driver = webdriver.Firefox(executable_path='/home/pyvip/code/my_selenium/geckodriver', firefox_profile=opfs, firefox_options=opts)

driver.implicitly_wait(20)
driver.get('https://weibo.com/')

usename_ele = driver.find_element_by_id('loginname')




webdriver.ActionChains(driver).move_to_element(usename_ele).send_keys_to_element(usename_ele, '122064149@qq.com').perform()
time.sleep(1)

passwoed_ele = driver.find_element_by_name('password')
webdriver.ActionChains(driver).move_to_element(passwoed_ele).send_keys_to_element(passwoed_ele, 'pythonvip123').perform()
time.sleep(1)

submit_ele = driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a')
webdriver.ActionChains(driver).move_to_element(submit_ele).click().perform()

print(driver.page_source)
