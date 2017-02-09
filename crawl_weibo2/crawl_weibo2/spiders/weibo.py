# -*- coding: utf-8 -*-
import scrapy
import sys
import time
import pymysql
import re
import datetime
reload(sys)
sys.setdefaultencoding('utf8')
from scrapy.spider import BaseSpider
from scrapy.http import Request
from crawl_weibo2.weibo.weibo_simulator import weibo_simulator
from crawl_weibo2.weibo.passport_manager import passport_manager

class weiboSpider(BaseSpider):
    name="weibo"
    download_delay=22
    def __init__(self):
        self.passport = passport_manager()
        self.passport.read_conf()
        self.simulator = weibo_simulator()

    def start_requests(self):
        (username, password) = self.passport.get_next_passport()
        self.simulator.login(username, password)
        self.cookie = self.simulator.get_cookiedict()
        # cookie_str = 'SINAGLOBAL=3208405503537.506.1433685315966; _ga=GA1.2.128294337.1467384569; __gads=ID=c545d8802063a491:T=1467384567:S=ALNI_MbPioLy4igXDM7KZ0qy1_TNgWxEHA; _s_tentry=login.sina.com.cn; Apache=700969313803.4856.1479049978341; ULV=1479049978846:48:3:1:700969313803.4856.1479049978341:1478849358797; SWB=usrmdinst_11; UOR=zipperary.com,widget.weibo.com,login.sina.com.cn; WBtopGlobal_register_version=ed627fcaaaabd5aa; SCF=ArZxSuNd0ENDhrfbqBEHyOQxNajvsmeEqDwNqvbS03JcXt9TCL67eKpY_blaeN3wSAUx16_5ZvY4cH8sMNGgteU.; SUB=_2A251LTsfDeTxGedJ41sQ9CbNyD-IHXVWWyvXrDV8PUNbmtBeLUTEkW-btmgHaq9zyv74fQ8UiX6zXjSC7g..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWjKdxa5gWJRCNaz8aK_is-5JpX5K2hUgL.Fo2N1h.pShnpe0e2dJLoI7p3Igf_wPDQqg4re0et; SUHB=0y0IDf10o7sdrB; ALF=1479706064; SSOLoginState=1479101263; un=zhangtengji@gmail.com; WBStorage=2c466cc84b6dda21|undefined'
        # self.cookie = parse_cookie(cookie_str)
        time.sleep(2)
        yield Request('http://weibo.cn/heromoba?page=1', cookies=self.cookie, callback=self.getPageNum)


    def getPageNum(self,response):
        div=response.xpath('//div[@id="pagelist"]')
        n=int(re.findall(r'1/(\d+)页'.decode('utf8'),div.extract()[0])[0])
        for i in range(n+1):
            yield Request('http://weibo.cn/heromoba?page={}'.format(i), cookies=self.cookie, callback=self.parse)
            time.sleep(3)

    def parse(self,response):
        conn = pymysql.connect(host='127.0.0.1', user='root', passwd='fyf!!961004', db='scraping',charset='utf8')
        cur = conn.cursor()
        divs=response.xpath('//div[@class="c" and @id]')
        game_name=post_user=u'王者荣耀'
        for div in divs:
            try:
                #置顶的在下面也出现了，先排除掉
                if re.findall(r'置顶'.decode('utf8'),div.xpath('div[1]').extract()[0].decode('utf8')):
                    continue
                divNum=len(div.xpath('div'))
                #尝试过直接抓取赞之前的内容，失败，因为div.extract()[0]无法被识别，我也不知道为什么。。。
                if divNum==3:
                    #转发的带图片的微博
                    content = div.xpath('div[1]').extract()[0].decode('utf8')+div.xpath('div[2]').extract()[0].decode('utf8')+re.findall(r'(.+)(?=<a\shref=".+">赞)'.decode('utf8'), div.xpath('div[3]').extract()[0].decode('utf8'))[0]+'</div>'
                    tmp = div.xpath('div[3]')
                elif divNum==2:
                    #带图片的微博或者转发的不带文字的微博
                    #如果是文字的话，选取赞标签之前的内容
                    # 如果是图片的话，就选取第一个<a>的内容
                    tmp = div.xpath('div[2]')
                    if re.findall(r'(.+)(?=&nbsp;&nbsp)'.decode('utf8'),tmp.extract()[0]):
                        content = div.xpath('div[1]').extract()[0].decode('utf8')+re.findall(r'(.+)(?=<a\shref=".+">赞)'.decode('utf8'),tmp.extract()[0].decode('utf8'))[0]+'</div>'
                    else:
                        content=div.xpath('div[1]').extract()[0].decode('utf8')+tmp.xpath('a').extract()[0].decode('utf8')+'</div>'
                else:
                    #只有一条文字的微博
                    tmp = div.xpath('div[1]')
                    content = tmp.xpath('span[1]').extract()[0].decode('utf8')
                thumbs_up_cnt = int(re.findall(r'赞\[(\d+)\]'.decode('utf8'), tmp.extract()[0])[0])
                repost_cnt = int(re.findall(r'转发\[(\d+)\]'.decode('utf8'), tmp.extract()[0])[0])
                reply_cnt = int(re.findall(r'评论\[(\d+)\]'.decode('utf8'), tmp.extract()[0])[0])
                _time = tmp.xpath('span[last()]').extract()[0]
                if re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'.decode('utf8'), _time.decode('utf8')):
                    #去年或者之前发的 2016-10-01 01:01:01
                    t_when = re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'.decode('utf8'), _time.decode('utf8'))[0]
                    post_month = t_when[:7]
                elif re.findall(r'\d{2}月\d{2}日 \d{2}:\d{2}'.decode('utf8'), _time.decode('utf8')):
                    #01月10日 11:32 不带秒，一般是今年发的
                    month, day, hour, minute = re.findall(r'\d{2}'.decode('utf8'), _time.decode('utf8'))
                    year=str(datetime.datetime.now().year)
                    t_when = year + '-' + month + '-' + day + ' ' + hour + ':' + minute
                    post_month = year + '-' + month
                elif re.findall(r'分钟'.decode('utf8'), _time.decode('utf8')):
                    #**分钟前
                    minutes=int(re.findall(r'\d{2}'.decode('utf8'), _time.decode('utf8'))[0])
                    delta=datetime.timedelta(minutes=minutes)
                    posttime=datetime.datetime.now()-delta
                    year,month,day,hour,minute=map(self.change,[posttime.year,posttime.month,posttime.day,posttime.hour,posttime.minute])
                    t_when = year + '-' + month + '-' + day + ' ' + hour + ':' + minute
                    post_month = year + '-' + month
                else:
                    #今天 19:59
                    hour,minute=re.findall(r'(\d{2})'.decode('utf8'), _time.decode('utf8'))
                    posttime = datetime.datetime.now()
                    year, month, day= map(self.change,[posttime.year, posttime.month, posttime.day])
                    t_when = year + '-' + month + '-' + day + ' ' + hour + ':' + minute
                    post_month = year + '-' + month
                cur.execute('set names utf8mb4')
                sql = "insert into  weibo_search_result(game_name, post_user, post_month, repost_cnt, thumbs_up_cnt, reply_cnt, t_when, content) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                cur.execute(sql,(game_name, post_user, post_month, repost_cnt, thumbs_up_cnt, reply_cnt, t_when, content))
                conn.commit()
            except Exception,e:
                print e
                continue
        cur.close()
        conn.close()


    def change(self,item):
        item=str(item)
        if len(item)<2:
            item='0'+item
        return item
