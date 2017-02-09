import os
import time

class passport_manager:
    def __init__(self):
        self.conf_file =  os.path.join(os.path.dirname(os.path.realpath(__file__)),'conf/passport.conf')
        self.key_username = 'username'
        self.key_password = 'password'
        self.key_killed = 'killed'
        
        self.passport_pool = []
        self.total_number = 0
        self.living_number = 0
        self.index = 0
    
    def read_conf(self):
        if os.path.isfile(self.conf_file):
            f = open(self.conf_file)
            self.passport_pool = eval(f.read())
            f.close()
        
        self.total_number = 0
        self.living_number = 0
        
        for passport in self.passport_pool:
            self.total_number += 1
            if not passport[self.key_killed]:
                self.living_number += 1
        
        self.index = len(self.passport_pool) - 1
        
    def get_next_passport(self, kill=False):
        if len(self.passport_pool) == 0:
            return None
        if self.living_number <= 0:
            print 'no living passport, sleep 10 minutes'
            time.sleep(600)
            
        if kill:
            if not self.passport_pool[self.index][self.key_killed]:
                self.living_number -= 1
            self.passport_pool[self.index][self.key_killed] = True
            f = open(self.conf_file, 'w')
            f.write(repr(self.passport_pool))
            f.close()
        
        self.index = (self.index + 1) % len(self.passport_pool)
        passport = self.passport_pool[self.index]
        print 'change passport %d' % self.index
        print passport
        return (passport[self.key_username], passport[self.key_password])
    
    def write_conf(self, passport_list):
        f = open(self.conf_file, 'w')
        f.write(repr(passport_list))
        f.close()
    
    def __str__(self):
        return str(self.passport_pool)
    
if __name__ == '__main__':
    manager = passport_manager()
#     pool = [{'username':'weiboxiaohao101@163.com', 'password':'a11111111', 'killed':False},
#             {'username':'weiboxiaohao102@163.com', 'password':'a11111111', 'killed':False},
#             {'username':'weiboxiaohao103@163.com', 'password':'a11111111', 'killed':False},
#             {'username':'weiboxiaohao104@163.com', 'password':'a11111111', 'killed':False},
#             {'username':'weiboxiaohao105@163.com', 'password':'a11111111', 'killed':False},
#             ]
    pool = [{'username':'wuzhichuan001@163.com', 'password':'wu198931198931', 'killed':False},
            {'username':'wuzhichuan002@163.com', 'password':'a11111111', 'killed':False},
            {'username':'mailing_server@163.com', 'password':'wu198931198931', 'killed':False},
            ]
#     pool = [{'username':'wuwuzhichuan@163.com', 'password':'wu198931198931', 'killed':False}]
    manager.write_conf(pool)
    manager.read_conf()
    print manager
    
    
    
    
    
    
    
    
    
    