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
        self.addToOpen(self.openList, self.sortOptions(self.addOptions(self.path, self.closedList, self.obstaclePoints), self.endPoint))
        self.sortOpen(self.openList, self.endPoint)
        self.addoptiontoPath(self.path, self.closedList, self.openList, self.sortOptions(self.addOptions(self.path, self.closedList, self.obstaclePoints), self.endPoint))
        print("Path: ", self.path)
        print("Closed list:", self.closedList)
        print("Open list:", self.openList,"\n\n")

        #return self.path, self.closedList, self.openList, self.winCondition(self.path, self.endPoint)
        

    def runIter(self):
        #while not self.winCondition(path, self.endPoint):
        try:
            self.addToOpen(self.openList, self.sortOptions(self.addOptions(self.path, self.closedList, self.obstaclePoints), self.endPoint))
            self.sortOpen(self.openList, self.endPoint)
            self.target = self.openList[-1]
            print("Target: ", self.target)
            self.path = self.makePath(self.path, self.target, self.closedList, self.openList)
            self.path, self.closedList, self.openList = self.getOptimalPath(self.path, self.target, self.closedList, self.openList)
            print("Path: ", self.path)
            print("Closed list:", self.closedList)
            print("Open list:", self.openList)
            self.removeDuplicates(self.closedList, self.openList)
            print("Open after clean: ", self.openList)
            print(self.path)

        #self.addToOpen(self.openList, self.sortOptions(self.addOptions(self.path, self.closedList, self.obstaclePoints), self.endPoint))
        #self.sortOpen(self.openList, self.endPoint)
        #self.target = self.openList[-1]
        #print("Target: ", self.target)
        #self.path = self.makePath(self.path, self.target, self.closedList, self.openList)
        #print("Open list after 1 is:", self.openList)
        #self.path, self.closedList, self.openList = self.getOptimalPath(self.path, self.target, self.closedList, self.openList)
        #print("Open list after 2 is:", self.openList)
        ##print("Closed list:", self.closedList)
        #print("Open list:", self.openList)
        #print("Path: ", self.path, "\n\n")
        ##print("New path outside: ", self.path)
        ##self.sortOpen(self.openList, self.endPoint)
        ##print("Outside closed list:", self.closedList)
        ##print("Outside open list:", self.openList)
        ##self.getOptimalPath(self.path, target, self.closedList, self.openList)

        #print(self.closedList)
        #print(self.path)

        except Exception as e:
            print(e)

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
        #openList.extend(options)

    def makePath(self, path, point, closedList, openList):#, optimizeFunction = False, optimumPath = None, optimumClosedList = None, optimumOpenList = None):
        #if(not optimizeFunction):
            #newopenList = []
            while not self.winCondition(path, point):
                options = self.sortOptions(self.addOptions(path, closedList, self.obstaclePoints), point)
                #self.addToOpenList(path, closedList, openList, self.obstaclePoints)
                if(options):
                    self.addoptiontoPath(path, closedList, openList, options)
                    self.addToOpen(openList, self.sortOptions(self.addOptions(path, closedList, self.obstaclePoints), self.endPoint))
                else:
                    path = []
                    break
            return path
            #self.sortOpen(openList, self.endPoint)
            #print("Inside closed list:", closedList)
            #print("Inside open list:", openList)
                
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

    #def addpointtoPath(self, path, point, closedList, openList):
    #    path.append(point)
    #    closedList.append([point,(len(path))])
    #    openList.remove(point)

    def getOptimalPath(self, path, point, closedList, openList):
        #print("Old path: ", path)
        #optimumPath = []
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
            #print("Path closed list: ", newclosedList)
            #print("Optimum path:", optimumPath)
            if ((newclosedList[-1][1] < len(optimumPath) or not optimumPath) and newpath):
                #print("Replcaing with a new path")
                optimumPath = newpath
                optimumClosedList = newclosedList
                optimumOpenList = newopenList

        path = optimumPath
        print("Optimal open list:", optimumOpenList)
        print("Open list inside before: ", openList)
        self.resolveList(optimumClosedList, optimumOpenList, closedList, openList)
        print("Open list inside after: ", openList)

        return path, closedList, openList

        #print("New path outside func: ", path)
        #print("New closed lsit:", optimumClosedList)
        #self.resolveList(optimumClosedList, optimumOpenList, closedList, openList)

    def resolveList(self, optimumClosedList, optimumOpenList, closedList, openList):
        for point in optimumOpenList:
            if((point not in openList) and (point not in [p for p,l in closedList]) and (point not in [p for p,l in optimumClosedList])):
                openList.append(point)

        for point,length in optimumClosedList:
            #if (point in openList):
            #    openList.remove(point)
            if(point not in [p for p,l in closedList]):
                closedList.append([point,length])
            else:
                closedList[[p for p,l in closedList].index(point)] = [point,length]


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