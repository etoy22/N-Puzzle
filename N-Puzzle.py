from math import sqrt
from copy import deepcopy
from queue import PriorityQueue
import time

textFile="testing/4x4.txt"

class n_puzzle():
    '''
    The N-Puzzle Class
    '''
    state = []
    length = 0
    movePosX = None
    movePosY = None
    parent = None
    goalState = None


    def __lt__(self, other):
        return self.heuristicsValue < other.heuristicsValue
    
    def findPos(self,value):
        '''
        Find the starting points empty cell
        '''
        for i in range (self.length):
            if value in self.state[i]:
                for j in range (self.length):
                    if self.state[i][j] == value:
                        return i,j

        return 0,0

    def heuristics(self):
        '''
        This will be done using Euclidian Distance
        '''
        distance = 0
        for i in range(self.length):
            for j in range (self.length):
                value = self.state[i][j]
                if value != 0:
                    xPos = value //self.length
                    yPos = (value)%self.length
                    xCalc = (xPos-i)**2
                    yCalc = (yPos-j)**2
                    calc = sqrt(xCalc+yCalc)
                    distance += calc
        return round(distance)

    def __init__(self,state,movePosX=None,movePosY=None,parent=None):
        self.state = state
        self.parent = parent
        self.length = len(state)
        self.movePosX = movePosX
        self.movePosY = movePosY
        # self.goalState = goalState

        # Initalize Goal State if its the first time being run 
        # if (self.goalState == None):
        #     self.goalState = self.goal(self.length)

        # Initalize where the 0 position is so i know what i can move 
        if(self.movePosX == None or self.movePosY == None):
            self.movePosX,self.movePosY = self.findPos(0)
        
        self.heuristicsValue = self.heuristics()
    
    def getState(self) -> object:
        '''
        Returns the State 
        '''
        return self.state
    
    def getLength(self) -> int:
        return self.length

    def getMovePos(self):
        return [self.movePosX,self.movePosY]

    def move(self):
        '''
        Figure out the movement that can be made by the puzzle and then figuring out which one to choose
        '''
        xLeft = None
        xRight = None
        yUp = None
        yDown = None
        xRHer = None
        xLHer = None
        yDHer = None
        yUHer = None
        if(self.heuristicsValue == 0):
            print(self.getState)
            return 3
        

        if (self.movePosX != (self.length - 1)):
            newState = deepcopy(self.state)
            temp = newState[self.movePosX][self.movePosY]
            newState[self.movePosX][self.movePosY] = newState[self.movePosX+1][self.movePosY]
            newState[self.movePosX+1][self.movePosY] = temp
            xRight = n_puzzle(newState,self.movePosX+1,self.movePosY,self)
            xRHer = xRight.heuristics()
        
        
        if (self.movePosX != 0):
            newState = deepcopy(self.state)
            temp = newState[self.movePosX][self.movePosY]
            newState[self.movePosX][self.movePosY] = newState[self.movePosX-1][self.movePosY]
            newState[self.movePosX-1][self.movePosY] = temp
            xLeft = n_puzzle(newState,self.movePosX-1,self.movePosY,self)
            xLHer = xLeft.heuristics()
        
        if (self.movePosY != (self.length - 1)):
            newState = deepcopy(self.state)
            temp = newState[self.movePosX][self.movePosY]
            newState[self.movePosX][self.movePosY] = newState[self.movePosX][self.movePosY+1]
            newState[self.movePosX][self.movePosY+1] = temp
            yDown = n_puzzle(newState,self.movePosX,self.movePosY+1,self)
            yDHer = yDown.heuristics()

        if (self.movePosY != 0):
            newState = deepcopy(self.state)
            temp = newState[self.movePosX][self.movePosY]
            newState[self.movePosX][self.movePosY] = newState[self.movePosX][self.movePosY-1]
            newState[self.movePosX][self.movePosY-1] = temp
            yUp = n_puzzle(newState,self.movePosX,self.movePosY-1,self)
            yUHer = yUp.heuristics()
        
        # Setting up a priority queue so that they are all added to the list
        priorQ = PriorityQueue()
    

        if(None != xRHer):
            priorQ.put((xRHer,xRight))
        if(None != xLHer):
            priorQ.put((xLHer,xLeft))
        if(None != yDHer):
            priorQ.put((yDHer,yDown))
        if (None != yUHer):
            priorQ.put((yUHer,yUp))
        return priorQ

    def reverseCall(self):
        if (self.parent != None):
            self.parent.reverseCall()
        print(self.state)

def import_file(textFile='n-puzzle.txt'):
    '''
    Import from n-puzzle and set up the array

    Returns:
    - start_state (array): the state at the beginning of the n-puzzle
    '''
    start_state = []
    with open(textFile, 'r') as in_file:
        lines = (in_file.read()).split("\n")

    for line in lines:
        start_state.append(line.split("\t"))

    for i in range (len(start_state)):
        for j in range (len(start_state[i])):
            start_state[i][j] = int(start_state[i][j])

    return start_state

def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    print("Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec))


start_time = time.time()
start_state = n_puzzle(import_file(textFile))
closed = []
openNodes = PriorityQueue()
node = start_state
count = 0
while True:
    closed.append(node.getState())  # Append the state, not the object
    
    temp = node.move()
    
    for i in range(temp.qsize()):
        if temp.queue[i][1].getState() not in closed:
            openNodes.put(temp.queue[i])
    if (openNodes.empty()):
        print("Unsolvable")
        break
    node = None
    while node == None:
        if openNodes.queue[0][1] not in closed:
            node = openNodes.queue[0][1]
        openNodes.get()
    
    # print("Iteration number:", count, " State:", node.getState())
    count += 1
    if node.heuristicsValue == 0:
        node.reverseCall()
        break
end_time = time.time()
time_lapsed = end_time - start_time
time_convert(time_lapsed)