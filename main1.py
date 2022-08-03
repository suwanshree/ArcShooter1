import pygame
import sys
import random
import pickle

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 130))
    screen.blit(floor_surface, (floor_x_pos + 1280, 130))


def create_building1():
    random_building_pos = random.choice(building1_height)
    bottom_building = building1_surface.get_rect(midtop=(2000, random_building_pos))
    return bottom_building


def draw_buildings1(buildings):
    for building in buildings:
        screen.blit(building1_surface, building)


def create_building2():
    random_building_pos = random.choice(building2_height)
    bottom_building = building2_surface.get_rect(midtop=(1500, random_building_pos))
    return bottom_building


def draw_buildings2(buildings):
    for building in buildings:
        screen.blit(building2_surface, building)


def create_building3():
    random_building_pos = random.choice(building3_height)
    bottom_building = building3_surface.get_rect(midtop=(1700, random_building_pos))
    return bottom_building


def draw_buildings3(buildings):
    for building in buildings:
        screen.blit(building3_surface, building)


def move_buildings(buildings):
    for building in buildings:
        building.centerx -= 3
    return buildings

def stop_buildings(buildings):
    for building in buildings:
        building.centerx += 3
    return buildings


def check_collision(buildings1, buildings2, buildings3):
    for building in buildings1:
        if ship_rect.colliderect(building):
            return False
    for building in buildings2:
        if ship_rect.colliderect(building):
            return False
    for building in buildings3:
        if ship_rect.colliderect(building):
            return False

    if ship_rect.top <= -100 or ship_rect.bottom >= 720:
        return False

    return True


def rotate_ship(ship):
    new_ship = pygame.transform.rotozoom(ship, -ship_movement * 3, 1)
    return new_ship


def ship_animation():
    new_ship = ship_frames[ship_index]
    new_ship_rect = new_ship.get_rect(center=(200, ship_rect.centery))
    return new_ship, new_ship_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(f'Distance: {str(score)} kms', True, (118, 118, 118))
        score_rect = score_surface.get_rect(center=(120, 705))
        screen.blit(score_surface, score_rect)

        control_surface = game_font.render(f'Boost: Space - Hover: X (Hold) - Restart: R', True, (120, 120, 120))
        control_rect = control_surface.get_rect(center=(970, 705))
        screen.blit(control_surface, control_rect)

        pygame.draw.rect(screen, black, [250, 682, 402, 34])
        pygame.draw.rect(screen, grey, [251, 683, 400, 32])
        pygame.draw.rect(screen, black, [255, 687, boost, 24])


    if game_state == 'game_over':
        score_surface = game_font.render(f'Distance: {str(score)} kms', True, (180, 150, 150))
        score_rect = score_surface.get_rect(center=(640, 200))
        screen.blit(score_surface, score_rect)

        reason_surface = game_font.render(f'{over_message}', True, (180, 150, 150))
        reason_rect = reason_surface.get_rect(center=(640, 420))
        screen.blit(reason_surface, reason_rect)

        high_score_surface = game_font.render(f'Highest Distance: {str(high_score)} kms', True, (180, 150, 150))
        high_score_rect = high_score_surface.get_rect(center=(640, 560))
        screen.blit(high_score_surface, high_score_rect)

        new_game_surface = game_font.render(f'Restart: Enter - Quit: Esc', True, (180, 150, 150))
        new_game_rect = new_game_surface.get_rect(center=(640, 700))
        screen.blit(new_game_surface, new_game_rect)

    if game_state == 'game_start':
        high_score_surface = game_font.render(f'Highest Distance: {str(high_score)} kms', True, (180, 150, 150))
        high_score_rect = high_score_surface.get_rect(center=(640, 420))
        screen.blit(high_score_surface, high_score_rect)

        new_game_surface = game_font.render(f'Start: Enter - Quit: Esc', True, (180, 150, 150))
        new_game_rect = new_game_surface.get_rect(center=(640, 700))
        screen.blit(new_game_surface, new_game_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
        with open('score.dat', 'wb') as file:
            pickle.dump(high_score, file)
    return high_score


pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=256)
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
game_font = pygame.font.Font('assets/distant galaxy 2.ttf', 24)

