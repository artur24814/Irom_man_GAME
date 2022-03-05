import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 6

            if obstacle_rect.bottom == 387:
                screen.blit(car_surf,obstacle_rect)
            else:
                screen.blit(fly_surf,obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def player_animation():
    global player_surf
    if player_rect.bottom < 391:
        player_surf = player_jump
    else:
        player_surf = pygame.image.load('graphics/men1.png').convert_alpha()
        player_surf = pygame.transform.scale(player_surf, (65, 90))


pygame.init()
screen = pygame.display.set_mode((730,400))
pygame.display.set_caption('iron man Game')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/Theme.mp3')
bg_music.set_volume(0.1)
bg_music.play(loops= -1)

sky_surf = pygame.image.load('graphics/background.jpg').convert()

# score_surf = test_font.render('My game', False, (64,64,64))
# score_rect = score_surf.get_rect(center = (400, 50))

#Obstacles
car_surf = pygame.image.load('graphics/ZuZ1.png').convert_alpha()
car_rect = car_surf.get_rect(bottomright = (700,387))

fly_surf = pygame.image.load('graphics/fly.png').convert_alpha()

obstacle_rect_list = []

player_surf = pygame.image.load('graphics/men1.png').convert_alpha()
player_surf = pygame.transform.scale(player_surf, (65,90))
player_jump = pygame.image.load('graphics/man2.png').convert_alpha()
player_jump = pygame.transform.scale(player_jump, (65,90))
player_rect = player_surf.get_rect(topleft = (0,270))
player_gravity = 0
jump_sound = pygame.mixer.Sound('audio/up.mp3')
jump_sound.set_volume(0.07)

#Start
start_surf = pygame.image.load('graphics/start.png').convert()
player_stand = pygame.image.load('graphics/stand1.png').convert_alpha()
player_stand_rect = player_stand.get_rect(center = (370,200))

game_name = test_font.render('Iron Man Game',False,(63, 37, 57))
game_name_rect = game_name.get_rect(center = (370,50))

game_message = test_font.render('Pres mouse to start',False,(63, 37, 57))
game_message_rect = game_message.get_rect(center = (370,350))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1700)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 150:
                    player_gravity = -15
                    jump_sound.play()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 150:
                    player_gravity = -15
                    jump_sound.play()
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_active = True
                car_rect.left = 730
                start_time = int(pygame.time.get_ticks() / 1000)

        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(car_surf.get_rect(bottomright = (randint(900,2000),387)))
            else:
                obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 2000),200)))




    if game_active:
        screen.blit(sky_surf,(0,0))
        # pygame.draw.rect(screen, (85, 159, 228), score_rect)
        # pygame.draw.rect(screen, (85, 159, 228), score_rect,10)
        # screen.blit(score_surf,score_rect)
        score = display_score()

        # car_rect.x -= 3
        # if car_rect.right <= 0: car_rect.left = 730
        # screen.blit(car_surf,car_rect)

        #Player
        player_gravity += 0.5
        player_rect.y += player_gravity
        if player_rect.bottom >= 391 : player_rect.bottom = 391
        player_animation()
        screen.blit(player_surf,player_rect)

        #Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #Collision
        game_active = collisions(player_rect,obstacle_rect_list)
    else:
        screen.blit(start_surf, (-100,-100))
        #screen.fill((85, 159, 228))
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,391)
        player_gravity = 0

        score_messege = test_font.render(f'Your score: {score}',False,(63, 37, 57))
        score_messege_rect = score_messege.get_rect(center = (370,350))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name,game_name_rect)
        if score == 0: screen.blit(game_message,game_message_rect)
        else: screen.blit(score_messege,score_messege_rect)




    pygame.display.update()
    clock.tick(60)