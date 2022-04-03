import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf

def run_game():

    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    # Cоздает кнопку Play.
    play_button = Button(ai_settings, screen, "Play")
    
    # Cоздает объекты статистики и визуальный счет
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    
    # Устанавливает цвет фона.
    bg_color = (230, 230, 230)
    
    # Создаются игровые сущности.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    
    # Создается флот инопланетян.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Основной цикл игры.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
            aliens, bullets)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
                bullets)
        
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,
            bullets, play_button)

run_game()