# Game Variables

gravity = 0.04
ship_movement = 0
movement = True
game_active = False
game_start = True
game_paused = False
boost = 392
over_message = 'Your ship hit a building or went out of bounds!'
bogey_collision = 'Your ship collided with another ship!'

grey = pygame.color.Color('#808080')
black = pygame.color.Color('#000000')
score = 0
try:
    with open('score.dat', 'rb') as file:
        high_score = pickle.load(file)
except:
    high_score = 0


pygame.display.set_caption("ArcShooter")
icon = pygame.image.load('assets/icon0.png')
pygame.display.set_icon(icon)
counter = 0

bg_surface1 = pygame.image.load('assets/shooterbkg2.png').convert()
bg_surface2 = pygame.image.load('assets/shooterbkg3.png').convert()
bg_surface3 = pygame.image.load('assets/shooterbkg4.png').convert()
bg_surface4 = pygame.image.load('assets/shooterbkg5.png').convert()
floor_surface = pygame.image.load('assets/movingbkg.png').convert_alpha()
cloud1_surface = pygame.image.load('assets/cloud.png').convert_alpha()
cloud2_surface = pygame.image.load('assets/cloud1.png').convert_alpha()
floor_x_pos = 0
cloud1_x_pos = 1280
cloud2_x_pos = 2000

ship_downvec = pygame.image.load('assets/ship1.png').convert_alpha()
ship_downvec = pygame.transform.scale(ship_downvec, (80, 20))
ship_midvec = pygame.image.load('assets/ship2.png').convert_alpha()
ship_midvec = pygame.transform.scale(ship_midvec, (80, 20))
ship_upvec = pygame.image.load('assets/ship3.png').convert_alpha()
ship_upvec = pygame.transform.scale(ship_upvec, (80, 20))
ship_frames = [ship_downvec, ship_midvec, ship_upvec]
ship_index = 2
ship_surface = ship_frames[ship_index]
shipX = 200
shipY = 420
ship_rect = ship_surface.get_rect(center=(shipX, shipY))
SHIPVEC = pygame.USEREVENT + 1
pygame.time.set_timer(SHIPVEC, 100)

building1 = pygame.image.load('assets/build1.png').convert_alpha()
building1_surface = building1
building1_list = []
SPAWNBUILDING1 = pygame.USEREVENT
pygame.time.set_timer(SPAWNBUILDING1, 750)
building1_height = [220, 250, 350, 450, 500, 550]

building2 = pygame.image.load('assets/build2.png').convert_alpha()
building2_surface = building2
building2_list = []
SPAWNBUILDING2 = pygame.USEREVENT
pygame.time.set_timer(SPAWNBUILDING2, 1500)
building2_height = [200, 228, 364, 439, 565, 592]

building3 = pygame.image.load('assets/build3.png').convert_alpha()
building3_surface = building3
building3_list = []
SPAWNBUILDING3 = pygame.USEREVENT
pygame.time.set_timer(SPAWNBUILDING3, 2250)
building3_height = [190, 290, 378, 419, 449, 497]

bogey1_downvec = pygame.image.load('assets/bogey1a.png').convert_alpha()
bogey1_midvec = pygame.image.load('assets/bogey1b.png').convert_alpha()
bogey1_upvec = pygame.image.load('assets/bogey1c.png').convert_alpha()
bogey1_frames = [bogey1_downvec, bogey1_midvec, bogey1_upvec]
bogey1_index = 0
bogey1_surface = bogey1_frames[bogey1_index]
bogey1X = 1400
bogey1Y = random.randint(60, 220)
bogey1_rect = bogey1_surface.get_rect(center=(bogey1X, bogey1Y))
BOGEY1VEC = pygame.USEREVENT + 1
pygame.time.set_timer(BOGEY1VEC, 100)

