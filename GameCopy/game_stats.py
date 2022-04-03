class GameStats():
    # Отслеживает статистиу приложения
    
    def __init__(self, ai_settings):
        
        self.ai_settings = ai_settings
        self.reset_stats()
        
        # Начало игры в инактивном состоянии.
        self.game_active = False
        
        # Наивысший счет не должен обнуляться.
        self.high_score = 0
        
    def reset_stats(self):
        # Обнуление статистики
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
