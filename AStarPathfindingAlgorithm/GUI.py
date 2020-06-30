from PySide2 import QtWidgets, QtCore, QtGui
import pygame
from pygame.locals import *

WINDOW_WIDTH = 720  
WINDOW_HEIGHT = 840 
Columns = 25
Rows = 25
Width = int(WINDOW_WIDTH/(Columns-1))
Height = int(WINDOW_HEIGHT/(Rows-1))

class GUI():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        
        running = True
        self.startLocationSet = False
        self.endLocationSet = False
        self.obstacleLocations = []
        #self.state 

        while running:
            for event in pygame.event.get():
                if pygame.mouse.get_pressed() == (1,0,0):
                    if(self.startLocationSet != True):
                        self.setStart(pygame.mouse.get_pos())
                    elif(self.endLocationSet != True):
                        self.setEnd(pygame.mouse.get_pos())
                    else:
                        self.setObstableLocations(pygame.mouse.get_pos())
                    #elif()
                    #print(self.startLocation)
                elif event.type == pygame.QUIT:
                    running = False

            self.screen.fill((0,0,0))

            self.displayGrid()

            pygame.display.flip()

        pygame.quit()

    def displayGrid(self):
        for col in range(Columns):
            for row in range(Rows):
                pygame.draw.circle(self.screen, (200,200,200), (col*Width,row*Height), int(Width/7.5))

        for col in range(Columns):
            pygame.draw.line(self.screen,(200,200,200),(col*Width,0),(col*Width,WINDOW_HEIGHT))
        for row in range(Rows):
            pygame.draw.line(self.screen,(200,200,200),(0,row*Height),(WINDOW_WIDTH,row*Height))

        #print(self.startLocationSet)
        if (self.startLocationSet):
            pygame.draw.circle(self.screen, (0,255,0), self.startLocation, int(Width/5))
        if (self.endLocationSet):
            pygame.draw.circle(self.screen, (255,0,0), self.endLocation, int(Width/5))
        prev_pos = (0,0)
        for i,pos in enumerate(self.obstacleLocations):
            if(i !=0 and (abs(pos[0]-prev_pos[0]) == Width or abs(pos[1]-prev_pos[1]) == Height) and abs(pos[0]-prev_pos[0]) <= Width and abs(pos[1]-prev_pos[1]) <= Height):
                pygame.draw.line(self.screen, (165,42,42),pos,prev_pos, 4) 
            prev_pos = pos

    def setStart(self,pos):
        locationFound = False
        for col in range(Columns):
            for row in range(Rows):
                if( abs(pos[0]-(col*Width)) < (Width*0.34) and abs(pos[1]-(row*Height)) < (Height*0.34)):
                    self.startLocation = [col*Width, row*Height]
                    locationFound = True
                    break
            if locationFound:
                self.startLocationSet = True
                break

    def setEnd(self,pos):
        locationFound = False
        for col in range(Columns):
            for row in range(Rows):
                if( abs(pos[0]-(col*Width)) < (Width*0.34) and abs(pos[1]-(row*Height)) < (Height*0.34)):
                    self.endLocation = [col*Width, row*Height]
                    locationFound = True
                    break
            if locationFound:
                self.endLocationSet = True
                break

    def setObstableLocations(self,pos):
        locationFound = False
        for col in range(Columns):
            for row in range(Rows):
                if( abs(pos[0]-(col*Width)) < (Width*0.34) and abs(pos[1]-(row*Height)) < (Height*0.34)):
                    if(not([col*Width, row*Height] in self.obstacleLocations)):
                        self.obstacleLocations.append([col*Width, row*Height])
                    locationFound = True
                    break
            if locationFound:
                break
        for val in self.obstacleLocations:
            print (val)
