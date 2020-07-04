from PySide2 import QtWidgets, QtCore, QtGui
import pygame
from pygame.locals import *
from PySide2 import QtWidgets, QtGui, QtCore
import sys
from PathFindingAlgorithm import *
import pdb

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
        
        self.running = True
        self.startLocationSet = False
        self.endLocationSet = False
        self.pathFound = False
        self.obstacleLocations = []
        self.path = []
        self.infoDisplay()

        while self.running:
            self.eventHandler()

            self.screen.fill((0,0,0))

            self.displayGrid()
            self.displayElements()

            if(self.pathFound and not self.won):
                pdb.set_trace()
                self.path,self.won = self.algorithm.run()
                self.path = [[x*30,y*35] for x,y in self.path]

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

    def displayElements(self):
        if (self.startLocationSet):
            pygame.draw.circle(self.screen, (0,255,0), self.startLocation, int(Width/5))
        if (self.endLocationSet):
            pygame.draw.circle(self.screen, (255,0,0), self.endLocation, int(Width/5))
        prev_pos = (0,0)
        for i,pos in enumerate(self.obstacleLocations):
            if(i !=0 and (abs(pos[0]-prev_pos[0]) == Width or abs(pos[1]-prev_pos[1]) == Height) and abs(pos[0]-prev_pos[0]) <= Width and abs(pos[1]-prev_pos[1]) <= Height):
                pygame.draw.line(self.screen, (165,42,42),pos,prev_pos, 8) 
            prev_pos = pos
        if(self.pathFound):
            for i in range(len(self.path)-1):
                pygame.draw.line(self.screen, (0,255,0),[self.path[i][0],self.path[i][1]],[self.path[i+1][0],self.path[i+1][1]], 4) 

    def eventHandler(self):
        for event in pygame.event.get():
            if pygame.mouse.get_pressed() == (1,0,0):
                if(self.startLocationSet != True):
                    self.setStart(pygame.mouse.get_pos())
                elif(self.endLocationSet != True):
                    self.setEnd(pygame.mouse.get_pos())
                else:
                    self.setObstableLocations(pygame.mouse.get_pos())

            elif(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_r ):
                    self.startLocationSet = False
                    self.endLocationSet = False
                    self.obstacleLocations=[]
                    self.pathFound = False
                    self.path = []
                elif(event.key == pygame.K_g ):
                    self.algorithm = pathFinder([self.startLocation[0]/30,self.startLocation[1]/35], [self.endLocation[0]/30,self.endLocation[1]/35], [[x/30,y/35] for x,y in self.obstacleLocations])
                    self.path,self.won = self.algorithm.run()
                    self.path = [[x*30,y*35] for x,y in self.path]
                    self.pathFound = True

            elif event.type == pygame.QUIT:
                self.running = False

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


    def infoDisplay(self):
        app = QtWidgets.QApplication(sys.argv)
        self.infoWindow = QtWidgets.QWidget()
        self.infoWindow.setGeometry(200,200,200,200)
        self.infoWindow.setWindowTitle("Info")
        self.infoWindow.setWindowIcon( QtGui.QIcon(r"resources/Icons/help.png")) 
        self.okButton()
        self.infoText()
        layout = QtWidgets.QVBoxLayout(self.infoWindow)
        layout.addWidget(self.text)
        layout.addWidget(self.btn)
        self.infoWindow.show()
        app.exec_()

    def okButton(self):
        self.btn = QtWidgets.QPushButton(self.infoWindow)
        self.btn.setText("Ok")
        self.btn.resize(self.btn.minimumSizeHint())
        self.btn.clicked.connect(self.infoWindow.close)

    def infoText(self):
        self.text = QtWidgets.QLabel(parent = self.infoWindow)
        self.text.setWordWrap(True)
        self.text.setText("""Click on a vetex to select the start point.\nThen, click on a vertex to select the end point.\nThen, hold left mouse button to draw the obstacles.\n\nPress \'R\' key to reset the software.\n""")
        self.text.resize(self.text.minimumSizeHint())