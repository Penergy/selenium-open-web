#!flask/bin/python
from flask import Flask, send_from_directory
from flask import jsonify
from flask import g
from flask import request
import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from time import sleep 
import sys
import os
import configparser
import logging


app = Flask(__name__)
browser = None
cache = {}
currentHandle = None
config = configparser.ConfigParser()
config.read("ini.conf")

def getTab(handles):
    global cache
    for key in cache:
        if(cache[key] in handles):
            handles.remove(cache[key])
    return handles[0]

def autoLogin(typeUrl,driver):
    # global browser
    print(typeUrl)
    print("==================auto login ========================")
    if(typeUrl == "light"):
        print(driver.current_window_handle)
        username = driver.find_element_by_id('ssoId')
        password = driver.find_element_by_id('password')
        usernameStr = config.get("feilo-light","username")
        passwordStr = config.get("feilo-light","password")
        username.clear()
        username.send_keys( usernameStr)
        password.clear()
        password.send_keys( passwordStr)
    elif(typeUrl == "waste-oil"):
        print(driver.current_window_handle)
        username = driver.find_element_by_id('userid')
        password = driver.find_element_by_id('pwd')
        usernameStr = config.get("waste-oil","username")
        passwordStr = config.get("waste-oil","password")
        username.clear()
        username.send_keys( usernameStr)
        password.clear()
        password.send_keys( passwordStr)
    elif(typeUrl == "quick-test"):
        print(driver.current_window_handle)
        username = driver.find_element_by_id('userid')
        password = driver.find_element_by_id('pwd')
        usernameStr = config.get("quick-test","username")
        passwordStr = config.get("quick-test","password")
        username.clear()
        username.send_keys( usernameStr)
        password.clear()
        password.send_keys( passwordStr)
    elif(typeUrl == "second-water-supply"):
        print(driver.current_window_handle)
        username = driver.find_element_by_id('input-user')
        password = driver.find_element_by_id('input-password')
        usernameStr = config.get("second-water-supply","username")
        passwordStr = config.get("second-water-supply","password")
        username.clear()
        username.send_keys( usernameStr)
        password.clear()
        password.send_keys( passwordStr)
        
@app.before_request
def before_request():
    global browser
    print("++++++++++++++++ before request ++++++++++++++++++++")
    data = request.values.get('url')
    pathValue = request.path
    pathArray = pathValue.split("/")
    print("++++++++++++++++++++++++++++++++++++")
    if((pathArray[1] == 'page') and (pathArray[2] != "") and (data in cache)):
        tabToCheck = cache[data]
        if(not(tabToCheck in browser.window_handles)):
            # delete url in "cache"
            del cache[data]

@app.route('/')
def index():
    app.logger.info('info log')
    app.logger.warning('warning log')
    return app.send_static_file('index.html')

@app.route('/_get_current_user')
def get_current_user():
    return jsonify(username="pengyc",
                   email="@gmail.com",
                   id="tt")

@app.route('/page/<string:url>')
def page(url):
    global browser
    global cache
    global currentHandle
    data = request.values.get('url')
    print(data)
    if(data in cache):
        browser.switch_to.window(cache[data])
        print("=========== old URL============")
        if(not(currentHandle in browser.window_handles)):
            print('test')
            browser.switch_to.window(browser.window_handles[0])
        currentHandle = browser.current_window_handle
    else:
        # print("=========== current window =================")
        if(not(currentHandle in browser.window_handles)):
            browser.switch_to.window(browser.window_handles[0])
        browser.execute_script("window.open('http://"+data+"')")
        # cache[url] = browser.window_handles[count]
        cache[data] = getTab(browser.window_handles)
        print("=========== new URL============")
        print(cache)
        browser.switch_to.window(cache[data])
        currentHandle = browser.current_window_handle
        print(currentHandle)
        print(cache[data])
    
    autoLogin(url,browser)
    return 'page %s' % data

"""
url：            http://xxx.xxx.xxx.xxx/page1,
description:     通过该链接打开istack平台、食品溯源二维码、智能路灯、废弃油脂四个平台

"""
@app.route('/page1')
def page1():
    global browser
    # 第一个浏览器打开：istack
    url =  config.get("istack", "url")
    x_pos = config.get("browser-win-1", "x_position")
    y_pos = config.get("browser-win-1", "y_position")
    width = config.get("browser-win-1", "width")
    height = config.get("browser-win-1", "height")
    
    browser = webdriver.Firefox()
    browser.get('http://'+url)
    # sleep(5)
    cache[url] = browser.current_window_handle
    browser.set_window_position(x_pos, y_pos)
    browser.set_window_size(width,height)

    # 第二个浏览器打开：
    url =  config.get("food-trace-qr", "url")
    x_pos = config.get("browser-win-2", "x_position")
    y_pos = config.get("browser-win-2", "y_position")
    width = config.get("browser-win-2", "width")
    height = config.get("browser-win-2", "height")
    
    browser = webdriver.Firefox()
    browser.get('http://'+url)
    # sleep(5)
    cache[url] = browser.current_window_handle
    browser.set_window_position(x_pos, y_pos)
    browser.set_window_size(width,height)

    # 第三个浏览器打开：
    url =  config.get("feilo-light", "url")
    x_pos = config.get("browser-win-3", "x_position")
    y_pos = config.get("browser-win-3", "y_position")
    width = config.get("browser-win-3", "width")
    height = config.get("browser-win-3", "height")
    
    browser = webdriver.Firefox()
    browser.get('http://'+url)
    # sleep(5)
    cache[url] = browser.current_window_handle
    browser.set_window_position(x_pos, y_pos)
    browser.set_window_size(width,height)
    autoLogin('light',browser)

    # 第四个浏览器打开：
    url =  config.get("waste-oil", "url")
    x_pos = config.get("browser-win-4", "x_position")
    y_pos = config.get("browser-win-4", "y_position")
    width = config.get("browser-win-4", "width")
    height = config.get("browser-win-4", "height")
    
    browser = webdriver.Firefox()
    browser.get('http://'+url)
    # sleep(5)
    cache[url] = browser.current_window_handle
    browser.set_window_position(x_pos, y_pos)
    browser.set_window_size(width,height)
    autoLogin('waste-oil',browser)
    return 'page 1'

