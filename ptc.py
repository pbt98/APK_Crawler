from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib, sqlite3, subprocess, re, os, time, sys
from pyvirtualdisplay import Display
import configparser
import requests
#import logging

config = configparser.ConfigParser()
config.read(r'config.ini')
#apk_directory = config.get('Setting', 'APK_DIRECTORY')
# display = Display(visible = 0, size = (800, 600))
# display.start()
chrome = webdriver.Chrome(executable_path = 'C:\chromedriver.exe' , chrome_options = Options().add_argument("--headless"))
category_list = config.items('PlayStoreURL')
db_directory = config.get('Setting', 'DB_DIRECTORY') # Recommend fill with your DB file's directory
conn=sqlite3.connect('test.db')
c=conn.cursor()
c.execute('''CREATE TABLE App
            (category text, name text, package text, img_src text, updated_date text)''')

def get_new_applist(popurl):
    chrome.get(popurl)
    chrome.implicitly_wait(10)
    more_detail_url = chrome.find_element_by_class_name("LkLjZd.ScJHi.U8Ww7d.xjAeve.nMZKrb.id-track-click").get_attribute("href");
    chrome.get(more_detail_url)
    chrome.implicitly_wait(10)
    for scroll in (10000, 20000, 30000):
        chrome.execute_script("window.scrollTo(0, " + str(scroll) + ");")
        time.sleep(2)
    
    package_list = []
    div_app_list = chrome.find_elements_by_class_name("JC71ub")

    for div_app in div_app_list:
        app_detail = div_app.get_attribute('href')
        package_name = app_detail.split('id=')[1]
        package_list.append(package_name)
    return package_list
    
def get_app_detail(category_name, package_list):
    base_url = "https://play.google.com/store/apps/details?id="
    detail_list = []

    for package in package_list:
        app_url = base_url + package
        chrome.get(app_url)
        chrome.implicitly_wait(10)

        try:
            name = chrome.find_element_by_class_name('AHFaub').text
            img_src = chrome.find_element_by_class_name('T75of.sHb2Xb').get_attribute('src')
            updated_date = chrome.find_element_by_class_name('htlgb').text
        except:
            print("FATAL ERROR", package)
            continue

        detail_list.append([category_name, name, package, img_src, updated_date]) #이게 각 패키지별 이름

    return detail_list

def go_to_database(detail_list):
    # https://docs.python.org/3/library/sqlite3.html --> Last week, You can fill the code with the material I gave last week. gogogo!
    
    
    c.executemany("insert into App(category, name, package, img_src, updated_date) values (?,?,?,?,?)", detail_list)
    conn.commit()
    return True

for category in category_list:
    category_name = category[0]
    url = category[1]
    new_package_list = get_new_applist(url)
    print(new_package_list)
    updated_app_list = get_app_detail(category_name, new_package_list)
    print(updated_app_list)
    go_to_database(updated_app_list)
    
conn.close()
chrome.close()
