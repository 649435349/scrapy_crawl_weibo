class thesis_data:
    def __init__(self):
        self.user_url = ''
        self.username = ''
        self.pubtime = None
        self.url = ''
        self.content = ''
    
    def __str__(self):
        return '[%s,%s,%s,%s][%s]' % (self.user_url, self.username, self.pubtime, self.url, self.content)
    
if __name__ == '__main__':
    t = thesis_data()
    print t