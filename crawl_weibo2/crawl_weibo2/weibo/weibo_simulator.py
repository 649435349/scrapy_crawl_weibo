# -*- coding=gbk -*-

import urllib
import urllib2 
import cookielib
import base64
import json
import rsa
import binascii
import re

class weibo_simulator:
    def login(self, username, password):
        (servertime, nonce, rsakv, pubkey) = self.login_prepare(username)
        login_content = self.login_post(username, password, servertime, nonce, rsakv, pubkey)
        print('login_post finished')
        self.login_redirect(login_content)
        print('login finished')
        
    def logout(self):
        content_stream = self.opener.open(self.logout_sso_url)
        content_stream.read()
        print('logout_sso finished')
        content_stream = self.opener.open(self.logout_passort_url)
        content_stream.read()
        print('logout finished')
        
#     def login_success(self):
#         page_content = simulator.openurl(self.mainpage_url)
#         pattern = re.compile('\$CONFIG\[\'islogin\'\].*?\'([0,1])\'')
#         search_groups = pattern.search(page_content)
#         islogin = search_groups.group(1)
#         if(islogin == '1'):
#             return True
#         else:
#             return False
        
    def openurl(self, url):
        req = urllib2.Request(url)  
        content_stream = self.opener.open(req)  
        origin_content = content_stream.read()
        content = origin_content.decode('utf-8', 'replace')
        return content

    def word2url(self, word):
        return ''.join([self.search_prefix,
                        urllib2.quote(urllib2.quote(word.encode('utf-8', 'replace'))),
                        "&typeall=1&suball=1"])
                        # self.search_appendix])
        
    def get_cookiedict(self):
        result = {}
        for cookie in self.cookie:
            result[cookie.name] = cookie.value
        return result
        
    def __init__(self):
        self.cookie = cookielib.LWPCookieJar()  
        self.cookie_support = urllib2.HTTPCookieProcessor(self.cookie)  
        self.opener = urllib2.build_opener(self.cookie_support, urllib2.HTTPHandler)  
        
        self.prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php'
        self.login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
        self.mainpage_url = 'http://weibo.com/'
        self.search_prefix = 'http://s.weibo.com/weibo/'
        self.search_appendix = '&scope=ori&xsort=time'

        self.logout_sso_url = ''.join(['http://login.sina.com.cn/sso/logout.php?entry=miniblog&',
            'r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F'])
        
        self.logout_passort_url = ''.join(['http://passport.weibo.com/wbsso/logout?',
            'callback=sinaSSOController.doCrossDomainCallBack&',
            'scriptId=ssoscript0&client=ssologin.js(v1.4.2)&_=1408869665487'])
        
        self.prelogin_postdata = {
            'entry': 'account', 
            'su': '',
            'rsakt': 'mod',
            'checkpin': 1,
            'client': 'ssologin.js(v1.4.18)'
        }
        
        self.login_postdata = {
            'entry': 'weibo', 
            'gateway': '1',  
            'from': '',  
            'savestate': '7',  
            'userticket': '1',
            'ssosimplelogin': '1',  
            'vsnf': '1',  
            'vsnval': '',  
            'su': '',  
            'service': 'miniblog',  
            'servertime': '',  
            'nonce': '',  
            'pwencode': 'rsa2',  
            'sp': '',  
            'encoding': 'UTF-8',  
            'prelt': '115',  
            'rsakv': '',  
            'url': ''.join(['http://weibo.com/ajaxlogin.php?',
                'framelogin=1&',
                'callback=parent.sinaSSOController.feedBackUrlCallBack']), 
            'returntype': 'META'  
        }
        
        self.headers = {'User-Agent': ''.join(['Mozilla/5.0 (X11; Linux i686; rv:8.0) ',
            'Gecko/20100101 ',
            'Firefox/8.0 ',
            'Chrome/20.0.1132.57 ',
            'Safari/536.11'])
        }
        
    def login_prepare(self, username):
        self.prelogin_postdata['su'] = base64.encodestring(urllib2.quote(username))
        url = '%s?%s' % (self.prelogin_url, urllib.urlencode(self.prelogin_postdata))
        req = urllib2.Request(url)
        content_stream = self.opener.open(req)
        content = content_stream.read()
        prepare_info = json.loads(content)
        return (prepare_info['servertime'],
            prepare_info['nonce'],
            prepare_info['rsakv'],
            prepare_info['pubkey'])
    
    def login_post(self, username, password, servertime, nonce, rsakv, pubkey):
        self.login_postdata['servertime'] = servertime
        self.login_postdata['nonce'] = nonce
        self.login_postdata['rsakv'] = rsakv
        self.login_postdata['su'] = base64.encodestring(urllib2.quote(username))
        
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537)
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
        passwd = rsa.encrypt(message, key)
        passwd = binascii.b2a_hex(passwd)
        self.login_postdata['sp'] = passwd 
        
        req = urllib2.Request(
            url=self.login_url,
            data=urllib.urlencode(self.login_postdata),
            headers=self.headers)
        content_stream = self.opener.open(req)
        login_content = content_stream.read()
        return login_content
        
    def login_redirect(self, login_content):
        pattern = re.compile('location\.replace\([\'\"](.*?)[\'\"]\)')
        search_groups = pattern.search(login_content)
        redirect_url = search_groups.group(1)
        content_stream = self.opener.open(redirect_url)
        redirect_content = content_stream.read()
        return redirect_content
    
    
if __name__ == '__main__':
    simulator = weibo_simulator()
    # simulator.login('wuzhichuan001@163.com', 'wu198931198931')
    simulator.login('jimmyzhang33@126.com', 'tt123456789')
    print simulator.get_cookiedict()
#     print simulator.login_success()
    simulator.logout()
#     print simulator.login_success()
