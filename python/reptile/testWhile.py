# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests


def print_page_info(path):
    tar = 'http://www.imomoe.ai/search.asp'
    target = tar+path
    req = requests.get(url = target)
    req.encoding = req.apparent_encoding
    html = req.text
    # print(html)
    div_bf = BeautifulSoup(html,features = 'lxml')
    div = div_bf.find_all('div', class_ = 'pages')
    print(div)
    a_bf = BeautifulSoup(str(div[0]),features='lxml')
    aArr = a_bf.find_all('a')
    print(len(aArr))
    # print(aArr)
    next = str(aArr[7])
    if(len(aArr) == 11):
        next = str(aArr[9])
    aNext_bf = BeautifulSoup(str(next),features='lxml')
    aNext = aNext_bf.find_all('a')
    resut = ''
    for each in aNext:
        resut = each['href']
        if(each.string !='下一页'):
            resut = ''
        else:
            print(each.string,each['href'])
    return resut


if __name__ == "__main__":
    # href = '?searchword=%C8%D5%D3%EF'
    href = '?page=481&searchword=%C8%D5%D3%EF&searchtype=-1'
    while True:
        resut = print_page_info(href)
        if(resut == ''):
            break
        href = resut
