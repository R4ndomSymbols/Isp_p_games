import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    
    # Обработка событий нажатия
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
        
def check_keyup_events(event, ship):
    # Обработка событий отжатия
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
        bullets):

    #Поток общей обработки
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                ship, aliens, bullets, mouse_x, mouse_y)
            
def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
        aliens, bullets, mouse_x, mouse_y):
    #Начинает новую игру, когда игрок нажимает на кнопку
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Обнуление настроек.
        ai_settings.initialize_dynamic_settings()
        
        # Сокрытие курсора.
        pygame.mouse.set_visible(False)
        
        # Обнуление статистики.
        stats.reset_stats()
        stats.game_active = True
        
        # Обнуление счетчиков.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        # Удаление всех продуцируемых сущностей .
        aliens.empty()
        bullets.empty()
        
        # Создание нового флота перед кораблем.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def fire_bullet(ai_settings, screen, ship, bullets):
    # Выстрел, если лимит пуль еще не достигнут
    # Создание пули, добавление ее в группу.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
        play_button):
    # Обновление экрана
    # Обновление фона игры.
    screen.fill(ai_settings.bg_color)
    
    # Обновление изображения пуль, корабля и флота.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    
    # Отрисовка информации о счете.
    sb.show_score()
    
    # Отрисовка кнопки плей, если игра находится в состоянии паузы.
    if not stats.game_active:
        play_button.draw_button()

    # Отрисовка подготовленного кадра.
    pygame.display.flip()
    
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # Обновление позиций пуль, удаление вышедших за пределы экрана
    # Обновление позиций пуль.
    bullets.update()

    # Удаление невидимых пуль.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
        aliens, bullets)
        
def check_high_score(stats, sb):
    # Проверка нового рекорда
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
            
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
        aliens, bullets):
    # Проверка коллизий пуль и пришельцев
    # Удаление всех элементов, участвующих в коллизиях.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if len(collisions) > 0:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    
    if len(aliens) == 0:
        # Если весь флот уничтожен, то начать новый уровень.
        bullets.empty()
        ai_settings.increase_speed()
        
        # Обновление счетчика уровня.
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings, screen, ship, aliens)
    
def check_fleet_edges(ai_settings, aliens):
    # Проверяет, достигли ли пришельцы границы экрана
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
        
def change_fleet_direction(ai_settings, aliens):
    # Изменение направления движения флота
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    
def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    #Проверяет коллизию корабля и пришельца
    if stats.ships_left > 0:
        stats.ships_left -= 1
        # Обновление количества жизней.
        sb.prep_ships()
        
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    
    # Обнуление списков пришельцев и пуль.
    aliens.empty()
    bullets.empty()
    
    # Создание нового флота и центрирование корабля.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
    
    # Пауза.
    sleep(0.5)
    
def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens,
        bullets):
    #Проверка, достиг ли хоть один пришелец нижнего края экрана
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # То же поведение, как и при повреждении корабля.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break
            
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    
    # Обновление состояния флота
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    # Проверка коллизии корабля и пришельца.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # Проверка достижения пришельцем нижнего края экрана.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
            
def get_number_of_aliens_in_row(ai_settings, alien_width):
    #Определяет, какое количество инопланетян поместится в ряд
    return int(ai_settings.screen_width / ((2 * alien_width)+1))
    
def get_number_rows(ai_settings, ship_height, alien_height):
    #Определяет, какое количество иноплянетян поместится в вертикальный ряд
    return int((ai_settings.screen_height - (3 * alien_height + ship_height)) / (2 * alien_height))
    
def create_alien(ai_settings, screen, aliens, alien_number_in_row, row_number):
    # Создает пришельца
    alien = Alien(ai_settings, screen)
    alien.x = alien.rect.width + 2 * alien.rect.width * alien_number_in_row
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    # Созадет флот из пришельцев
    # Созадет пришельца и на его основании строит остальное.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_of_aliens_in_row(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    
    # Создание флота.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                row_number)
