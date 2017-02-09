# -*- coding=gbk -*-
from gameword_manager import gameword_manager
from passport_manager import passport_manager
from weibo_simulator import weibo_simulator
from weibo_searchpage_parser import weibo_searchpage_parser
from datetime import datetime
import time
import global_constants
import traceback

if __name__ == '__main__':
    passport = passport_manager()
    passport.read_conf()
    (username, password) = passport.get_next_passport()
    
    simulator = weibo_simulator()
    simulator.login(username, password)
    time.sleep(2)
    
    parser = weibo_searchpage_parser()
    
    gameword = gameword_manager()
    gameword.read_conf()
    
    page_count = 0
    game_count = 0
    while(True):
        game_count += 1
        game = gameword.get_next_word()
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        page_url = simulator.word2url(game)
        try:
            for page_index in range(1, 20):
                page_count += 1
                file_name = '%s_%s_%d' % (game, timestamp, page_index)
                page_html = simulator.openurl(page_url)
#                 page_html = open('log/天谕_2014-08-27_17-43-31_3').read().decode(global_constants.system_encoding, 'replace')
                log_file = open('log/%s' % file_name.encode(global_constants.system_encoding, 'replace'), 'w')
                log_file.write(page_html.encode(global_constants.system_encoding, 'replace'))
                log_file.close()
                
                parser.parsepage(page_html)
                page_content_list = parser.get_contentlist()
                out_file = open('out/%s' % file_name.encode(global_constants.system_encoding, 'replace'), 'w')
                for content in page_content_list:
                    out_file.write(content.__str__().encode(global_constants.system_encoding, 'replace') + '\n')
                out_file.close()
                
                if not parser.get_haslogin():
                    (username, password) = passport.get_next_passport()
                    simulator.login(username, password)
                    time.sleep(2)
                
                if parser.get_robotpage():
                    print '-' * 50
                    print 'is robot'
                    simulator.logout()
                    time.sleep(5)
                    (username, password) = passport.get_next_passport(kill=True)
                    simulator.login(username, password)
                    time.sleep(2)
                    print '-' * 50
                    continue
                
                (begin_time, end_time) = parser.get_timescope()
                print ('%s\t[%s,%s][game=%d,page=%d]' % (
                    file_name, begin_time.strftime('%m-%d %H:%M:%S'), 
                    end_time.strftime('%m-%d %H:%M:%S'),
                    game_count, page_count)).encode(global_constants.system_encoding, 'replace')
                
                page_url = parser.get_nextlink()
                time.sleep(21)
                if (not gameword.has_more_thesis(game, begin_time)) or page_url is None:
                    break
        except Exception as e:
            print '-' * 50
            print ('game name = %s' % game).encode(global_constants.system_encoding, 'replace')
            print ('url = %s' % page_url).encode(global_constants.system_encoding, 'replace')
            print traceback.format_exc()
            print '-' * 50
