import requests
from bs4 import BeautifulSoup
import os
import json

BASE_DIR=os.path.dirname(os.path.abspath(__file__))

ran=range(1,21)
url='https://www.rottentomatoes.com/m/parasite_2019/reviews?type=&sort=&page='
url_list=[]
for r in ran:
    url_list.append(url+str(r))
#print(url_list)

movie_review=[]
for url in url_list:
    req=requests.get(url)
    html=req.content
    soup=BeautifulSoup(html, 'html.parser')
    
    name=soup.select('div.review_table > div > div.col-xs-8 > div.col-sm-13.col-xs-24.col-sm-pull-4.critic_name > a.unstyled.bold.articleLink')
    belong=soup.select('div.review_table > div > div.col-xs-8 > div.col-sm-13.col-xs-24.col-sm-pull-4.critic_name > a > em')
    review=soup.select('div.review_table > div > div.col-xs-16.review_container > div.review_area > div.review_desc > div.the_review')
    date=soup.select('div.review_table > div > div.col-xs-16.review_container > div.review_area > div.review-date.subtle.small')
    
    for item in zip(name, belong, review, date):
        movie_review.append(
            {
            'name' : item[0].text.replace('\n', '').replace('\t', '').replace('  ', ''),
            'belong' : item[1].text.replace('\n', '').replace('\t', '').replace('  ', ''),
            'review' : item[2].text.replace('\n', '').replace('\t', '').replace('  ', ''),
            'date' : item[3].text.replace('\n', '').replace('\t', '').replace('  ', '')
            }
        )
   
with open(os.path.join(BASE_DIR, 'parasite.json'), 'w+') as json_file:
    json.dump(movie_review, json_file)
    
    
    
    
    


    