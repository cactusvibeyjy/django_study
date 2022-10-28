
from bs4 import BeautifulSoup
import matplotlib
import requests
import re
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt 
import os
from myproject03.settings import STATIC_DIR
 

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

