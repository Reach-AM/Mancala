import pathlib
import platform
import pygame
import random

random.seed(random.SystemRandom().randint(0,123))

# Referencia
# https://www.youtube.com/watch?v=FfWpgLFMI7w

############################################################
######################## Plataforma ########################
############################################################

path = str(pathlib.Path(__file__).parent.absolute())
if platform.system() == "Darwin":
  path += "/"
else:
  path += "\\"

############################################################
########################## Assets ##########################
############################################################

icono = pygame.image.load(path + 'mancala.png')
tablero = pygame.image.load(path + 'tablero.png')
stones = pygame.image.load(path + 'stones.png')
numbers = pygame.image.load(path + 'numbers.png')

############################################################
########################## Set up ##########################
############################################################

pygame.init()
screen = pygame.display.set_mode((1200,500))
pygame.display.set_caption("Mancala")
pygame.display.set_icon(icono)
playing = True

############################################################
##################### Pequeños ajustes #####################
############################################################

num_score = {}
for i in range(10):
    num_score[i] = 12 * (i+1) + 18 * (i)

def Tablero():
  screen.blit(tablero, (87.5, 100))

############################################################
######################### Semillas #########################
############################################################

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
  semillas[i+7] = grupoA
  semillas[i] = grupoB
semillas = semillas[0:7] + list(reversed(semillas[7:13])) + [semillas[13]]
def Semillas():
  for grupo in semillas:
    for semilla in grupo:
      if not(semilla[0] == 0):
        screen.blit(stones, (semilla[0] + 87.5, semilla[1] + 100), (semilla[2],semilla[3],25,25))

############################################################
########################### Score ##########################
############################################################

def Scoreboard():
  for i in range(len(semillas)):
    if (i < 6):
      drawScore(175 + 125 * i + 87.5, 445, i)
    elif (i == 6):
      drawScore(10,10, i)
    elif (i < 13):
      drawScore(175 + 125 * (i-7) + 87.5, 60, i)
    else:
      drawScore(1200-28, 10, i)

def drawScore(x,y,i):
  grupo = semillas[i]
  if len(grupo) == 1 and grupo[0][0] == 0:
    screen.blit(numbers, (x, y), (num_score[0], 12, 18, 30))
  else:
    screen.blit(numbers, (x, y), (num_score[len(grupo)], 12, 18, 30))

# Scoreboard()

############################################################
########################### Menu ###########################
############################################################

def MainMenu():
    while True:
        screen.fill((64, 98, 102))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        button_start = pygame.Rect(500, 300, 200, 75)
        pygame.draw.rect(screen, (255, 0, 0), button_start)
        if button_start.collidepoint((mouse_x, mouse_y)):
          if click:
            GameStart()

        click = False

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

        pygame.display.update()

############################################################
########################### Game ###########################
############################################################
def GameStart():
    while playing:
      screen.fill((64, 98, 102))
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          exit()

      Tablero()
      Semillas()
      Scoreboard()

      pygame.display.update()

MainMenu()
