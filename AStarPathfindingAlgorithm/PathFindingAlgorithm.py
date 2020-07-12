import math

COLUMNS = 49
ROWS = 49

class pathFinder():
    def __init__(self, startPoint, endPoint, obstaclePoints):
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.obstaclePoints = obstaclePoints

        self.won = False

        self.openList = []
        self.closedList = [[self.startPoint,1,[self.startPoint]]]
        self.path = [self.startPoint]
        self.target = self.endPoint
        
        self.addToOpen(self.openList, self.sortOptions(self.addOptions(self.path, self.closedList, self.obstaclePoints), self.endPoint))
        self.sortOpen(self.openList, self.endPoint)
        self.addoptiontoPath(self.path, self.closedList, self.openList, self.sortOptions(self.addOptions(self.path, self.closedList, self.obstaclePoints), self.endPoint))
        print("Path: ", self.path,"\n\n")

    def run(self):
        while not self.winCondition(self.path, self.endPoint):
            self.addToOpen(self.openList, self.sortOptions(self.addOptions(self.path, self.closedList, self.obstaclePoints), self.endPoint))
            self.sortOpen(self.openList, self.endPoint)
            self.target = self.openList[-1]
            self.path = []
            self.path, self.closedList, self.openList = self.getOptimalPath(self.path, self.target, self.closedList, self.openList)
            print("Path: ", self.path,"\n\n")

        return self.path, self.closedList, self.openList, self.winCondition(self.path, self.endPoint)

    def runIter(self):
        self.addToOpen(self.openList, self.sortOptions(self.addOptions(self.path, self.closedList, self.obstaclePoints), self.endPoint))
        self.sortOpen(self.openList, self.endPoint)
        self.target = self.openList[-1]
        self.path = []
        self.path, self.closedList, self.openList = self.getOptimalPath(self.path, self.target, self.closedList, self.openList)
        print("Path: ", self.path,"\n\n")

        return self.path, self.closedList, self.openList, self.winCondition(self.path, self.endPoint)

    def addToOpen(self, openList, options):
        for option in options:
            if(option not in openList):
                openList.append(option)
                    
    def sortOpen(self, openList, goal):
        for count in range(len(openList)-1):
            for i in range(len(openList)-1-count):
                if(self.heuristic(openList[i], goal) < self.heuristic(openList[i+1], goal)):
                    temp = openList[i+1]
                    openList[i+1] = openList[i]
                    openList[i] = temp

    def addOptions(self, path, closedList, obstacleList):
        options = []
        for x in [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]]:
            if(([x[0]+path[-1][0], x[1]+path[-1][1]] not in obstacleList) and ([x[0]+path[-1][0], x[1]+path[-1][1]] not in [point for point,length,prevpath in closedList])):
                if((x[0]+path[-1][0] > -1) and (x[0]+path[-1][0] < COLUMNS) and (x[1]+path[-1][1] > -1) and (x[1]+path[-1][1] < ROWS) and (([x[0]+path[-1][0],path[-1][1]] not in obstacleList) or ([path[-1][0],x[1]+path[-1][1]] not in obstacleList))):
                        options.append([x[0]+path[-1][0], x[1]+path[-1][1]])
        return options

    def sortOptions(self, options, goal):
        for count in range(len(options)-1):
            for i in range(len(options)-1-count):
                if(self.heuristic(options[i], goal) <= self.heuristic(options[i+1], goal)):
                    temp = options[i+1]
                    options[i+1] = options[i]
                    options[i] = temp
        return options

    def addoptiontoPath(self, path, closedList, openList, options):
        path.append(options[-1])
        if(options[-1] not in [p for p,l,prevpath in closedList]):
            prev = closedList[[p2 for p2,l2,pp22 in closedList].index(path[-2])][2][:]
            prev.append(options[-1])
            closedList.append([options[-1],(closedList[[p2 for p2,l2,pp22 in closedList].index(path[-2])][1]+1),prev])
        if(options[-1] in openList):
            openList.remove(options[-1])
        options.pop()

    def makePath(self, path, point, closedList, openList):
            while not self.winCondition(path, point):
                options = self.sortOptions(self.addOptions(path, closedList, self.obstaclePoints), point)
                if(options):
                    self.addoptiontoPath(path, closedList, openList, options)
                    self.addToOpen(openList, self.sortOptions(self.addOptions(path, closedList, self.obstaclePoints), self.endPoint))
                else:
                    path = []
                    break
            return path

    def getOptimalPath(self, path, point, closedList, openList, mode = 'Primary'):
        optimumPath = path
        optimumClosedList = closedList
        optimumOpenList = []
        newpath = []
        newOpenList = []
        newClosedList = []
        for closedPoint, length,prevpath in closedList:
            newpath = [closedPoint]
            newclosedList = [[closedPoint,length,prevpath]]
            newopenList = []
            newpath = self.makePath(newpath, point, newclosedList, newopenList)
            if (((self.cost(optimumClosedList[-1][2]) > self.cost(newclosedList[-1][2])) or not optimumPath) and newpath):
                optimumPath = newpath
                optimumClosedList = newclosedList
                optimumOpenList = newopenList
        
        if(optimumPath[0] != self.startPoint and mode == 'Primary'):
            path = optimumClosedList[0][2][:]
            path.pop()
            path.extend(optimumPath)
        else:
            path = optimumPath
        
        self.resolveList(optimumClosedList, optimumOpenList, closedList, openList)
        
        return path, closedList, openList

    def resolveList(self, optimumClosedList, optimumOpenList, closedList, openList):
        for point in optimumOpenList:
            if((point not in openList) and (point not in [p for p,l,prevpath in closedList]) and (point not in [p for p,l,prevpath in optimumClosedList])):
                openList.append(point)

        for point,length,prevpath in optimumClosedList:
            if(point not in [p for p,l,pp in closedList]):
                closedList.append([point,length,prevpath])
            else:
                if( length <= closedList[[p for p,l,pp in closedList].index(point)][1]):
                    closedList.pop([p for p,l,pp in closedList].index(point))
                    closedList.append([point,length,prevpath])

        for point,length,prevpath in closedList:
            if(point in openList):
                openList.remove(point) 

    def winCondition(self, path, goal):
        if(path[-1] == goal):
            return True

    def heuristic(self, point, goal):
        return math.sqrt(((point[0]-goal[0])*(point[0]-goal[0]))+((point[1]-goal[1])*(point[1]-goal[1])))

    def cost(self, path):
        diag =0
        straight = 0 
        for i in range(len(path)-1):
            if((abs(path[i][0]-path[i+1][0])+abs(path[i][1]-path[i+1][1])) == 1):
                straight += 1
            else:
                diag += 1
        total = straight + math.sqrt(2) * diag
        return total