from datetime import datetime, timedelta

import opinion_collect.config_game_data as config_game_data


class gameword_manager:
    def read_conf(self):
        reload(config_game_data)
        self.game_list = []
        self.game_time = {}
        self.index = 0
        current_time = datetime.now() + timedelta(days = -1)
        for game_id, game_info in config_game_data.game_data.items():
            for game_name in game_info['aliases']:
                game_name = game_name.decode('gbk')
                self.game_list.append((game_id,game_name))
                self.game_time[game_name] = current_time
        
    def get_next_word(self):
        if self.index >= len(self.game_list):
            self.read_conf()
        game_id, game_name = self.game_list[self.index]
        self.index = self.index + 1
        current_time = datetime.now() + timedelta(days = -1)
        self.game_time[game_name] = current_time
        return (game_id, game_name)
    
    def has_more_thesis(self, game_name, game_time):
        if(game_name in self.game_time and self.game_time[game_name] < game_time):
            return True
        return False

if __name__ == '__main__':
    manager = gameword_manager()
    manager.read_conf()
    for i in range(10):
        game_id, game_name = manager.get_next_word()
        print game_id, game_name
