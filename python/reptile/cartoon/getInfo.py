# -*- coding:UTF-8 -*-
import sys

import bs4
from bs4 import BeautifulSoup, NavigableString
import requests
import pymysql


def getTitleInfo(html):
    div_bf = BeautifulSoup(html,features = "lxml")
    div = div_bf.find_all('div', class_ = 'alex')
    p_bf = BeautifulSoup(str(div[0]),features = "lxml")
    resut =[]
    for child in p_bf.div.children:
        if isinstance(child,NavigableString):
            continue
        if (child.string != None):
            resut.append(child.string)
        ss =''
        a = child.find_all('a')
        size = len(a)
        if (size <= 0):
            continue
        for aa in a:
            a_bf = BeautifulSoup(str(aa),features = "lxml")
            for child in a_bf.a.children:
                # print(child.string)
                ss += child.string
                ss +='#'
        resut.append(ss[0:-1])
    # print(resut)
    return resut



def getRemarkInfo(html,title):
    div_bf = BeautifulSoup(html,features = "lxml")
    div = div_bf.find_all('div', class_ = 'info')
    p_bf = BeautifulSoup(str(div[0]),features = "lxml")
    # print(p_bf)
    resut =[]
    for child in p_bf.div.children:
        if (child.string != None):
            resut.append(child.string)
    img = div_bf.find_all('img', attrs={'alt':title})
    img_bf = BeautifulSoup(str(img[0]),features = "lxml")
    tag = img_bf.img
    # print(tag['src'])
    resut.append(tag['src'])
    return resut


def saveInfo(listTitle, listRemark, title,url,conn):
    cursor = conn.cursor()
    # sql = "INSERT INTO cartoon_info(area,type,issue,language,title,alias,label,introduction,remark,poster_url,link_url) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s);"
    sql = "INSERT INTO cartoon_info(area,type,issue) VALUES (%s, %s,%s);"
    try:
        # 执行SQL语句
        # cursor.execute(sql, [listTitle[1],listTitle[2],listTitle[3],'日漫',title,listTitle[0],listTitle[5],listRemark[0],listTitle[6],listRemark[1],url])
        cursor.execute(sql, ['1','2','2021'])
        # 提交事务
        conn.commit()
    except Exception as e:
        # 有异常，回滚事务
        conn.rollback()
    cursor.close()
    # conn.close()


def getCartoonInfo(eacha,conn):
    title = eacha.string
    url = eacha.get('href')
    print(title, url)
    tar = 'http://www.imomoe.ai'
    target = tar+eacha.get('href')
    req = requests.get(url = target)
    req.encoding = req.apparent_encoding
    html = req.text
    # print(html)
    listTitle = []
    listRemark = []
    listTitle = getTitleInfo(html)
    listRemark = getRemarkInfo(html,title)
    saveInfo(listTitle,listRemark,title,url,conn)
    div_bf = BeautifulSoup(html,features = "lxml")
    div = div_bf.find_all('div', class_ = 'movurl')
    a_bf = BeautifulSoup(str(div[0]),features = "lxml")
    # print(a_bf)
    a = a_bf.find_all('a')
    for eacha in a:
        print(eacha.string, eacha.get('href'))




def getPageInfo(html,conn):
    div_bf = BeautifulSoup(html,features = "lxml")
    div = div_bf.find_all('div', class_ = 'pics')
    # print(str(div[0]))
    h2_bf = BeautifulSoup(str(div[0]),features = "lxml")
    h2 = h2_bf.find_all('h2')
    for each in h2:
        a_bf = BeautifulSoup(str(each),features = "lxml")
        a = a_bf.find_all('a')
        for eacha in a:
            getCartoonInfo(eacha,conn)


def print_page_info(path,conn):
    tar = 'http://www.imomoe.ai/search.asp'
    target = tar+path
    req = requests.get(url = target)
    req.encoding = req.apparent_encoding
    html = req.text
    # print(html)
    getPageInfo(html,conn)
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
    conn = pymysql.connect(host='127.0.0.1', user='root',password='wanghongbo',database='aohayou',charset='utf8')
    href = '?page=1&searchword=%C8%D5%D3%EF&searchtype=-1'
    while True:
        resut = print_page_info(href,conn)
        if(resut == ''):
            break
        href = resut








