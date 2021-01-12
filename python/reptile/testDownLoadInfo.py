# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests
if __name__ == "__main__":
    target = 'http://www.imomoe.ai/view/7947.html'
    req = requests.get(url = target)
    req.encoding = req.apparent_encoding
    html = req.text
    print(html)
    div_bf = BeautifulSoup(html,features = "lxml")
    div = div_bf.find_all('div', class_ = 'movurl')
    a_bf = BeautifulSoup(str(div[1]),features = "lxml")
    print(a_bf)
    a = a_bf.find_all('a')
    for eacha in a:
        print(eacha.string, eacha.get('href'))



