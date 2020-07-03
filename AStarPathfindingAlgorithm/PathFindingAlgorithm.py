import pdb

class pathFinder():
    def __init__(self, startPoint, endPoint, obstaclePoints):
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.obstaclePoints = obstaclePoints

        self.won = False

        self.openList = []
        self.closedList = [self.startPoint]
        self.path = [self.startPoint]

    def run(self):
        #try:
        while not self.won:
            #pdb.set_trace()
            self.addPointToPath(self.sortOptions(self.addOptions()))
            print(self.path)
            self.winCondition()
            self.loseCondition()
            if(len(self.path) != 2):
                if(not(self.verifyPath(self.path))):
                    self.switchPath()
        
        #print(self.path)
        return self.path
        #except Exception as e:
        #    print(e)

    def addOptions(self):
        options = []
        for x in [[1,0],[-1,0],[0,1],[0,-1]]:
            if(([x[0]+self.path[-1][0],x[1]+self.path[-1][1]] not in self.obstaclePoints) and ([x[0]+self.path[-1][0],x[1]+self.path[-1][1]] not in self.closedList)):
                options.append([x[0]+self.path[-1][0],x[1]+self.path[-1][1]])
        #print("Unsorted options", options)
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
    
    def addPointToPath(self, options):
        self.path.append(options[-1])
        self.closedList.append(options[-1])
        options.pop()
        self.openList.append(options)

    def verifyPath(self, path):
        self.neighbour = pathFinder(self.startPoint, path[-1], self.obstaclePoints,)
        if(len(self.path) < len(self.neighbour.run())):
            return True
        else:
            return False

    def switchPath(self):
        self.path = self.neighbour

    def heuristics(self,point):
        return (abs(point[0]-self.endPoint[0])+abs(point[1]-self.endPoint[1]))

    def winCondition(self):
        if(self.path[-1] == self.endPoint):
            self.won = True

    def loseCondition(self):
        if(not self.openList):
            print("No solution possible")
            exit()