# -*- coding: utf-8 -*-
import pymysql
import calendar
import datetime
import re

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='fyf!!961004',charset='utf8')
cur = conn.cursor()
cur.execute('use scraping')
def before_sunday(date):
    """
    返回前面最近那个周日
    :param date:
    :param weekend:
    :return: date对象
    """
    weekday = calendar.weekday(date.year, date.month, date.day)
    if weekday == 6:
        remain_days = 0
    else:
        remain_days =weekday+1
    td = datetime.timedelta(days=remain_days)
    return date - td


def change(item):
    item = str(item)
    if len(item) < 2:
        item = '0' + item
    return item

for i in range(38913,42237):
    try:
        sql='select t_when from weibo_search_result where id = (%s)'
        cur.execute(sql,(i))
        s=str(cur.fetchone()[0])
        t_when =s[:10]
        year,month,day=re.findall(r'(\d{4})-(\d{2})-(\d{2})',t_when)[0]
        date=datetime.datetime(int(year),int(month),int(day))
        year, month, day=map(change,[before_sunday(date).year,before_sunday(date).month,before_sunday(date).day])
        post_month=year+'-'+month+'-'+day
        sql='update weibo_search_result set post_month=(%s) where id=(%s) '
        cur.execute(sql,(post_month,i))
        conn.commit()
    except Exception,e:
        print i

cur.close()
conn.close()