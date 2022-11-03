import json

class GameConfig:

    #consts
    config_file_name = 'config.json' 


    def __init__(self):
        f = open(self.config_file_name)
        data = json.load(f)
        self.bot_token = data['bot-token']
        f.close()
        print("Config has been loaded")