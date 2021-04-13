import pygame
import pathlib

# https://www.youtube.com/watch?v=FfWpgLFMI7w

path = pathlib.Path(__file__).parent.absolute()
pygame.init()

# Set up de la interfaz
screen = pygame.display.set_mode((1200,500))
pygame.display.set_caption("Mancala")
print(str(path) + '\mancala.png')
icono = pygame.image.load(str(path) + '\mancala.png')
pygame.display.set_icon(icono)


playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((64, 98, 102))

    pygame.display.update()
