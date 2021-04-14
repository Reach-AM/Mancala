# -*- coding: utf-8 -*-
"""Mancala con ascii.ipynb

Automatically generated by Colaboratory.

# MANCALA

### Librerías auxiliares
"""
import copy as cp
import math

"""## Nodos
Estos nodos son la estructura de datos que forman el árbol generado por minmax.
En ellos se almacena la posición, el movimiento que llevo a esa jugada, los
posibles movimientos siguietnes, el puntaje heurístico de la posición y el
puntaje final al que lleva esa jugada.
"""

class Nodo:
  def __init__(self, b, mov):
    self.movimiento = mov
    self.posicion = b[0]
    self.estado = b[1]
    self.h = self.__score()
    self.movimientos = []
    self.f = True

  def __score(self):
    score = 0
    for i in range(6):
      score += self.posicion[i] * -30 * i
      score += self.posicion[i + 7] * 30 * i
    score += self.posicion[6] * -250
    score += self.posicion[13] * 250
    return score

  def nodo_posible(self, n):
    if (len(self.movimientos) > 0):
      if (n.h < self.movimientos[len(self.movimientos)-1].h):
        self.movimientos = self.movimientos + [n]
      else:
        for i in range(len(self.movimientos)):
          if (n.h >= self.movimientos[i].h):
            self.movimientos = self.movimientos[0:i] + [n] + self.movimientos[i:]
            break
    else:
      self.movimientos = [n]

"""## Mancala
Este es el juego de mesa y la inteligencia artificial que juega con nombre de cpu.
"""

