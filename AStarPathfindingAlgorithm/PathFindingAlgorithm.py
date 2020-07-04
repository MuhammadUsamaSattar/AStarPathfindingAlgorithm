import pdb

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
            #pdb.set_trace()
            self.addPointToPath(self.path, self.closedList, self.openList, self.sortOptions(self.addOptions(self.path, self.closedList)))
            self.loseCondition()
            self.optimizePath()
            if(not(self.winCondition(self.path, self.endPoint))):    print("\n\nPath is: ",self.path, "\n\n")
#                    pathFinder.lengthverified += 1
#                    if(len(self.path) > pathFinder.lengthverified):
#                        if(not(self.verifyPath(self.path))):
#                            self.switchPath()
#                            pathFinder.lengthverified -= 1
            
            #print(self.path)
        except Exception as e:
            print(e)

        return self.path, self.winCondition(self.path, self.endPoint)

    def optimizePath(self):
        #print("Entering optimzation")
        optimumNeighbour = []
        optimumOpenList = []
        optimumClosedList = []
        for i,start in enumerate(self.closedList):
            neighbour = [start[0]]
            newclosedList = [start[0]]
            newopenList = []
            length = start[1]
            while not self.winCondition(neighbour,self.path[-1]):
                self.addPointToPath(neighbour, newclosedList, newopenList, self.sortOptions(self.addOptions(neighbour, newclosedList)))
                length += 1
                #print("Neighour is: ",neighbour,"\nwith length: ",length)
                if(length >= len(self.path)):
                    break
            if(length < len(optimumNeighbour) or not optimumNeighbour):
                print("Found an optimum path")
                optimumNeighbour = neighbour
                optimumClosedList = newclosedList
                optimumOpenList = newopenList
        #print("Exiting optimzation")
        print("Optimum neighour length",len(optimumNeighbour),"     Path Length",len(self.path))
        if(len(optimumNeighbour) < len(self.path) and optimumNeighbour):
            print("Found a replaceable optimum path")
            self.path = optimumNeighbour
            for point in optimumClosedList:
                index = [p for p,l in self.closedList].index(point[0])
                if(index):
                    self.closedList[index] = point
                else:
                    self.closedList.append(point)
            for point in optimumOpenList:
                if((point not in self.openList) and (point not in [p for p,l in self.closedList])):
                    self.openList.append(point)
            #for point in self.openList:
            #    if (point in self.closedList):
            #        self.openList.remove(point)

#    def findPath(self):


    def addOptions(self, path, closedList):
        options = []
        for x in [[1,0],[-1,0],[0,1],[0,-1]]:
            if(([x[0]+path[-1][0],x[1]+path[-1][1]] not in self.obstaclePoints) and ([x[0]+path[-1][0],x[1]+path[-1][1]] not in [point for point,length in closedList]) and ([x[0]+path[-1][0],x[1]+path[-1][1]] != self.startPoint)):
                if((x[0]+path[-1][0]) > -1 and (x[0]+path[-1][0])<25 and (x[1]+path[-1][1]) > -1 and (x[1]+path[-1][1]) < 25):
                    options.append([x[0]+path[-1][0],x[1]+path[-1][1]])
        #print("Unsorted options", options)
        if (not options):
            if (len(path)!= 1):
                path.pop()
                return self.addOptions(path, self.closedList)
            else:
               self.loseCondition()
        return options

    def sortOptions(self, options):
        options.append([1000,1000])
        for count in range(len(options)-2):
            for i in range(len(options)-2-count):
                if(self.heuristics(options[i+1]) > self.heuristics(options[i])):
                    options[-1] = options[i+1]
                    options[i+1] = options[i]
                    options[i] = options[-1]
                    options[-1] = [1000,1000]
        options.pop()
        #print("Sorted options", options)
        return options   
    
    def addPointToPath(self, path,closedList,openList, options):
        #print("Options are: ",options)
        path.append(options[-1])
        #print(closedList)
        closedList.append([options[-1],(closedList[len(closedList)-1][1]+1)])
        #print(closedList)
        options.pop()
        openList.append(options)

    def heuristics(self,point):
        return (abs(point[0]-self.endPoint[0])+abs(point[1]-self.endPoint[1]))

    def winCondition(self,path ,point):
        if(path[-1] == point):
            return True

    def loseCondition(self):
        if(not self.openList):
            print("No solution possible")
            exit()