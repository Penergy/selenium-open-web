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
    if(typeUrl == "light"):
        print("==================auto login ========================")
        sleep(2)
        print(driver.current_window_handle)
        username = driver.find_element_by_id('ssoId')
        password = driver.find_element_by_id('password')
        usernameStr = config.get("feilo-light","username")
        passwordStr = config.get("feilo-light","password")
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

    url =  config.get("frontpage", "default_tab")
    firefox_x_pos = config.get("firefox-setting", "x_position")
    firefox_y_pos = config.get("firefox-setting", "y_position")
    firefox_width = config.get("firefox-setting", "width")
    firefox_height = config.get("firefox-setting", "height")

    browser = webdriver.Firefox()
    browser.get('http://'+url)
    # sleep(5)
    cache[url] = browser.current_window_handle
    browser.set_window_position(firefox_x_pos, firefox_y_pos)
    browser.set_window_size(firefox_width,firefox_height)
    app.run(debug=False)
    