class Mancala:
  def __init__(self, profundidad):
    self.board = [4,4,4,4,4,4,0,4,4,4,4,4,4,0]
    print("============ MANCALA ============\n")
    self.__imprimirTablero(self.board)
    print("=================================\n")
    self.profundidad = profundidad
    self.inv = {7:5, 8:4, 9:3, 10:2, 11:1, 12:0,
              5:7, 4:8, 3:9, 2:10, 1:11, 0:12}

  ##############################################################################
  ############################# COMIENZO DEL JUEGO #############################
  ##############################################################################

  def jugar(self):
    mancala = [self.board, False]
    print("\n========== ES TU TURNO ==========\n")
    mancala = self.__jugador(mancala)
    while (not self.__game_over(mancala[0])):
      if (mancala[1]):
        print("\n========= TURNO DEL CPU =========\n")
        mancala = self.__cpu(mancala)
      else:
        print("\n========== ES TU TURNO ==========\n")
        mancala = self.__jugador(mancala)
    mancala[0] = self.__finalizar(mancala[0])
    print("\n======= JUEGO  FINALIZADO =======\n")
    self.__imprimirTablero(mancala[0])
    print("=================================\n")

  ##############################################################################
  ######################### TURNOS DEL JUGADOR Y LA IA #########################
  ##############################################################################

  def __jugador(self, m):
    while(not m[1]):
      x = int(input())
      if (x <= 0 or x > 6 or self.board[x - 1] == 0):
        print("NO VALIDO!")
      else:
        m = self.__turno(x, m[1], m[0])
        if (self.__game_over(m[0])):
          return m
        self.__imprimirTablero(m[0])
        m[1] = not m[1]
    return m

  def __cpu(self, m):
    while(m[1]):
      x = self.__next(m[0])
      print(x)
      m = self.__turno(x + 7, m[1], m[0])
      if(self.__game_over(m[0])):
          return m
      self.__imprimirTablero(m[0])
    return m

  ##############################################################################
  #################### FUNCIÓN PARA LLEVAR ACABO LOS TURNOS ####################
  ##############################################################################

  def __turno(self, x, y, b):
    semillas = b[x - 1]
    b[x - 1] = 0
    offset = 0
    for i in range(semillas):
      if (x + i + offset >= len(b)):
        pos = x + i + offset - len(b) * math.floor((x + i + offset)/len(b))
      else:
        pos = x + i + offset

      if (i == semillas - 1):
        if (y):
          if (pos == 13):
            b[pos] += 1
            return [b,True]
          elif (b[pos] == 0 and pos >= 7 and pos < 13 and b[self.inv[pos]] > 0):
            b[13] += self.__robo(pos, b) + 1
          elif (pos == 6):
            if(b[x + semillas - len(b)] == 0):
              b[13] += self.__robo(x + semillas - len(b), b) + 1
            else:
              b[x + semillas - len(b)] += 1
          else:
            b[pos] += 1
        else:
          if (pos == 6):
            b[pos] += 1
            return [b,True]
          elif (b[pos] == 0 and pos >= 0 and pos < 6 and b[self.inv[pos]] > 0):
            b[6] += self.__robo(pos, b) + 1
          elif (pos == 13):
            if(b[x + semillas - len(b)] == 0):
              b[6] += self.__robo(x + semillas - len(b), b) + 1
            else:
              b[x + semillas - len(b)] += 1
          else:
            b[pos] += 1
      else:
        if (y and pos == 6) or (not y and pos == 13):
          offset += 1
          pos += 1
          if (pos >= len(b)):
            pos -= len(b)
        b[pos] += 1
    return [b,False]

  ##############################################################################
  ##################### FUNCIÓN PARA LLEVAR ACABO LOS ROBOS ####################
  ##############################################################################

  def __robo(self, n, b):
    if (n == 0 or n == 12):
      stealed_seeds = b[0] + b[12]
      b[0] = 0
      b[12] = 0
    elif (n == 1 or n == 11):
      stealed_seeds = b[1] + b[11]
      b[1] = 0
      b[11] = 0
    elif (n == 2 or n == 10):
      stealed_seeds = b[2] + b[10]
      b[2] = 0
      b[10] = 0
    elif (n == 3 or n == 9):
      stealed_seeds = b[3] + b[9]
      b[3] = 0
      b[9] = 0
    elif (n == 4 or n == 8):
      stealed_seeds = b[4] + b[8]
      b[4] = 0
      b[8] = 0
    elif (n == 5 or n == 7):
      stealed_seeds = b[5] + b[7]
      b[5] = 0
      b[7] = 0
    return stealed_seeds

  ##############################################################################
  ##################### FUNCIÓN PARA REVISAR SI YA TERMINÓ #####################
  ##############################################################################

  def __game_over(self, b):
    vacio = True
    for i in range(6):
      if (b[i] > 0):
        vacio = False
        break
    if (vacio):
      return vacio
    vacio = True
    for i in range(6):
      if (b[i+7]) > 0:
        vacio = False
        break
    return vacio

  ##############################################################################
  ################### FUNCIÓN PARA HACER LOS AJUSTES FINALES ###################
  ##############################################################################

  def __finalizar(self, board):
    b = cp.copy(board)
    for i in range(6):
      b[6] += b[i]
      b[i] = 0
      b[13] += b[i + 7]
      b[i + 7] = 0
    return b

  ##############################################################################
  ############## FUNCIÓN PARA PEDIR LA SIGUIENTE JUGADA DE LA IA ###############
  ##############################################################################

  def __next(self, b):
    n = Nodo([b,True], -1)
    next = self.minimax(n, self.profundidad, -999999, 999999, n.estado)
    for mov in n.movimientos:
      if (mov.f >= next):
        return mov.movimiento

  ##############################################################################
  #################### MÉTODO MINMAX CON ALPHA-BETA PRUNING ####################
  ##############################################################################

  def minimax(self, actual, profundidad, alpha, beta, maximizar):
    if (profundidad == 0):
      return actual.h
    elif (self.__game_over(actual.posicion)):
      provisional = Nodo([self.__finalizar(actual.posicion), False],-1)
      return provisional.h

    for i in range(6):
      b = cp.copy(actual.posicion)
      if maximizar:
        j = i + 8
      else:
        j = i + 1
      if (b[j-1] > 0):
        pos_i = self.__turno(j,maximizar,b)
        hijo = Nodo(pos_i,i+1)
        actual.nodo_posible(hijo)

    if (maximizar):
      maxEval = -999999
      for n in actual.movimientos:
        eval = self.minimax(n, profundidad-1, alpha, beta, n.estado)
        n.f = eval
        maxEval = max(maxEval, eval)
        alpha = max(alpha, eval)
        if beta <= alpha:
          break
      return maxEval

    else:
      minEval = 999999
      for n in reversed(actual.movimientos):
        eval = self.minimax(n, profundidad-1, alpha, beta, not n.estado)
        n.f = eval
        minEval = min(minEval, eval)
        beta = min(beta, eval)
        if beta <= alpha:
          break
      return minEval

    ##############################################################################
    ####################### MÉTODO PARA IMPRIMIR EL TABLERO ######################
    ##############################################################################

  def __imprimirTablero(self, b):
    print(" /  |",b[12],"|",b[11],"|",b[10],"|",b[9],"|",b[8],"|",b[7],"|  \\\n")
    print("|",b[13],"|                       |",b[6],"|\n")
    print(" \\  |",b[0],"|",b[1],"|",b[2],"|",b[3],"|",b[4],"|",b[5],"|  /\n")

"""## Inicio del juego
Desde aquí se lleva a cabo el inicio del juego. Lo único que se le pasa al objeto
Manacala es la profunidad, que se puede considerar la dificultad del oponente.

*12 es la mejor profundidad, antes de que la ia tome tiempos muy excesivos antes
de hacer su tirada*
"""

game = Mancala(12)
game.jugar()
