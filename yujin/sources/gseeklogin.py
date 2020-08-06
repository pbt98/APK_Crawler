from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pyperclip
from bs4 import BeautifulSoup


driver=webdriver.Chrome('./chromedriver')
driver.implicitly_wait(3)

driver.get('https://www.gseek.kr/memb/login')
tag_id=driver.find_element_by_xpath('//*[@id="ID"]')
tag_pw=driver.find_element_by_xpath('//*[@id="PW"]')
#tag_id.clear()
time.sleep(1)

tag_id.click()
pyperclip.copy('ID')
tag_id.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

tag_pw.click()
pyperclip.copy('PW')
tag_pw.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

login_btn=driver.find_element_by_xpath('//*[@id="frmLog2"]/div/div/div[5]/button')
login_btn.click()




