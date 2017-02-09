# -*- coding: utf-8 -*-
from crawl_weibo2 import db_utils
import warnings
import pymysql
warnings.filterwarnings('ignore', category=pymysql.Warning)


class CrawlWeiboPipeline(object):
    def __init__(self):
        self.conn = db_utils.get_conn()

    def process_item(self, item, spider):
        cursor = self.conn.cursor()
        sql = item.gen_sql()
        cursor.execute("set names utf8;")
        cursor.execute(sql)
        self.conn.commit()
        cursor.fetchone()
        return item
