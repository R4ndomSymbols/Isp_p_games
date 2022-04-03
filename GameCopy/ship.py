import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Загрузка изображения и области отрисовки корабля.
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Определение первоначальной позиции.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # Точная позиция корабля.
        self.center = float(self.rect.centerx)
        
        # Флаги движения.
        self.moving_right = False
        self.moving_left = False
        
    def center_ship(self):
        # Центрирование корабля
        self.center = self.screen_rect.centerx
        
    def update(self):
        
        #Обновление позиции корабля в зависисости от флагов

        # Обновление позиции корабля, но не области отрисовки
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
            
        # Обновление состояния области отрисовки.
        self.rect.centerx = self.center

    def blitme(self):
        #Отрисовка корабля
        self.screen.blit(self.image, self.rect)
