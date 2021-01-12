# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests
import pymysql

if __name__ == "__main__":
    conn = pymysql.connect(host='127.0.0.1', user='root',password='wanghongbo',database='aohayou',charset='utf8')
    cursor = conn.cursor()
    sql = "INSERT INTO cartoon_info(area, issue) VALUES (%s, %s);"
    area = "area"
    type = '2020'
    try:
        # 执行SQL语句
        cursor.execute(sql, [area, type])
        # 提交事务
        conn.commit()
    except Exception as e:
        # 有异常，回滚事务
        conn.rollback()
    cursor.close()
    conn.close()








