import requests
from bs4 import BeautifulSoup
import os
import json

BASE_DIR=os.path.dirname(os.path.abspath(__file__))

List=['com.ted.android', 'com.duolingo', 'org.khanacademy.android', 'air.nn.mobile.app.main']
url='https://play.google.com/store/apps/details?id='
url_list=[]
for l in List:
    url_list.append(url+str(l))
#print(url_list)

data=[]
for url in url_list:
    req=requests.get(url)
    html=req.content
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

    for item in zip(key, value):
            data.append(
                {
                    item[0].text : item[1].text.replace('\n', '/')
                    }
                )

    data.append({a_k[0].text : a_v[0].text}) 
    data.append({al_k[0].text : al_v[0].text})


    with open(os.path.join(BASE_DIR, 'TEDUOLINGOApp.json'), 'w+') as json_file:
        json.dump(data, json_file)
    
    
    
    
    


    