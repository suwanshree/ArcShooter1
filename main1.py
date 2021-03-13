import pygame
import sys
import random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 525))
    screen.blit(floor_surface, (floor_x_pos + 1280, 525))


def create_building():
    random_building_pos = random.choice(building_height)
    bottom_building = building_surface.get_rect(midtop=(1500, random_building_pos))
    top_building = 0
    return bottom_building


def move_buildings(buildings):
    for building in buildings:
        building.centerx -= 5
    return buildings


def draw_buildings(buildings):
    for building in buildings:
        screen.blit(building_surface, building)


def check_collision(buildings):
    for building in buildings:
        if ship_rect.colliderect(building):
            print("Object collision")
            return False

    if ship_rect.top <= -100 or ship_rect.bottom >= 720:
        print("Out of bounds")
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
    if game_state == 'game_over':
        score_surface = game_font.render(f'Distance: {str(score)} kms', True, (180, 150, 150))
        score_rect = score_surface.get_rect(center=(640, 300))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'Highest Distance: {str(high_score)} kms', True, (180, 150, 150))
        high_score_rect = high_score_surface.get_rect(center=(640, 420))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=256)
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
game_font = pygame.font.Font('distant galaxy 2.ttf', 24)

# Game Variables

gravity = 0.04
ship_movement = 0
game_active = True
score = 0
high_score = 0

pygame.display.set_caption("ArcShooter")
icon = pygame.image.load('icon0.png')
pygame.display.set_icon(icon)
counter = 0

bg_surface1 = pygame.image.load('shooterbkg2.png').convert()
bg_surface2 = pygame.image.load('shooterbkg3.png').convert()
floor_surface = pygame.image.load('movingbkg.png').convert_alpha()
cloud1_surface = pygame.image.load('cloud.png').convert_alpha()
cloud2_surface = pygame.image.load('cloud1.png').convert_alpha()
floor_x_pos = 0
cloud1_x_pos = 1280
cloud2_x_pos = 2000

ship_downvec = pygame.image.load('ship1.png').convert_alpha()
ship_downvec = pygame.transform.scale(ship_downvec, (80, 20))
ship_midvec = pygame.image.load('ship2.png').convert_alpha()
ship_midvec = pygame.transform.scale(ship_midvec, (80, 20))
ship_upvec = pygame.image.load('ship3.png').convert_alpha()
ship_upvec = pygame.transform.scale(ship_upvec, (80, 20))
ship_frames = [ship_downvec, ship_midvec, ship_upvec]
ship_index = 2
ship_divert = False
ship_surface = ship_frames[ship_index]
ship_rect = ship_surface.get_rect(center=(200, 420))
SHIPVEC = pygame.USEREVENT + 1
pygame.time.set_timer(SHIPVEC, 100)

building1 = pygame.image.load('build1.png').convert_alpha()
building2 = pygame.image.load('build2.png').convert_alpha()
building3 = pygame.image.load('build3.png').convert_alpha()
building_types = [building1, building2, building3]
building_index = random.randint(0, 2)
building_surface = building_types[building_index]
building_list = []
SPAWNBUILDING = pygame.USEREVENT
pygame.time.set_timer(SPAWNBUILDING, 800)
building_height = [500, 350, 300, 330, 470, 450]

game_over_surface = pygame.image.load('gameover.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(640, 360))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            ship_movement = 0
            ship_movement -= 2
        if keys[pygame.K_DOWN]:
            ship_movement = -gravity
        if keys[pygame.K_SPACE] and game_active is False:
            game_active = True
            building_list.clear()
            ship_rect.center = (200, 420)
            ship_movement = 0
            score = 0

        if event.type == SPAWNBUILDING:
            building_list.append(create_building())

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
        print('ship_rect_centery: ', ship_rect.centery)
        print('ship_movement: ', ship_movement)
        ship_rect.centery += ship_movement
        screen.blit(rotated_ship, ship_rect)
        game_active = check_collision(building_list)

        # Buildings

        building_list = move_buildings(building_list)
        draw_buildings(building_list)

        score += 1
        score_display('main_game')
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

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
    clock.tick(120)
