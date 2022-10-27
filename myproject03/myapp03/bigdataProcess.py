from bs4 import BeautifulSoup
import requests
from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import urllib.request
import pandas as pd

path = "C:\\utility\\chromedriver.exe"
options = wd.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = wd.Chrome(path, options=options)
driver.implicitly_wait(2)
driver.get('https://www.melon.com/chart/week/index.htm')

tbody = driver.find_element(By.XPATH, '//*[@id="frm"]/div/table/tbody')
trs = tbody.find_elements(By.TAG_NAME, 'tr')
#ct > div.press_ranking_home > div:nth-child(3)
# //*[@id="ct"]/div[2]/div[2]

datas = []
for i in trs:
    rank = i.find_element(By.CLASS_NAME, 'rank').text
    title = i.find_element(By.CLASS_NAME,'wrap_song_info').find_element(By.TAG_NAME, 'a').text
    singer = i.find_element(By.CSS_SELECTOR,'div.rank02').find_element(By.TAG_NAME, 'a').text
    album = i.find_element(By.CSS_SELECTOR,'div.rank03').find_element(By.TAG_NAME, 'a').text
    likes = i.find_element(By.CLASS_NAME,'like').find_element(By.CLASS_NAME,'cnt').text
    likes = re.sub(',', '', likes)
    datas.append([rank, title, singer, album, likes])
print(datas)

melon_weekchart = pd.DataFrame(datas, columns=('순위', '곡명', '가수','앨범','좋아요'))
print(melon_weekchart)

