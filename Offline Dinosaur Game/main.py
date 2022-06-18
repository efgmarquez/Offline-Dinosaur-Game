import pygame
import sys
import random
import settings
import sprites


WINDOW = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption("You are not connected to the internet.")

CREATE_OBSTACLE = pygame.USEREVENT
pygame.time.set_timer(CREATE_OBSTACLE, 1500)

def draw_window():
    if sprites.ongoing:
        WINDOW.fill(settings.BACKGROUND)
        WINDOW.blit(sprites.ground.image, (sprites.ground.x, sprites.ground.y))
        WINDOW.blit(sprites.ground.image, (sprites.ground.x + 600, sprites.ground.y))
        WINDOW.blit(sprites.cloud.image, (sprites.cloud.x, sprites.cloud.y))
        WINDOW.blit(sprites.dinosaur.image, (sprites.dinosaur.x, sprites.dinosaur.y))
        
        text = sprites.font.render("Score: " + str(int(settings.SCORE)), True, (0,0,0))
        WINDOW.blit(text, (530, 10))

        for obstacle in sprites.obstacles:
            WINDOW.blit(obstacle.image, (obstacle.x, obstacle.y))

    else:
        WINDOW.blit(sprites.game_over, (200, 40))
        WINDOW.blit(sprites.replay, (280, 60))

    pygame.display.update()

def create_obstacle():
    index = random.randint(0,2)     

    if index == 0:
        sprites.SmallCactus(random.randint(600, 650), 100)
    elif index == 1:
        sprites.BigCactus(random.randint(600, 650), 90)
    else: 
        sprites.Bird(random.randint(600, 650), random.choice([20, 55, 90]))

def score():
    if sprites.ongoing:
        settings.SCORE += 0.1

def main():
    clock = pygame.time.Clock()
    sprites.ongoing = True
    sprites.obstacles.clear()
    settings.SCORE = 0
    sprites.dinosaur.y = 90

    while True:
        clock.tick(settings.FPS) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if sprites.ongoing:
                    if sprites.dinosaur.is_running == True:
                        if event.key == pygame.K_DOWN:
                            sprites.dinosaur.duck()
                        elif event.key == pygame.K_UP:
                            pygame.mixer.Sound.play(sprites.jump_sound)
                            sprites.dinosaur.jump()
                else:
                        main()
            if event.type == pygame.KEYUP:
                if sprites.dinosaur.is_ducking == True:
                    if event.key == pygame.K_DOWN:
                        sprites.dinosaur.unduck()
            if event.type == CREATE_OBSTACLE:
                create_obstacle()
                

        sprites.dinosaur.animate()
        sprites.ground.move()
        sprites.cloud.move()
        for obstacle in sprites.obstacles:
            obstacle.move()
            if pygame.Rect.colliderect(sprites.dinosaur.rect, obstacle.rect):
                if sprites.ongoing == True:
                    pygame.mixer.Sound.play(sprites.die_sound)
                sprites.ongoing = False

        draw_window()
        score()

        
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                main()
                
        WINDOW.fill(settings.BACKGROUND)
        WINDOW.blit(sprites.ground.image, (sprites.ground.x, sprites.ground.y))
        WINDOW.blit(sprites.dinosaur.image, (sprites.dinosaur.x, sprites.dinosaur.y))
        text = sprites.main_menu_font.render("Press Any Key", True, (0,0,0))
        WINDOW.blit(text, (230, 45))
        pygame.display.update()



if __name__ == "__main__":
    main_menu()
    