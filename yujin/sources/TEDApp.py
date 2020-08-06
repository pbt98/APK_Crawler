import requests
from bs4 import BeautifulSoup
import json
import os

BASE_DIR=os.path.dirname(os.path.abspath(__file__))

req=requests.get("https://play.google.com/store/apps/details?id=com.ted.android")
html=req.text
soup=BeautifulSoup(html, 'html.parser')
key=soup.select(
   '#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div > main > c-wiz:nth-child(4) > div.W4P4ne > div.JHTxhe.IQ1z0d > div > div > div.BgcNfc'
   )
value=soup.select(
    '#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div > main > c-wiz:nth-child(4) > div.W4P4ne > div.JHTxhe.IQ1z0d > div > div > span > div > span.htlgb'
    )
a_k=soup.select(
    '#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div > main > c-wiz:nth-child(4) > div.W4P4ne > div.JHTxhe.IQ1z0d > div > c-wiz > div > div'
    )
a_v=soup.select(
    '#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div > main > c-wiz:nth-child(4) > div.W4P4ne > div.JHTxhe.IQ1z0d > div > c-wiz > div > span > div > span > div > a'
    )
al_k=soup.select('#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div > main > c-wiz:nth-child(4) > div.W4P4ne > div.JHTxhe.IQ1z0d > div > div.JHTxhe.IQ1z0d.YjpPef > div > div')
al_v=soup.select('#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div > main > c-wiz:nth-child(4) > div.W4P4ne > div.JHTxhe.IQ1z0d > div > div.JHTxhe.IQ1z0d.YjpPef > div > span > div > span > a')
data=[]
for item in zip(key, value):
        data.append(
            {
            item[0].text : item[1].text.replace('\n', '/')
            }
        )

data.append({a_k[0].text : a_v[0].text}) 
data.append({al_k[0].text : al_v[0].text})

with open(os.path.join(BASE_DIR, 'TEDApp.json'), 'w+') as json_file:
    json.dump(data, json_file)
#print(data)