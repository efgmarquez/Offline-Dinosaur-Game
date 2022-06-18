import pygame
import os
import settings
import random

pygame.font.init()
pygame.mixer.init()

class Dinosaur(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.is_jumping = False
        self.is_running = True
        self.is_ducking = False
        self.dy = 9

        self.running_dino = [
            pygame.transform.scale(pygame.image.load(os.path.join('resources', 'dino_right_foot.png')), (35, 45)),
            pygame.transform.scale(pygame.image.load(os.path.join('resources', 'dino_left_foot.png')), (35, 45))
        ]
        self.ducking_dino = [
            pygame.transform.scale(pygame.image.load(os.path.join('resources', 'dino_ducking_right_foot.png')), (35, 25)),
            pygame.transform.scale(pygame.image.load(os.path.join('resources', 'dino_ducking_left_foot.png')), (35, 25))
        ]
        self.standing_dino = pygame.transform.scale(pygame.image.load(os.path.join('resources', 'dino_standing.png')), (35, 45))

        self.current_index = 0
        self.image = self.standing_dino
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def animate(self):
        if ongoing:
            self.current_index += 0.07
            if self.is_running:
                if self.current_index >= 2:
                    self.current_index = 0
                self.image = self.running_dino[int(self.current_index)]
                self.rect = self.image.get_rect(center=(self.x, self.y))
            elif self.is_ducking:
                self.y = 110
                if self.current_index >= 2:
                    self.current_index = 0
                self.image = self.ducking_dino[int(self.current_index)]
                self.rect = self.image.get_rect(center=(self.x, self.y))
            elif self.is_jumping:
                self.image = self.standing_dino
                self.rect = self.image.get_rect(center=(self.x, self.y))
                self.y -= self.dy
                self.rect.y -= self.dy
                self.dy -= settings.GRAVITY

                if self.y > 90:
                    self.y = 90
                    self.rect = self.image.get_rect(center=(self.x, self.y))
                    self.dy = 9
                    self.unjump()
                
    def unduck(self):
        self.y = 90
        self.is_ducking = False
        self.is_jumping = False
        self.is_running = True

    def duck(self):
        self.is_ducking = True
        self.is_jumping = False
        self.is_running = False
    
    def jump(self):
        self.is_ducking = False
        self.is_jumping = True
        self.is_running = False

    def unjump(self):
        self.is_ducking = False
        self.is_jumping = False
        self.is_running = True


class BigCactus():
    big_cacti = [
        pygame.transform.scale(pygame.image.load(os.path.join('resources', 'big_cactus1.png')), (35, 45)),
        pygame.transform.scale(pygame.image.load(os.path.join('resources', 'big_cactus2.png')), (35, 45)),
        pygame.transform.scale(pygame.image.load(os.path.join('resources', 'big_cactus3.png')), (35, 45))
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y 
        self.image = BigCactus.big_cacti[random.randint(0,2)]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        obstacles.append(self)

    def move(self):
        self.x -= settings.DX
        self.rect.x -= settings.DX
        if self.x <= -100:
            obstacles.pop(0)

class SmallCactus():
    small_cacti = [
        pygame.transform.scale(pygame.image.load(os.path.join('resources', 'small_cactus1.png')), (35, 30)),
        pygame.transform.scale(pygame.image.load(os.path.join('resources', 'small_cactus2.png')), (35, 30)),
        pygame.transform.scale(pygame.image.load(os.path.join('resources', 'small_cactus3.png')), (35, 30))
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y 
        self.image = SmallCactus.small_cacti[random.randint(0,2)]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        obstacles.append(self)

    def move(self):
        self.x -= settings.DX
        self.rect.x -= settings.DX
        if self.x <= -100:
            obstacles.pop(0)

    

class Bird():
    def __init__(self, x, y):
        self.x = x
        self.y = y 
        self.flying_bird = [
            pygame.transform.scale(pygame.image.load(os.path.join('resources', 'bird_wing_down.png')), (35, 45)),
            pygame.transform.scale(pygame.image.load(os.path.join('resources', 'bird_wing_up.png')), (35, 45))
        ]
        self.current_index = 0
        self.image = self.flying_bird[self.current_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        obstacles.append(self)
    
    def move(self):
        self.x -= settings.DX
        self.rect.x -= settings.DX
        if ongoing:
            self.current_index += 0.05

            if self.current_index >= 2:
                self.current_index = 0

        self.image = self.flying_bird[int(self.current_index)]

        if self.x <= -100:
            obstacles.pop(0)



class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x 
        self.y = y 
        self.dx = 0
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('resources', 'ground.png')), (600, 20))

    def move(self):
        self.x -= settings.DX
        if self.x <= -600:
            self.x = 0

class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x 
        self.y = y 
        self.dx = 0
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('resources', 'cloud.png')), (80, 20))

    def move(self):
        self.x -= (settings.DX * 2/5)
        if self.x <= -100:
            self.x = 600
            self.y = random.randint(20, 70)


obstacles = []
ongoing = True

#INSTANTIATE objects
dinosaur = Dinosaur(20, 90)
ground = Ground(0, 120)
cloud = Cloud(600, random.randint(20, 70))

#Other images
game_over = pygame.transform.scale(pygame.image.load(os.path.join('resources', 'game_over.png')), (190, 11))
replay = pygame.transform.scale(pygame.image.load(os.path.join('resources', 'replay_button.png')), (30, 30))

#Font
font = pygame.font.Font('freesansbold.ttf', 12)
main_menu_font = pygame.font.Font('freesansbold.ttf', 15)

#Sounds
jump_sound = pygame.mixer.Sound(os.path.join('resources', 'jump.wav'))
die_sound = pygame.mixer.Sound(os.path.join('resources', 'die.wav'))