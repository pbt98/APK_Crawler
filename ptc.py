from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sqlite3
import configparser
import os
import requests

config = configparser.ConfigParser()
config.read(r'config.ini')
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
    c.executemany("insert into App(category, name, package, img_src, updated_date) values (?,?,?,?,?)", detail_list)
    conn.commit()
    return True

def download_apk(package_name, name):
    download_url = "https://apkpure.com/kr/" + name + "/" + package_name +  "/download?from=details"
    file_name = str(package_name) + '.apk'
    # timout 1분으로 설정하여 반응이 없는 것들은 예외처리
    try:
        r = requests.get(download_url, timeout=60)
        # apk directory에 패키지이름.apk 형태로 저장
        with open(file_name,'wb') as apk:
            apk.write(r.content)
    except requests.exceptions.Timeout as e:
        print('time out')
        return False
    except Exception as e:
        print(e)
        return False
    return True

for category in category_list:
    category_name = category[0]
    url = category[1]
    new_package_list = get_new_applist(url)
    print(new_package_list)
    updated_app_list = get_app_detail(category_name, new_package_list)
    for parameter in updated_app_list:
        package = parameter[2]
        name = parameter[1]
        try:
            download_apk(package_name, name)
        except Exception as e:
            print(e)
            continue
    print(updated_app_list)
    go_to_database(updated_app_list)
    
conn.close()
chrome.close()
