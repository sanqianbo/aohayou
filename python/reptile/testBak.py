# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests
if __name__ == "__main__":
    target = 'http://www.imomoe.ai/search.asp?searchword=%C8%D5%D3%EF'
    req = requests.get(url = target)
    req.encoding = req.apparent_encoding
    html = req.text
    div_bf = BeautifulSoup(html,features = "lxml")
    div = div_bf.find_all('div', class_ = 'pics')
    print(str(div[0]))
    h2_bf = BeautifulSoup(str(div[0]),features = "lxml")
    h2 = h2_bf.find_all('h2')
    for each in h2:
        a_bf = BeautifulSoup(str(each),features = "lxml")
        a = a_bf.find_all('a')
        for eacha in a:
            print(eacha.string, eacha.get('href'))


