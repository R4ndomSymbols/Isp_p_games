import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    #Класс, определяющий сущность пришельца

    def __init__(self, ai_settings, screen):
        #Создание и препроцесс пришельца
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Накладывает текстуру на модель пришельца
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Размещает пришельца в верхем левом углу экрана.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Содержит точную позицию пришельца
        self.x = float(self.rect.x)
        
    def check_edges(self):
        # Возвращает истину, если пришелец выходит за границу экрана
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        
    def update(self):
        #Перемещает пришельцев в право или влево
        self.x += (self.ai_settings.alien_speed_factor *
                        self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        #Рисует пришельца
        self.screen.blit(self.image, self.rect)
