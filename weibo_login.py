#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


options = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_setting_values':
        {
            'notifications': 2
        }
}
options.add_experimental_option('prefs', prefs)  # 关掉浏览器左上角的通知提示，如上图
options.add_argument("disable-infobars")  # 关闭'chrome正受到自动测试软件的控制'提示
driver = webdriver.Chrome(chrome_options=options)
driver.maximize_window() #最大化窗口
driver.implicitly_wait(3) # 显示等待

driver.get("https://www.weibo.com")
time.sleep(2)
# driver.quit()

user = driver.find_element_by_id("loginname")
# pwd = driver.find_element_by_css_selector(".W_input")
# submit = driver.find_element_by_xpath("//*[@id='pl_login_form']/div/div[3]/div[6]/a")
# save_me = driver.find_element_by_id("login_form_savestate")


webdriver.ActionChains(driver).move_to_element(user).send_keys_to_element(user, '1092972423@qq.com').perform()
time.sleep(1)

passwoed_ele = driver.find_element_by_name('password')
webdriver.ActionChains(driver).move_to_element(passwoed_ele).send_keys_to_element(passwoed_ele, 'xl1229').perform()
time.sleep(1)

submit_ele = driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a')
webdriver.ActionChains(driver).move_to_element(submit_ele).click().perform()

print(driver.page_source)


# ActionChains(driver).move_to_element(user).send_keys('1092972423@qq.com').move_to_element(pwd).send_keys('xl1229').move_to_element(submit).click()
# driver.close()
time.sleep(10)
# driver.quit()


# # 打开谷歌浏览器
# driver = webdriver.Chrome()
# # 访问页面
# driver.get('http://www.python.org')
# # 获取属性name='q'的元素
# elem = driver.find_element_by_name('q')
# # 清空它的text值，如果它是一个可以输入text的元素
# elem.clear()
# # 模拟输入'pycon'
# elem.send_keys('pycon')
# # 模拟回车键进行搜索
# elem.send_keys(Keys.ENTER)
# # 关闭浏览器
# driver.close()