from selenium import webdriver
import urllib, sqlite3, subprocess, re, os, time, sys
from pyvirtualdisplay from Display
import configparser
import requests
import logging
from DBController import DBController

config = configparser.ConfigParser()
config.read('config.ini')
apk_directory = config.get('Setting', 'APK_DIRECTORY')
display = Display(visible = 0, size = (800, 600))
display.start()

chrome = webdriver.Chrome(config.get('Setting', 'CHROME_DRIVER_DIRECTORY'))
category_list = config.items('PlayStoreURL')

def get_new_applist(popurl):
    chrome.get(popurl)
    chrome.implicitly_wait(10)
    for scroll in (10000, 20000, 30000, 40000, 50000):
        chrome.execute_script("window.scrollTo(0, " + str(scroll) + ");")
        time.sleep(2)
    
    package_list = []
    div_app_list = chrome.find_elements_by_css_selector(".card.no-rationale.square-cover.apps.small")

    for div_app in div_app_list:
        app_detail = div_app.find_element_by_class_name('details')
        url = app_detail.find_element_by_class_name('title').get_attribute('href')
        package_name = url.split('id=')[1]
        package_list.append(package_name)
    
    return package_list
    
def get_app_detail(package_list):
    base_url = "https://play.google.com/store/apps/details?id="
    detail_list = []

    for package in package_list:
        app_url = base_url + package
        chrome.get(app_url)
        chrome.implicitly_wait(10)

        try:
            name = chrome.find_elements_by_css_selector('.id-app-title').text
            img_src = chrome.find_elements_by_css_selector('.cover-image').get_attribute('src')
            updated_date = chrome.find_elements_by_css_selector('.content')[0].text
        except:
            print("FATAL ERROR", package)
            continue

        detail_list.append([name, package, img_src, updated_date, False])

    return detail_list



for category in category_list:
    category_name = category[0]
    url = category[1]
    new_package_list = get_new_applist(url)
    updated_app_list = get_app_detail(package_list)
    print(updated_app_list)
