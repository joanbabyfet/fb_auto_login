from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import configparser

# 检查元素是否存在
def check_element_exists(browser, element, condition):
    try:
        if condition == 'class':
            browser.find_element(By.CLASS_NAME, element)
        elif condition == 'id':
            browser.find_element(By.ID, element)
        elif condition == 'xpath':
            browser.find_element(By.XPATH, element)
        return True
    except Exception as e:
        return False

def main():
    url = 'https://www.facebook.com'

    conf = configparser.ConfigParser()
    conf.read('config.ini', encoding='utf-8') # 这里要加utf-8, 否则会报错, 默认gbk
    config_section  = 'fb_config'
    username = conf.get(config_section, 'username') # 帐号
    password = conf.get(config_section, 'password') # 密码
    target_url = conf.get(config_section, 'target_url')

    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)  # 不自动关闭浏览器
    options.add_experimental_option('prefs', { 
        "profile.default_content_setting_values.notifications": 2 # 防止跳出通知
    })
    #browser = webdriver.Chrome('./chromedriver', options = options) # 实例化
    browser = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)
    browser.maximize_window() # 窗口最大化
    browser.get(url)

    # 登入
    browser.find_element(By.ID, 'email').send_keys(username)
    browser.find_element(By.ID, 'pass').send_keys(password)
    browser.find_element(By.NAME, 'login').click()
    sleep(3)

    # 检测是否被挡下
    if check_element_exists(browser, '//*[contains(text(), "你的帳號暫時被鎖住")]', 'xpath'):
        browser.find_element(By.XPATH, '//*[contains(text(), "是")]').click()

    # 切换页面
    browser.get(target_url)

if __name__ == '__main__':
    main()