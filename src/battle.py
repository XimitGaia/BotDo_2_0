from screen import Screen


class Battle:


    def __init__(self, screen):
        self.screen = screen
        battle_info = self.screen.get_battle_map_info()





if __name__ == '__main__':
    
    screen = Screen()
    battle = Battle(screen=screen)