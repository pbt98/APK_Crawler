from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pyperclip
from bs4 import BeautifulSoup


driver=webdriver.Chrome('./chromedriver')
driver.implicitly_wait(3)

driver.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
tag_id=driver.find_element_by_name('id')
tag_pw=driver.find_element_by_name('pw')
tag_id.clear()
time.sleep(1)

tag_id.click()
pyperclip.copy('my_id')
tag_id.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

tag_pw.click()
pyperclip.copy('my_pw')
tag_pw.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

login_btn=driver.find_element_by_xpath('//*[@id="log.login"]')
login_btn.click()

driver.find_element_by_xpath('//*[@id="new.dontsave"]').click()

driver.get('https://order.pay.naver.com/home?tabMenu=POINT_TOTAL')
html=driver.page_source
soup=BeautifulSoup(html, 'html.parser')
date=soup.select('#_listContentArea > ul > li > div > div.item_content > div.info_space > span')
name=soup.select('#_listContentArea > ul > li > div > div.item_content > div.info_space > strong')
place=soup.select('#_listContentArea > ul > li > div > div.item_content > div.info_space > p')

data=[]

for item in zip(date, name, place):
    data.append(
        [
            item[0].text,
            item[1].text,
            item[2].text
            ]
        )
    
print(data)