game_over_surface = pygame.image.load('assets/gameover.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(640, 360))

game_start_surface = pygame.image.load('assets/gamestart.png').convert_alpha()
game_start_rect = game_start_surface.get_rect(center=(640, 360))

while True:

    if boost > 392:
        boost = 392
    elif boost < 0:
        boost = 0
    if boost < 100:
        movement = False
    else:
        movement = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            ship_movement = 0
            ship_movement -= 2
            boost -= 5
        if keys[pygame.K_x]:
            ship_movement = -gravity
            boost -= 5
        if keys[pygame.K_RETURN] and game_active is False:
            game_active = True
            game_start = False
            building1_list.clear()
            building2_list.clear()
            building3_list.clear()
            ship_rect.center = (shipX, shipY)
            ship_movement = 0
            score = 0
            boost = 392
            bogey1X = 2000
            bogey1Y = random.randint(70, 220)
        if keys[pygame.K_r] and game_active is True:
            game_active = True
            game_start = False
            building1_list.clear()
            building2_list.clear()
            building3_list.clear()
            ship_rect.center = (shipX, shipY)
            ship_movement = 0
            score = 0
            boost = 392
            bogey1X = 2000
            bogey1Y = random.randint(70, 220)
        if keys[pygame.K_p]:
            game_paused = True
        if keys[pygame.K_p] and game_paused is True:
            game_paused = False
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        boost += 1



        if event.type == SPAWNBUILDING1:
            building1_list.append(create_building1())
        if event.type == SPAWNBUILDING2:
            building2_list.append(create_building2())
        if event.type == SPAWNBUILDING3:
            building3_list.append(create_building3())

        if event.type == SHIPVEC:
            if ship_index < 2:
                ship_index += 1
            else:
                ship_index = 0

            ship_surface, ship_rect = ship_animation()

    # Background

    if counter == 0:
        screen.blit(bg_surface1, (0, 0))
        counter = 1
    elif counter == 1:
        screen.blit(bg_surface2, (0, 0))
        counter = 2
    elif counter == 2:
        screen.blit(bg_surface3, (0, 0))
        counter = 3
    elif counter == 3:
        screen.blit(bg_surface4, (0, 0))
        counter = 0

    # Floor

    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -1280:
        floor_x_pos = 0

    if game_active:

        # Ship

        ship_movement += gravity
        rotated_ship = rotate_ship(ship_surface)
        ship_rect.centery += ship_movement
        screen.blit(rotated_ship, ship_rect)
        game_active = check_collision(building1_list, building2_list, building3_list)

        # Buildings

        building1_list = move_buildings(building1_list)
        draw_buildings1(building1_list)
        building2_list = move_buildings(building2_list)
        draw_buildings2(building2_list)
        building3_list = move_buildings(building3_list)
        draw_buildings3(building3_list)

        score += 1
        score_display('main_game')

        # Contacts

        bogey1X -= 2
        bogey1_surface = bogey1_frames[bogey1_index]
        bogey1_index += 1
        screen.blit(bogey1_surface, (bogey1X, bogey1Y))
        if bogey1X <= -400:
            bogey1X = 1400
            bogey1Y = random.randint(70, 220)
        if bogey1_index > 2:
            bogey1_index = 0
        bogey1_rect = bogey1_surface.get_rect(center=(bogey1X, bogey1Y))
        if ship_rect.colliderect(bogey1_rect):
            over_message = bogey_collision
            game_active = False


    elif game_start:
        screen.blit(game_start_surface, game_start_rect)
        high_score = update_score(score, high_score)
        score_display('game_start')

    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Pause
    if game_paused:
        screen.blit(game_over_surface, game_over_rect)
        building1_list = stop_buildings(building1_list)
        building2_list = stop_buildings(building2_list)
        building3_list = stop_buildings(building3_list)
        bogey1X += 2

    # Clouds

    cloud1_x_pos -= .5
    screen.blit(cloud1_surface, (cloud1_x_pos, 50))
    if cloud1_x_pos <= -400:
        cloud1_x_pos = 1280
    cloud2_x_pos -= .5
    screen.blit(cloud2_surface, (cloud2_x_pos, 110))
    if cloud2_x_pos <= -400:
        cloud2_x_pos = 2000

    pygame.display.update()
    clock.tick(60)
