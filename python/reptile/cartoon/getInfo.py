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
    sql = "INSERT INTO cartoon_info(area,type,issue,language,title,alias,label,introduction,remark,poster_url,link_url) VALUES (%s, %s,%s, %s,%s, %s,%s, %s, %s,%s, %s);"
    try:
        # 执行SQL语句
        cursor.execute(sql, [listTitle[1],listTitle[2],listTitle[3],'日语动漫',title,listTitle[0],listTitle[5],listRemark[0],listTitle[6],listRemark[1],url])
        # 提交事务
        conn.commit()
    except Exception as e:
        # 有异常，回滚事务
        conn.rollback()
    cursor.close()


def savePlayer(palyUrl,title,i,conn):
    i -=1
    tar = 'http://www.imomoe.ai'
    target = tar + palyUrl
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
    orderId =1
    type =1
    list = mp4Json.split('$')
    print(palyUrl)
    cursor = conn.cursor()
    for each in list:
        if(each.find('http') == 0):
            print(each)
            if(orderId > i):
                type += 1
                orderId =1
            sql = "INSERT INTO cartoon_play(link_url,title,order_id,type) VALUES (%s,%s,%s,%s);"
            try:
                # 执行SQL语句
                cursor.execute(sql, [each,title,orderId,type])
                orderId += 1
                # 提交事务
                conn.commit()
            except Exception as e:
                # 有异常，回滚事务
                conn.rollback()
    cursor.close()


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
    i =1
    palyUrl = ''
    cursor = conn.cursor()
    for eacha in a:
        print(eacha.string, eacha.get('href'))
        if (i == 1):
            palyUrl = eacha.get('href')
        sql = "INSERT INTO cartoon_file(link_url,title,order_id,order_info) VALUES (%s,%s,%s,%s);"
        try:
            # 执行SQL语句
            cursor.execute(sql, [eacha.get('href'),title,i,eacha.string])
            i+=1
            # 提交事务
            conn.commit()
        except Exception as e:
            # 有异常，回滚事务
            conn.rollback()
    cursor.close()
    savePlayer(palyUrl,title,i,conn)




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
    href = '?page=1&searchword=%C8%D5%D3%EF&searchtype=-1'
    while True:
        conn = pymysql.connect(host='127.0.0.1', user='root',password='wanghongbo',database='aohayou',charset='utf8')
        resut = print_page_info(href,conn)
        conn.close()
        if(resut == ''):
            break
        href = resut








