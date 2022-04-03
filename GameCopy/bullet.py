import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    # Класс, отвечающий за контроль над объктами пуль

    def __init__(self, ai_settings, screen, ship):
        #Пуля создается на носу корабля
        super(Bullet, self).__init__()
        self.screen = screen

        # Создание пули и ее размещение в корректной позиции.
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
            ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        # Хранит точную позицию пули.
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        # Двигает пули по экрану
        # Обновляет точную позицию пули.
        self.y -= self.speed_factor
        # Обновляет позицию спрайта.
        self.rect.y = self.y

    def draw_bullet(self):
        # Рисует пулю на экране
        pygame.draw.rect(self.screen, self.color, self.rect)
