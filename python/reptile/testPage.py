# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests
if __name__ == "__main__":
    tar = 'http://www.imomoe.ai/search.asp'
    target = tar+'?searchword=%C8%D5%D3%EF'
    req = requests.get(url = target)
    req.encoding = req.apparent_encoding
    html = req.text
    # print(html)
    div_bf = BeautifulSoup(html,features = 'lxml')
    div = div_bf.find_all('div', class_ = 'pages')
    print(div)
    a_bf = BeautifulSoup(str(div[0]),features='lxml')
    aArr = a_bf.find_all('a')
    print(aArr)
    next = str(aArr[7])
    aNext_bf = BeautifulSoup(str(next),features='lxml')
    aNext = aNext_bf.find_all('a')
    for each in aNext:
        print(each.string,each['href'])


