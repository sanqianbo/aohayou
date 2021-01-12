# -*- coding:UTF-8 -*-
import bs4
from bs4 import BeautifulSoup, NavigableString
import requests
import pymysql


def getTitleInfo(html):
    div_bf = BeautifulSoup(html,features = "lxml")
    div = div_bf.find_all('div', class_ = 'alex')
    p_bf = BeautifulSoup(str(div[0]),features = "lxml")
    print(p_bf)
    for child in p_bf.div.children:
        if isinstance(child,NavigableString):
            continue
        print(child,child.string)




def getRemarkInfo(html):
    pass


def getCartoonInfo(eacha):
    print(eacha.string, eacha.get('href'))
    tar = 'http://www.imomoe.ai'
    target = tar+eacha.get('href')
    req = requests.get(url = target)
    req.encoding = req.apparent_encoding
    html = req.text
    # print(html)
    listTitle = []
    listRemark = []
    list = getTitleInfo(html)
    listRemark = getRemarkInfo(html)
    div_bf = BeautifulSoup(html,features = "lxml")
    div = div_bf.find_all('div', class_ = 'movurl')
    a_bf = BeautifulSoup(str(div[0]),features = "lxml")
    # print(a_bf)
    a = a_bf.find_all('a')
    for eacha in a:
        print(eacha.string, eacha.get('href'))




def getPageInfo(html):
    div_bf = BeautifulSoup(html,features = "lxml")
    div = div_bf.find_all('div', class_ = 'pics')
    # print(str(div[0]))
    h2_bf = BeautifulSoup(str(div[0]),features = "lxml")
    h2 = h2_bf.find_all('h2')
    for each in h2:
        a_bf = BeautifulSoup(str(each),features = "lxml")
        a = a_bf.find_all('a')
        for eacha in a:
            getCartoonInfo(eacha)


def print_page_info(path):
    tar = 'http://www.imomoe.ai/search.asp'
    target = tar+path
    req = requests.get(url = target)
    req.encoding = req.apparent_encoding
    html = req.text
    # print(html)
    getPageInfo(html)
    div_bf = BeautifulSoup(html,features = 'lxml')
    div = div_bf.find_all('div', class_ = 'pages')
    # print(div)
    a_bf = BeautifulSoup(str(div[0]),features='lxml')
    aArr = a_bf.find_all('a')
    # print(len(aArr))
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
    # conn = pymysql.connect(host='127.0.0.1', user='root',password='wanghongbo',database='aohayou',charset='utf8')
    # cursor = conn.cursor()
    # sql = "INSERT INTO cartoon_info(area, issue) VALUES (%s, %s);"
    # area = "area"
    # type = '2020'
    # try:
    #     # 执行SQL语句
    #     cursor.execute(sql, [area, type])
    #     # 提交事务
    #     conn.commit()
    # except Exception as e:
    #     # 有异常，回滚事务
    #     conn.rollback()
    # cursor.close()
    # conn.close()
    href = '?page=1&searchword=%C8%D5%D3%EF&searchtype=-1'
    while True:
        resut = print_page_info(href)
        if(resut == ''):
            break
        href = resut








