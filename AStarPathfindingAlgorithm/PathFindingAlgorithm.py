import pdb

class pathFinder():
    def __init__(self, startPoint, endPoint, obstaclePoints):
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.obstaclePoints = obstaclePoints

        self.won = False

        self.openList = []
        self.closedList = [[self.startPoint,1]]
        self.path = [self.startPoint]
        self.target = self.endPoint
        
        print("Target: ", self.target)
        print("Closed list:", self.closedList)
        print("Open list:", self.openList,"\n\n")
        self.addToOpen(self.openList, self.sortOptions(self.addOptions(self.path, self.closedList, self.obstaclePoints), self.endPoint))
        self.sortOpen(self.openList, self.endPoint)
        self.addoptiontoPath(self.path, self.closedList, self.openList, self.sortOptions(self.addOptions(self.path, self.closedList, self.obstaclePoints), self.endPoint))
        print("Path: ", self.path)

    def runIter(self):
        #while not self.winCondition(path, self.endPoint):
        #try:
        self.addToOpen(self.openList, self.sortOptions(self.addOptions(self.path, self.closedList, self.obstaclePoints), self.endPoint))
        self.sortOpen(self.openList, self.endPoint)
        self.target = self.openList[-1]
        print("Target: ", self.target)
        print("Closed list:", self.closedList)
        print("Open list:", self.openList)
        self.path = self.makePath(self.path, self.target, self.closedList, self.openList)
        self.path, self.closedList, self.openList = self.getOptimalPath(self.path, self.target, self.closedList, self.openList)
        print("Path: ", self.path)
        #print("Open list after:", self.openList)
        #self.removeDuplicates(self.closedList, self.openList)
        #print("Open after clean: ", self.openList)
        #print(self.path)

        #except Exception as e:
        #    print(e)

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
        for x in [[1,0],[-1,0],[0,1],[0,-1]]:
            if(([x[0]+path[-1][0], x[1]+path[-1][1]] not in obstacleList) and ([x[0]+path[-1][0], x[1]+path[-1][1]] not in [point for point,length in closedList])):
                if((x[0]+path[-1][0] > -1) and (x[0]+path[-1][0] < 25) and (x[1]+path[-1][1] > -1) and (x[1]+path[-1][1] < 25)):
                        options.append([x[0]+path[-1][0], x[1]+path[-1][1]])
        return options

    def sortOptions(self, options, goal):
        for count in range(len(options)-1):
            for i in range(len(options)-1-count):
                if(self.heuristic(options[i], goal) < self.heuristic(options[i+1], goal)):
                    temp = options[i+1]
                    options[i+1] = options[i]
                    options[i] = temp
        return options

    def addoptiontoPath(self, path, closedList, openList, options):
        path.append(options[-1])
        if(options[-1] not in [p for p,l in closedList]):
            closedList.append([options[-1],(closedList[-1][1]+1)])
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

    def getOptimalPath(self, path, point, closedList, openList):
        optimumPath = path
        optimumClosedList = []
        optimumOpenList = []
        newpath = []
        newOpenList = []
        newClosedList = []
        for closedPoint, length in closedList:
            newpath = [closedPoint]
            newclosedList = [[closedPoint,length]]
            newopenList = []
            newpath = self.makePath(newpath, point, newclosedList, newopenList)
            if ((newclosedList[-1][1] < len(optimumPath) or not optimumPath) and newpath):
                optimumPath = newpath
                optimumClosedList = newclosedList
                optimumOpenList = newopenList

        #newpath = []
        #if(optimumPath[0] != self.startPoint):
        #    newpath = [self.startPoint]
        #    newclosedList = [[[self.startPoint],1]]
        #    newopenList = []
        #    newpath2 = []
        #    
        #    if(path.index(optimumPath[0])):
        #        if(path):
        #            newpath2 = path[:path.index(optimumPath[0])]
        #
        #    newpath = self.makePath(newpath, optimumPath[0], newclosedList, newopenList)
        #    print("Newpath: ", newpath)
        #    newpath.pop()
        #
        #    if(len(newpath) <= len(newpath2) or not newpath2):
        #        self.resolveList(newclosedList, newopenList, closedList, openList)
        #    else:
        #        newpath = newpath2
        #
        #print("Optimal path: ", optimumPath)
        #
        #if(newpath):
        #    path = newpath.extend(optimumPath)
        #else:
        #    path = optimumPath
        path = optimumPath
        #print("Path inside is: ", path)
        #print("Optimal open list:", optimumOpenList)
        #print("Open list inside before: ", openList)
        self.resolveList(optimumClosedList, optimumOpenList, closedList, openList)
        #print("Open list inside after: ", openList)

        return path, closedList, openList

    def resolveList(self, optimumClosedList, optimumOpenList, closedList, openList):
        for point in optimumOpenList:
            if((point not in openList) and (point not in [p for p,l in closedList]) and (point not in [p for p,l in optimumClosedList])):
                openList.append(point)

        for point,length in optimumClosedList:
            if(point not in [p for p,l in closedList]):
                closedList.append([point,length])
            else:
                closedList[[p for p,l in closedList].index(point)] = [point,length]

        for point,length in closedList:
            if(point in openList):
                openList.remove(point) 

    def winCondition(self, path, goal):
        if(path[-1] == goal):
            return True

    def heuristic(self, point, goal):
        return (abs(point[0]-goal[0])+abs(point[1]-goal[1]))

    def removeDuplicates(self, closedList, openList):
        for i in range(len(openList)-1):
            for k in range(len(openList)-1-i):
                if(openList[i] == openList[i+k+1]):
                    openList.pop(i+k+1)

        for point,length in closedList:
            for i in range(len(openList)):
                if(point == openList[i]):
                    openList.pop(i)