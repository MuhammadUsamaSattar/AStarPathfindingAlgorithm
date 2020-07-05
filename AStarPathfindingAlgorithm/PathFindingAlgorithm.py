class pathFinder():
    lengthverified = 1

    def __init__(self, startPoint, endPoint, obstaclePoints):
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.obstaclePoints = obstaclePoints

        self.won = False

        self.openList = []
        self.closedList = [[self.startPoint,1]]
        self.path = [self.startPoint]

    def run(self):
        try:
        #if (not self.winCondition(self.path, self.endPoint)):
            self.addPointToPath(self.path, self.closedList, self.openList, self.sortOptions(self.addOptions(self.path, self.closedList),self.endPoint))
            #self.loseCondition()
            self.path,self.closedList,self.openList = self.optimizePath(self.path, self.closedList, self.openList)
            #print(self.path)
            if(not(self.winCondition(self.path, self.endPoint))):
                print("\n\nPath is: ",self.path)
                print("\nClosed List: ", self.closedList)
                print("\nOpen List: ", self.openList, "\n\n")
                 #pathFinder.lengthverified += 1
                 #if(len(self.path) > pathFinder.lengthverified):
                 #    if(not(self.verifyPath(self.path))):
                 #        self.switchPath()
                 #        pathFinder.lengthverified -= 1
            
            #print(self.path)
        except Exception as e:
            print(e)

        return self.path, self.closedList , self.openList,self.winCondition(self.path, self.endPoint)

    def optimizePath(self, path, closedList,openList):
        #print("Entering optimzation")
        optimumNeighbour = []
        optimumOpenList = []
        optimumClosedList = []
        for i,start in enumerate(closedList):
            neighbour = [start[0]]
            newclosedList = [start]
            newopenList = []
            length = int(start[1])
            while not self.winCondition(neighbour,path[-1]):
                self.addPointToPath(neighbour, newclosedList, newopenList, self.sortOptions(self.addOptions(neighbour, newclosedList),path[-1]))
                length += 1
                #print("Neighour is: ",neighbour,"\nwith length: ",length)
                if(length >= len(path)):
                    break
            #print("Current optimum neighbour is:" ,neighbour)
            if((length < len(optimumNeighbour)) or not (optimumNeighbour)):
                #print("Found an optimum path")
                optimumNeighbour = neighbour
                optimumClosedList = newclosedList
                optimumOpenList = newopenList

        #print("Exiting optimzation")
        #print("Optimum neighour length",len(optimumNeighbour),"     Path Length",len(path))
        print("Old path :", path)
        #print("Optimal neighbour", optimumNeighbour)
        if((len(optimumNeighbour) < len(path)) and (optimumNeighbour)):
            print("Optimum poath parital is: ", optimumNeighbour)
            #print("Open list before: ", openList)
            if(optimumNeighbour[0] != self.startPoint and optimumNeighbour):
                #path = [optimumNeighbour[0]]
                print("Path should be replaced now")
                pathCopy = []
                if (path.index(optimumNeighbour[0])):
                    pathCopy = path[:(path.index(optimumNeighbour[0]))]
                    #print("Adding path to path", path)
                    
                newclosedList = [[self.startPoint,1]]
                newopenList = []
                path = [self.startPoint]
                while not self.winCondition(path, optimumNeighbour[0]):
                    self.addPointToPath(path, newclosedList, newopenList, self.sortOptions(self.addOptions(path, newclosedList),optimumNeighbour[0]))
                self.rebuildLists(closedList, openList, newclosedList, newopenList)
                path.pop()
                if(pathCopy):
                    path = min(pathCopy,path)
                print("Optimum full is",path)
                #print("Adding point to path", path)
                #print(path)
            else:
                path =[]

            path.extend(optimumNeighbour)
            print("New path: ", path)
            #print("Open list after: ", openList)
            self.rebuildLists(closedList, openList, optimumClosedList, optimumOpenList)

            
        return path, closedList, openList

    def addOptions(self, path, closedList):
        options = []
        for x in [[1,0],[-1,0],[0,1],[0,-1]]:
            if(([x[0]+path[-1][0],x[1]+path[-1][1]] not in self.obstaclePoints) and ([x[0]+path[-1][0],x[1]+path[-1][1]] not in [point for point,length in closedList]) and ([x[0]+path[-1][0],x[1]+path[-1][1]] != self.startPoint)):
                if(((x[0]+path[-1][0]) > -1) and ((x[0]+path[-1][0])<25) and ((x[1]+path[-1][1]) > -1) and ((x[1]+path[-1][1]) < 25)):
                    options.append([x[0]+path[-1][0],x[1]+path[-1][1]])
        #print("Unsorted options", options)
        if (not options):
            if (len(path)!= 1):
                path.pop()
                return self.addOptions(path, self.closedList)
            else:
               self.loseCondition()
        return options

    def sortOptions(self, options, goal):
        options.append([1000,1000])
        for count in range(len(options)-2):
            for i in range(len(options)-2-count):
                if(self.heuristics(options[i+1],goal) > self.heuristics(options[i],goal)):
                    options[-1] = options[i+1]
                    options[i+1] = options[i]
                    options[i] = options[-1]
                    options[-1] = [1000,1000]
        options.pop()
        print("Sorted options", options)
        return options   
    
    def addPointToPath(self, path,closedList,openList, options):
        print("Options are: ",options)
        path.append(options[-1])
        print(closedList)
        closedList.append([options[-1],(closedList[len(closedList)-1][1]+1)])
        print(closedList)
        options.pop()
        openList.extend(options)

    def rebuildLists(self, closedList, openList, newclosedList, newopenList):
        for point in newclosedList:
            if([p for p,l in closedList].index(point[0])):
                closedList[[p for p,l in closedList].index(point[0])] = point
            else:
                closedList.append(point)
            if(point[0] in openList):
                openList.remove(point[0])
        for point in newopenList:
            if((point not in openList) and (point not in [p for p,l in closedList])):
                openList.append(point[0])

    def heuristics(self,point,goal):
        return (abs(point[0]-goal[0])+abs(point[1]-goal[1]))

    def winCondition(self,path ,point):
        #if(path):
        if(path[-1] == point):
            return True

    def loseCondition(self):
        if(not self.openList):
            print("No solution possible")
            exit()