import pygame
import numpy as np
import time

pygame.init()

width, height = 1000, 1000
screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25
screen.fill(bg)

nxC, nyC = 25, 25

dimCW = width / nxC
dimCH = height / nyC

# Cells' state. Alive == 1; Death == 0
gameState = np.zeros((nxC, nyC))

# Stick automata.
gameState[5,3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

# Movil automata.
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

# Execution Loop
while True:

  newGameState = np.copy(gameState)

  screen.fill(bg)
  time.sleep(0.1)
  
  for y in range(0, nxC):
    for x in range(0, nyC):

      # Calculates the number of neighbours (toroidal approach)
      n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + \
                gameState[(x)   % nxC, (y-1) %  nyC] + \
                gameState[(x+1) % nxC, (y-1) % nyC] + \
                gameState[(x-1) % nxC, (y) % nyC] + \
                gameState[(x+1) % nxC, (y) % nyC] + \
                gameState[(x-1) % nxC, (y + 1) % nyC] + \
                gameState[(x)   % nxC, (y + 1) % nyC] + \
                gameState[(x + 1) % nxC, (y + 1) % nyC]

      # Rule #1 : A dead cell with exactly 3 alive neighbours, revives.
      if gameState[x, y] == 0 and n_neigh == 3:
        newGameState[x, y] = 1

      # Rule #2 : An alive cell with less than 2 or more than 3 alive neighbours, die.
      elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
        newGameState[x, y] = 0

      # Creates the polygon of each cell to display it.
      poly = [
        (  x   * dimCW,    y    * dimCH),
        ((x+1) * dimCW,    y    * dimCH),
        ((x+1) * dimCW, (y + 1) * dimCH),
        (  x   * dimCW, (y + 1) * dimCH)
      ]

      # Draws the cell for each (x, y) pair.
      if newGameState[x, y] == 0:
        pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
      else:
        pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

  #Updates the game's state
  gameState = np.copy(newGameState)

  # Renders the screen
  pygame.display.flip()