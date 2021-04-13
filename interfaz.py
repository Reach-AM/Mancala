import pathlib
import platform
import pygame
import random

random.seed(random.SystemRandom().randint(0,123))

# Referencia
# https://www.youtube.com/watch?v=FfWpgLFMI7w
# Set up de la plataforma
path = str(pathlib.Path(__file__).parent.absolute())
if platform.system() == "Darwin":
  path += "/"
else:
  path += "\\"

#Assets
icono = pygame.image.load(path + 'mancala.png')
tablero = pygame.image.load(path + 'tablero.png')
stones = pygame.image.load(path + 'stones.png')

    


# Set up de la ventana
pygame.init()
screen = pygame.display.set_mode((1200,500))
pygame.display.set_caption("Mancala")
pygame.display.set_icon(icono)
playing = True

# Tablero
def Tablero():
  screen.blit(tablero, (87.5, 100))
  
# Semillas
semillas = [[[0]]]*14
for i in range(6):
  grupoA = [[[0]]]*4
  grupoB = [[[0]]]*4
  for j in range(4):
    if(j==0): offset = [0,0]
    elif(j==1): offset = [0,25]
    elif(j==2): offset = [25,0]
    else: offset = [25,25]
    grupoA[j] = [175 + 125*i + offset[0], 50 + offset[1], random.randint(0, 4)*25, random.randint(0,2)*25]
    grupoB[j] = [175 + 125*i+ offset[0], 225 + offset[1], random.randint(0, 4)*25, random.randint(0,2)*25]
  semillas[i] = grupoA
  semillas[i+7] = grupoB

def Semillas():
  for grupo in semillas:
    for semilla in grupo:
      if not(semilla[0] == 0):
        screen.blit(stones, (semilla[0] + 87.5, semilla[1] + 100), (semilla[2],semilla[3],25,25))

# Draw
while playing:
  screen.fill((64, 98, 102))
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  Tablero()
  Semillas()

  pygame.display.update()
