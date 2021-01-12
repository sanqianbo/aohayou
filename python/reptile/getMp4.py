# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests

if __name__ == "__main__":
    tar = 'http://www.imomoe.ai'
    target = tar + '/player/7947-0-0.html'
    req = requests.get(url = target)
    req.encoding = req.apparent_encoding
    html = req.text
    # print(html)
    div_bf = BeautifulSoup(html,features = "lxml")
    div = div_bf.find_all('div', class_ = 'player')
    # print(div)
    script_bf = BeautifulSoup(str(div[0]),features = "lxml")
    a = script_bf.find_all('script')
    path = ''
    for eacha in a:
        if(eacha.get('src') is not None):
            path = eacha.get('src')
    path = tar + path
    # print(path)
    req = requests.get(url = path)
    req.encoding = req.apparent_encoding
    mp4Json = req.text
    # print(mp4Json)
    list = mp4Json.split('$')
    for each in list:
        if(each.find('http') == 0):
            print(each)









