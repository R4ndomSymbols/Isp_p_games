class Settings():
    #Все настройки приложения

    def __init__(self):

        # Настройки экрана.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (8,8,13)

        # Настройки количества жизней.
        self.ship_limit = 3

        # Настройки пуль.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 219, 21, 38
        self.bullets_allowed = 3

        # Настройки скорости флота.
        self.fleet_drop_speed = 10

        # Ускорение игры.
        self.speedup_scale = 1.1
        # Множитель счета.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # Инициализация динамических настроек

        self.ship_speed_factor = 2
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.9

        # Награда за пришельца.
        self.alien_points = 50

        # Направление движения флота.
        self.fleet_direction = 1

    def increase_speed(self):
       
        # Увеличение сложности игры

        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
