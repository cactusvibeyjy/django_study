
from bs4 import BeautifulSoup
import folium
import matplotlib
import pandas as pd
import requests
import re
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt 
import os

import urllib.request
from myproject03.settings import STATIC_DIR, TEMPLATE_DIR
from wordcloud import WordCloud
from konlpy.tag import Okt
from collections import Counter
import numpy as np

def movierate(data):
    font_location="c:/Windows/fonts/malgun.ttf"
    reviews = data.dropna()
    reviews =reviews.drop_duplicates(['comment'])

    #print(reviews)
    # reviews.head(20)
    movie_list = reviews.title.unique()
    # print('전체 영화 편수 =', len(movie_list))
    # print(movie_list[:20])
    cnt_movie = reviews.title.value_counts() 
    cnt_movie[:20]
    info_movie = reviews.groupby('title')['score'].describe()
    info_movie.sort_values(by=['count'], axis=0, ascending=False)
    font_path = "C:/Windows/Fonts/malgunsl.ttf"
    font = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font)
    top20 = reviews.title.value_counts().sort_values(ascending=False)[:20]
    top20_title = top20.index.tolist()
    top20_reviews =reviews[reviews['title'].isin(top20_title)]
    movie_title = top20_reviews.title.unique().tolist()    #-- 영화 제목 추출
    avg_score = {}  #-- {제목 : 평균} 저장
    for t in movie_title:
        avg = top20_reviews[top20_reviews['title'] == t]['score'].mean()
        avg_score[t] = avg


    plt.cla()
    plt.figure(figsize=(30, 18))
    plt.title('영화 평균 평점 (top 20:)', fontsize=17)
    plt.xlabel('영화 제목',fontsize=12)
    plt.ylabel('평균 평점',fontsize=12)
    plt.xticks(rotation=70)

    for x, y in avg_score.items():
        color = np.array_str(np.where(y == max(avg_score.values()), 'orange', 'lightgrey'))    
        plt.bar(x, y, color=color)
        plt.text(x, y, '%.2f' % y, 
                horizontalalignment='center',  
                verticalalignment='bottom')    
   
    plt.legend()
    
    plt.savefig(os.path.join(STATIC_DIR, 'images\\movie_rate_bar_graph.png'), dpi=500)


#-- 그래프 마이너스 기호 표시 설정
import matplotlib
matplotlib.rcParams['axes.unicode_minus'] = False

def weather_crawling(last_date,forecast):
    
    req=requests.get('https://www.weather.go.kr/weather/forecast/mid-term-rss3.jsp?stnld=108')
    soup = BeautifulSoup(req.text, 'html.parser')
    # table = soup.find('table', {'class': 'table-col'})


        
    for i in soup.find_all('location'):
        forecast[i.find('city').text] = []
        for j in i.find_all('data'):
            tmp =[]
            if(len(last_date) ==0) or (j.find('tmef').text> last_date[0]['tmef']): 
                tmp.append(j.find('tmef').text)
                tmp.append(j.find('wf').text)
                tmp.append(j.find('tmn').text)
                tmp.append(j.find('tmx').text)
                forecast[i.find('city').string].append(tmp)
                print(last_date)

    print(forecast)

#날씨 크롤링
def weather_make_chart(result, wfs, dcounts):
    font_location="c:/Windows/fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_location).get_name()
    rc('font', family=font_name)
    high =[]
    low =[]
    xdata =[]

    for row in result.values_list():
        high.append(row[5])
        low.append(row[4])
        xdata.append(row[2].split('-')[2])
    plt.cla()
    plt.figure(figsize=(10,6))
    plt.plot(xdata, low, label='최저기온')
    plt.plot(xdata, high, label='최고기온')
    plt.legend()
    plt.savefig(os.path.join(STATIC_DIR, 'images\\weather_busan.png'), dpi=300)

    plt.cla()
    plt.bar(wfs, dcounts)
    plt.savefig(os.path.join(STATIC_DIR, 'images\\weather_bar.png'), dpi=300)


    plt.cla()
    plt.pie(dcounts, labels=wfs, autopct = '%.1f%%')
    plt.savefig(os.path.join(STATIC_DIR, 'images\\weather_pie.png'), dpi=300)

    image_dic = {
        'plot' : 'weather_busan.png',
        'bar' : 'weather_bar.png',
        'pie' : 'weather_pie.png'
        }
    return image_dic





