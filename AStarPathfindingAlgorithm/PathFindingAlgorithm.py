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

    def runIter(self):
        #while not self.winCondition(path, self.endPoint):
        
        self.makePath(self.path, self.target, self.closedList, self.openList)
        #self.sortOpen(self.openList, self.endPoint)
        self.target = self.openList[-1]
        #self.getOptimalPath(self.path, target, self.closedList, self.openList)

        #print(self.closedList)
        #print(self.path)

        return self.path, self.closedList, self.openList, self.winCondition(self.path, self.endPoint)

    #def addToOpenList(self, path, closedList, openList, obstacleList):
    #    for x in [[1,0],[-1,0],[0,1],[0,-1]]:
    #        if(([x[0]+path[-1][0], x[1]+path[-1][1]] not in obstacleList) and ([x[0]+path[-1][0], x[1]+path[-1][1]] not in [point for point,length in closedList])):
    #            if((x[0]+path[-1][0] > -1) and (x[0]+path[-1][0] < 25) and (x[1]+path[-1][1] > -1) and (x[1]+path[-1][1] < 25)):
    #                if([x[0]+path[-1][0], x[1]+path[-1][1]] not in openList):
    #                    openList.append([x[0]+path[-1][0], x[1]+path[-1][1]])
                    
    
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
        closedList.append([options[-1],len(path)])
        if(options[-1] in openList):
            openList.remove(options[-1])
        options.pop()
        openList.extend(options)

    def makePath(self, path, point, closedList, openList):#, optimizeFunction = False, optimumPath = None, optimumClosedList = None, optimumOpenList = None):
        #if(not optimizeFunction):
            #newopenList = []
        while not self.winCondition(path, point):
            #self.addToOpenList(path, closedList, openList, self.obstaclePoints)
            self.addoptiontoPath(path, closedList, openList, self.sortOptions(self.addOptions(path, closedList, self.obstaclePoints), point))
            self.sortOpen(openList, self.endPoint)
                
                #print(closedList)
            #openList.extend(newopenList)
        #else:
        #    length = closedList[-1][1]
        #    print("Entering optimization loop")
        #    while not self.winCondition(path, point):
        #        self.addToOpenList(path, closedList, openList, self.obstaclePoints)
        #        self.sortOpen(openList, point)
        #        self.addoptiontoPath(path, closedList, openList, self.sortOptions(self.addOptions(path, closedList, openList, self.obstaclePoints), point))
        #        #self.addpointtoPath(path, openList[-1], closedList, openList)
        #        length += 1
        #        if(len(path) >= len(optimumPath)):
        #            break
        #    if((len(path)+length) < len(optimumPath)):
        #        print("Replacing path")
        #        print("Previoud path: ", optimumPath)
        #        optimumPath = path
        #        optimumClosedList = closedList
        #        optimumOpenList = openList
        #        print("New path: ", optimumPath)

            #return optimumPath, optimumClosedList, optimumOpenList

    def addpointtoPath(self, path, point, closedList, openList):
        path.append(point)
        closedList.append([point,(len(path))])
        openList.remove(point)

    def getOptimalPath(self, path, point, closedList, openList):
        #optimumPath = []
        optimumOpenList = []
        optimumClosedList = []
        for closedPoint, length in closedList:
            newpath = [closedPoint]
            newclosedList = [[closedPoint,length]]
            newopenList = []
            self.makePath(newpath, point, newclosedList, newopenList, True, path, optimumClosedList, optimumOpenList)

        print("New path outside func: ", path)
        print("New closed lsit:", optimumClosedList)
        self.resolveList(optimumClosedList, optimumOpenList, closedList, openList)

    def resolveList(self, optimumClosedList, optimumOpenList, closedList, openList):
        for point in optimumOpenList:
            if(point not in openList):
                openList.append(point)

        for point,length in optimumClosedList:
            if (point in openList):
                openList.remove(point)
            if(point not in closedList):
                closedList.append([point,length])
            else:
                closedList[[p for p,l in closedList].index(point)] = [point,length]


    def winCondition(self, path, goal):
        if(path[-1] == goal):
            return True

    def heuristic(self, point, goal):
        return (abs(point[0]-goal[0])+abs(point[1]-goal[1]))
