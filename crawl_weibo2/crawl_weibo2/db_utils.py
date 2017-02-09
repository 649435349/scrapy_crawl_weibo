# -*- coding:utf8 -*-
import pymysql
import os
import sys
# sys.path.append("os.")

op_sys = os.uname()[0]

if "linux" not in op_sys.lower():
    DB_URL = "127.0.0.1"
    DB_USER = "root"
    DB_PSW = "fyf!!961004"
    DB_NAME = "scraping"
    DB_CHARSET = "utf8"
else:
    DB_URL = "10.63.76.38"
    DB_USER = "us_player_base"
    DB_PSW = "7DY87EEmVXz8qYf2"
    DB_NAME = "us_player_base_test"
    DB_CHARSET = "utf8"

def get_conn():
    conn = pymysql.connect(host=DB_URL, user=DB_USER, passwd=DB_PSW, db=DB_NAME, charset=DB_CHARSET)
    return conn

def get_all_keywords(conn):
    cur = conn.cursor()
    cur.execute("set names utf8")
    cur.execute(u"select id, keyword from itunes_keywords")
    res = cur.fetchall()
    cur.fetchone()
    return res
