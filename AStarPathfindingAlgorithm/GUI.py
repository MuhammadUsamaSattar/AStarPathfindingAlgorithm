from PySide2 import QtWidgets, QtCore, QtGui
import pygame
from pygame.locals import *
from PySide2 import QtWidgets, QtGui, QtCore
import sys
from PathFindingAlgorithm import *
import pdb

WINDOW_WIDTH = 720  
WINDOW_HEIGHT = 840 
Width = int(WINDOW_WIDTH/(COLUMNS-1))
Height = int(WINDOW_HEIGHT/(ROWS-1))

class GUI():

    def __init__(self, iterative_visualization = True):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

        self.iterative_visualization = iterative_visualization
        self.running = True
        self.startLocationSet = False
        self.endLocationSet = False
        self.pathFound = False
        self.obstacleLocations = []
        self.path = []
        self.closedList = []
        self.openList = []
        self.infoDisplay()
        
        while self.running:
            self.eventHandler()

            self.screen.fill((0,0,0))

            if( self.iterative_visualization == True and self.pathFound and not self.won):
                print("Entering here")
                #pdb.set_trace()
                self.path,self.closedList,self.openList,self.won = self.algorithm.runIter()
                self.path = [[x*Width,y*Height] for x,y in self.path]
                self.closedList = [[p[0]*Width,p[1]*Height] for p,l,pp in self.closedList]
                self.openList = [[x*Width,y*Height] for x,y in self.openList]
                if self.won:
                    print("\n\nSolution found")
                    print("Path: ", [[x/Width,y/Height] for x,y in self.path],"\n\n")

            self.displayGrid()
            self.displayElements()

            pygame.display.flip()

        pygame.quit()


    def displayGrid(self):
        for col in range(COLUMNS):
            for row in range(ROWS):
                pygame.draw.circle(self.screen, (200,200,200), (col*Width,row*Height), int(Width/7.5))

        for col in range(COLUMNS):
            pygame.draw.line(self.screen,(200,200,200),(col*Width,0),(col*Width,WINDOW_HEIGHT))
        for row in range(ROWS):
            pygame.draw.line(self.screen,(200,200,200),(0,row*Height),(WINDOW_WIDTH,row*Height))

    def displayElements(self):
        prev_pos = (0,0)
        for i,pos in enumerate(self.obstacleLocations):
            pygame.draw.circle(self.screen, (165,42,42), [pos[0], pos[1]], int(Width/4))
        for i,pos in enumerate(self.obstacleLocations):
            if(i !=0 and (abs(pos[0]-prev_pos[0]) == Width or abs(pos[1]-prev_pos[1]) == Height) and abs(pos[0]-prev_pos[0]) <= Width and abs(pos[1]-prev_pos[1]) <= Height):
                pygame.draw.line(self.screen, (165,42,42),pos,prev_pos, int(Width/4)) 
            prev_pos = pos
        if(self.pathFound):       
            for i in range(len(self.closedList)):
                pygame.draw.circle(self.screen, (0,0,0), [int(self.closedList[i][0]), int(self.closedList[i][1])], int(Width/5))
            for i in range(len(self.openList)):
                pygame.draw.circle(self.screen, (0,0,255), [int(self.openList[i][0]), int(self.openList[i][1])], int(Width/5))
            for i in range(len(self.path)-1):
                pygame.draw.line(self.screen, (0,255,0),[self.path[i][0],self.path[i][1]],[self.path[i+1][0],self.path[i+1][1]], 4) 
        if (self.startLocationSet):
            pygame.draw.circle(self.screen, (0,255,0), self.startLocation, int(Width/5))
        if (self.endLocationSet):
            pygame.draw.circle(self.screen, (255,0,0), self.endLocation, int(Width/5))

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
                    self.algorithm = pathFinder([self.startLocation[0]/Width,self.startLocation[1]/Height], [self.endLocation[0]/Width,self.endLocation[1]/Height], [[x/Width,y/Height] for x,y in self.obstacleLocations])
                    #pdb.set_trace()
                    if(self.iterative_visualization == True):
                        self.path,self.closedList,self.openList,self.won = self.algorithm.firstIter()
                        if self.won:
                            print(self.closedList)
                            self.path = [[x*Width,y*Height] for x,y in self.path]
                            self.closedList = [[p[0]*Width,p[1]*Height] for p,l,pp in self.closedList]
                            self.openList = [[x*Width,y*Height] for x,y in self.openList]
                            print("\n\nSolutionm found")
                            print("Path: ", [[x/Width,y/Height] for x,y in self.path],"\n\n")
                            print(self.closedList)
                    else:
                        self.path,self.closedList,self.openList,self.won = self.algorithm.run()
                        if self.won:
                            print("\n\nSolution found")
                            print("Path: ", [[x/Width,y/Height] for x,y in self.path],"\n\n")
                            self.path = [[x*Width,y*Height] for x,y in self.path]
                            self.closedList = [[p[0]*Width,p[1]*Height] for p,l,pp in self.closedList]
                            self.openList = [[x*Width,y*Height] for x,y in self.openList]
                    self.pathFound = True
                    self.displayElements()

            elif event.type == pygame.QUIT:
                self.running = False

    def setStart(self,pos):
        locationFound = False
        for col in range(COLUMNS):
            for row in range(ROWS):
                if( abs(pos[0]-(col*Width)) < (Width*0.34) and abs(pos[1]-(row*Height)) < (Height*0.34)):
                    self.startLocation = [col*Width, row*Height]
                    locationFound = True
                    break
            if locationFound:
                self.startLocationSet = True
                break

    def setEnd(self,pos):
            locationFound = False
            for col in range(COLUMNS):
                for row in range(ROWS):
                    if( abs(pos[0]-(col*Width)) < (Width*0.34) and abs(pos[1]-(row*Height)) < (Height*0.34) and [col*Width,row*Height] != self.startLocation):
                        self.endLocation = [col*Width, row*Height]
                        locationFound = True
                        break
                if locationFound:
                    self.endLocationSet = True
                    break

    def setObstableLocations(self,pos):
        if (pos != self.startLocation and pos != self.endLocation):
            locationFound = False
            for col in range(COLUMNS):
                for row in range(ROWS):
                    if( abs(pos[0]-(col*Width)) < (Width*0.34) and abs(pos[1]-(row*Height)) < (Height*0.34) and [col*Width,row*Height] != self.startLocation and [col*Width,row*Height] != self.endLocation):
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
        self.text.setText("""Click on a vetex to select the start point.\nThen, click on a vertex to select the end point.\nThen, hold left mouse button to draw the obstacles.\n\nPress \'R\' key to reset the software.\nPress \'G\' key to start the software.\n""")
        self.text.resize(self.text.minimumSizeHint())