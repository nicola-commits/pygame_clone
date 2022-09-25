# flappy bird clone
import pygame

from background import Background
from bird import Bird
import random

pygame.init()
pygame.font.init()
defFont = pygame.font.get_default_font()
sysFont = pygame.font.SysFont(defFont, 30)

screensize = (800, 600)
backgroundcolor = (50, 250, 255)

screen = pygame.display.set_mode(screensize)
clock = pygame.time.Clock()

bird = Bird(r"res/bird.png")
background = Background(screen, color=backgroundcolor)
running = True

while running:

    screen.fill(background.color)
    background.moveSky(screen, 1 / 60)
    background.showTerrain(screen)
    screen.blit(bird.surface, (bird.x, bird.y))

    keys = pygame.key.get_pressed()
    pressed = False

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            pressed = True
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    bird.update(pressed, 1 / 60)
    if bird.y > screensize[1]:
        running = False
        pygame.quit()
        exit(0)

    background.updateObjects(screen, 1 / 60, bird)

    score = sysFont.render(f"your score is: {background.removed}", True, (0, 0, 0))
    screen.blit(score, (0, 0))

    pygame.display.flip()

    clock.tick(60)
