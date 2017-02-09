# -*- coding=gbk -*-
import re
from bs4 import BeautifulSoup
from data.thesis_data import thesis_data
from datetime import datetime

class weibo_searchpage_parser:
    def parsepage(self, text_page):
        bs_list = self.extract_html_part(text_page)
        
        self.is_robot = self.extract_robotpage(bs_list)
        self.has_login = self.extract_has_login(text_page)
        
        content_list = self.extract_contentlist(bs_list)
        self.content_list = content_list
        
        self.time_scope = self.extract_timescope(content_list)
        
        self.next_link = self.extract_nextlink(bs_list)
    
    def get_contentlist(self):
        return self.content_list
    
    def get_nextlink(self):
        return self.next_link
    
    def get_robotpage(self):
        return self.is_robot
    
    def get_haslogin(self):
        return self.has_login
    
    def get_timescope(self):
        return self.time_scope
    
    def __init__(self):
        self.root_url = 'http://s.weibo.com'
        self.content_list = []
        self.next_link = None
        self.time_scope = (0, 0)
        self.is_robot = False
        self.has_login = False
        
    def extract_html_part(self, text_page):
        bs_list = []
        html_pattern = re.compile(r'"html":"(.*?[^\\])"')
        for s in html_pattern.findall(text_page):
            content = eval('u"' + s + '"').replace('\\','')
            bs_list.append(BeautifulSoup(content))
        return bs_list

    def extract_contentlist(self, bs_list):
        content_list = []
        for soup in bs_list:
            for block in soup.find_all('div', {'class': 'WB_feed_detail clearfix'}):
                thesis = thesis_data()
                weibo_content = block.find('p', {'class': 'comment_txt'})
                weibo_date = block.find('a', {'class': 'W_textb'})
                weibo_face = block.find('div', {'class': 'feed_content wbcon'}).find('a')
                thesis.content = ''.join(weibo_content.stripped_strings)
                thesis.pubtime = datetime.fromtimestamp(((long)(weibo_date['date'])) / 1000)
                thesis.url = weibo_date['href']
                thesis.username = weibo_face['nick-name']
                thesis.user_url = weibo_face['href']
                content_list.append(thesis)
        return content_list

    def extract_timescope(self, content_list):
        min_date = datetime.now()
        max_date = datetime.fromtimestamp(0)
        for thesis in self.content_list:
            if thesis.pubtime < min_date:
                min_date = thesis.pubtime
            if thesis.pubtime > max_date:
                max_date = thesis.pubtime
        return (min_date, max_date)

    def extract_nextlink(self, bs_list):
        for soup in bs_list:
            link = soup.find('a', {'class': 'page next S_txt1 S_line1'})
            if link is None:
                continue
            return self.root_url + link['href']

    def extract_has_login(self, text_page):
        pattern = re.compile(r"\$CONFIG\['islogin'\]\s*?.*?\s*?'([0,1])'")
        search_groups = pattern.search(text_page)
        if search_groups is None:
            return False
        islogin = search_groups.group(1)
        if (islogin == '1'):
            return True
        else:
            return False

    def extract_robotpage(self, bs_list):
        for soup in bs_list:
            item = soup.find('p', {'class': 'code_tit'})
            if item is not None and item.string.find(u'你的行为有些异常，请输入验证码') >= 0:
                return True
        return False
    
if __name__ == '__main__':
    file_input = open('log/weibo_page.html')
    text = file_input.read()
    my_parser = weibo_searchpage_parser()
    my_parser.parsepage(text)
    print my_parser.get_robotpage()
    print my_parser.get_nextlink()
    print my_parser.get_timescope()
    print my_parser.get_haslogin()
    for content in my_parser.get_contentlist():
        print content