"""
url：            http://xxx.xxx.xxx.xxx/page2,
description:     通过该链接打开istack平台、食品溯源二维码、智能路灯、废弃油脂四个平台

"""
@app.route('/page2')
def page2():
    global browser
    # 第一个浏览器打开：istack
    url =  config.get("quick-test", "url")
    x_pos = config.get("browser-win-1", "x_position")
    y_pos = config.get("browser-win-1", "y_position")
    width = config.get("browser-win-1", "width")
    height = config.get("browser-win-1", "height")
    
    browser = webdriver.Firefox()
    browser.get('http://'+url)
    # sleep(5)
    cache[url] = browser.current_window_handle
    browser.set_window_position(x_pos, y_pos)
    browser.set_window_size(width,height)
    autoLogin('quick-test',browser)

    # 第二个浏览器打开：
    url =  config.get("second-water-supply", "url")
    x_pos = config.get("browser-win-2", "x_position")
    y_pos = config.get("browser-win-2", "y_position")
    width = config.get("browser-win-2", "width")
    height = config.get("browser-win-2", "height")
    
    browser = webdriver.Firefox()
    browser.get('http://'+url)
    # sleep(5)
    cache[url] = browser.current_window_handle
    browser.set_window_position(x_pos, y_pos)
    browser.set_window_size(width,height)
    autoLogin('second-water-supply',browser)

    # 第三个浏览器打开：
    url =  config.get("mooc-edu", "url")
    x_pos = config.get("browser-win-3", "x_position")
    y_pos = config.get("browser-win-3", "y_position")
    width = config.get("browser-win-3", "width")
    height = config.get("browser-win-3", "height")
    
    browser = webdriver.Firefox()
    browser.get('http://'+url)
    # sleep(5)
    cache[url] = browser.current_window_handle
    browser.set_window_position(x_pos, y_pos)
    browser.set_window_size(width,height)
    # autoLogin('light',browser)

    # 第四个浏览器打开：
    url =  config.get("smart-water-supply", "url")
    x_pos = config.get("browser-win-4", "x_position")
    y_pos = config.get("browser-win-4", "y_position")
    width = config.get("browser-win-4", "width")
    height = config.get("browser-win-4", "height")
    
    browser = webdriver.Firefox()
    browser.get('http://'+url)
    # sleep(5)
    cache[url] = browser.current_window_handle
    browser.set_window_position(x_pos, y_pos)
    browser.set_window_size(width,height)
    # autoLogin('waste-oil',browser)

    return 'page 2'

@app.route('/closeFirefox')
def closeFirefox():
    cmd = "taskkill /IM firefox.exe"
    p=os.popen(cmd)
    return p.read()

@app.route('/smartcity')
def smartcity():
    global browser
    # 第一个浏览器打开：istack
    url =  config.get("smart-city", "url")
    x_pos = config.get("full-screen", "x_position")
    y_pos = config.get("full-screen", "y_position")
    width = config.get("full-screen", "width")
    height = config.get("full-screen", "height")
    
    browser = webdriver.Firefox()
    browser.get('http://'+url)
    # sleep(5)
    cache[url] = browser.current_window_handle
    browser.set_window_position(x_pos, y_pos)
    browser.set_window_size(width,height)
    return "smart-city go!!!"

@app.route('/min')
def min():
    global browser
    firefox_x_min = config.get("firefox-setting", "win_min_x")
    firefox_y_min = config.get("firefox-setting", "win_min_y")
    browser.set_window_position(0, 0)
    return 'min'

@app.route('/max')
def max():
    global browser
    firefox_x_pos = config.get("firefox-setting", "x_position")
    firefox_y_pos = config.get("firefox-setting", "y_position")
    browser.set_window_position(firefox_x_pos, firefox_y_pos)
    return 'max'

if __name__ == '__main__':
    handler = logging.FileHandler('flask.log', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)

    # url =  config.get("frontpage", "default_tab")
    # firefox_x_pos = config.get("firefox-setting", "x_position")
    # firefox_y_pos = config.get("firefox-setting", "y_position")
    # firefox_width = config.get("firefox-setting", "width")
    # firefox_height = config.get("firefox-setting", "height")

    # # browser = webdriver.Chrome()
    # browser = webdriver.Firefox()
    # browser.get('http://'+url)
    # # sleep(5)
    # cache[url] = browser.current_window_handle
    # browser.set_window_position(firefox_x_pos, firefox_y_pos)
    # browser.set_window_size(firefox_width,firefox_height)

    app.run(debug=False)
    