#멜론 위크 차트 크롤링
def melon_crawling(datas):
    header = {'User-Agent': 'Mozilla/5.0'}
    req=requests.get('https://www.melon.com/chart/week/index.htm', headers = header)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    tbody = soup.select_one('#frm>div>table>tbody')

    trs=tbody.select("#lst50")
    for tr in trs [:10]:
        rank = tr.select_one("span.rank").get_text()
        #lst50 > td:nth-child(6) > div > div > div.ellipsis.rank01
        #lst50 > td:nth-child(4) > div > a > img
        imgs = tr.select_one("div > a > img").get
        name = re.sub('\n', '', tr.select_one("div.ellipsis.rank01").get_text())
        singer = re.sub('\n', '',tr.select_one("div.ellipsis.rank02>a").get_text())
        album =  re.sub('\n', '',tr.select_one("div.ellipsis.rank03 > a").get_text())
        # print('rank: ', rank)
        # print('name: ', name)
        # print('singer: ', singer)
        # print('album: ', album)
        tmp=dict()
        tmp['rank'] = rank
        tmp['imgs'] = imgs
        tmp['name'] = name
        tmp['singer'] = singer
        tmp['album'] = album
       
        datas.append(tmp)


def map(request):
    ex = {'경도' : [127.061026,127.047883,127.899220,128.980455,127.104071,127.102490,127.088387,126.809957,127.010861,126.836078
                ,127.014217,126.886859,127.031702,126.880898,127.028726,126.897710,126.910288,127.043189,127.071184,127.076812
                ,127.045022,126.982419,126.840285,127.115873,126.885320,127.078464,127.057100,127.020945,129.068324,129.059574
                ,126.927655,127.034302,129.106330,126.980242,126.945099,129.034599,127.054649,127.019556,127.053198,127.031005
                ,127.058560,127.078519,127.056141,129.034605,126.888485,129.070117,127.057746,126.929288,127.054163,129.060972],
     '위도' : [37.493922,37.505675,37.471711,35.159774,37.500249,37.515149,37.549245,37.562013,37.552153,37.538927,37.492388
              ,37.480390,37.588485,37.504067,37.608392,37.503693,37.579029,37.580073,37.552103,37.545461,37.580196,37.562274
              ,37.535419,37.527477,37.526139,37.648247,37.512939,37.517574,35.202902,35.144776,37.499229,35.150069,35.141176
              ,37.479403,37.512569,35.123196,37.546718,37.553668,37.488742,37.493653,37.498462,37.556602,37.544180,35.111532
              ,37.508058,35.085777,37.546103,37.483899,37.489299,35.143421],
     '구분' : ['음식','음식','음식','음식','생활서비스','음식','음식','음식','음식','음식','음식','음식','음식','음식','음식'
             ,'음식','음식','소매','음식','음식','음식','음식','소매','음식','소매','음식','음식','음식','음식','음식','음식'
             ,'음식','음식','음식','음식','소매','음식','음식','의료','음식','음식','음식','소매','음식','음식','음식','음식'
             ,'음식','음식','음식']}
    ex = pd.DataFrame(ex)
    print(ex)
    long =  ex['경도'].mean()
    lat = ex['위도'].mean()
    m = folium.Map([lat, long],zoom_start=8)
    for i in ex.index:
        sub_lat =ex.loc[i,'위도']
        sub_long= ex.loc[i,'경도']
    
        title = ex.loc[i,'구분']
    #지도에 데이터 찍어서 보여주기
        folium.Marker([sub_lat, sub_long], tooltip=title).add_to(m)
        m.save(os.path.join(TEMPLATE_DIR, 'bigdata/maptest.html'))


#워드클라우드이미지 띄우기
def make_wordCloud(data):
    data[0]['message']
    message = ''
    for item in data:
        print(item['message'])
    for item in data:
        if 'message' in item.keys():
            message = message + re.sub(r'[^\w]',' ', item['message'])+''
    nlp = Okt()
    message_N = nlp.nouns(message)
    count = Counter(message_N)
    # word_count = dict()
    word_count ={}
    for tag, counts in count.most_common(80):
        if(len(str(tag))>1):
            word_count[tag] = counts
        print("%s : %d" % (tag, counts))
    
    font_path="c:/Windows/fonts/malgun.ttf"
    wc =WordCloud(font_path, background_color ='ivory', width =800, height =600)
    cloud = wc.generate_from_frequencies(word_count)
    plt.figure(figsize=(8,8))
    plt.imshow(cloud)
    plt.axis('off')
    cloud.to_file('./static/images/kor_wordCloud.png')
    


