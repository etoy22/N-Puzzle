from math import sqrt
from copy import deepcopy
from queue import PriorityQueue
import time

textFile="n-puzzle.txt"

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
        '''
        Here in case a comparison needs to be made
        '''
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
        This will be done using Manhattan Distance
        In this code in a block of comments is my Euclidian Distance model as that works as well
        and developed it first and realized that Manhatten Distance works better
        '''
        distance = 0
        for i in range(self.length):
            for j in range (self.length):
                value = self.state[i][j]
                if value != 0:
                    '''
                    Made Euclidian Distance model before realizing while it works its not the best
                    in this case and i could just do 
                    xPos = value //self.length
                    yPos = (value)%self.length
                    xCalc = (xPos-i)**2
                    yCalc = (yPos-j)**2
                    calc = sqrt(xCalc+yCalc)
                    '''

                    '''
                    This is Manhattan Distance for one block
                    '''
                    xPos = value //self.length # Finds the values goal state y cordinate
                    yPos = (value)%self.length # Finds the values goal state y cordinate

                    xCalc = abs(xPos-i) # Figures out the x distance
                    yCalc = abs(yPos-j) # Figures out the y distance
                    calc = xCalc+yCalc # Figures out that blocks Manhatten Distance


                    distance += calc # Adds to total distance
        return distance

    def __init__(self,state,movePosX=None,movePosY=None,parent=None):
        '''
        Set up command
        

        '''
        self.state = state
        self.parent = parent
        self.length = len(state)
        self.movePosX = movePosX
        self.movePosY = movePosY
        # Initalize where the 0 position is so i know what i can move 
        if(self.movePosX == None or self.movePosY == None):
            self.movePosX,self.movePosY = self.findPos(0)
        
        self.heuristicsValue = self.heuristics()
    
    def getState(self) -> object:
        '''
        Returns the State 
        '''
        return self.state
    
    def move(self):
        '''
        Figure out the movement that can be made by the puzzle and then figuring out which one to choose
        '''

        # The possible moves
        xLeft = None
        xRight = None
        yUp = None
        yDown = None
     

        if (self.movePosX != (self.length - 1)):
            newState = deepcopy(self.state) # Deep copy makes it so its not a complete replica
            temp = newState[self.movePosX][self.movePosY]
            newState[self.movePosX][self.movePosY] = newState[self.movePosX+1][self.movePosY]
            newState[self.movePosX+1][self.movePosY] = temp
            xRight = n_puzzle(newState,self.movePosX+1,self.movePosY,self)
        
        if (self.movePosX != 0):
            newState = deepcopy(self.state)
            temp = newState[self.movePosX][self.movePosY]
            newState[self.movePosX][self.movePosY] = newState[self.movePosX-1][self.movePosY]
            newState[self.movePosX-1][self.movePosY] = temp
            xLeft = n_puzzle(newState,self.movePosX-1,self.movePosY,self)
        
        if (self.movePosY != (self.length - 1)):
            newState = deepcopy(self.state)
            temp = newState[self.movePosX][self.movePosY]
            newState[self.movePosX][self.movePosY] = newState[self.movePosX][self.movePosY+1]
            newState[self.movePosX][self.movePosY+1] = temp
            yDown = n_puzzle(newState,self.movePosX,self.movePosY+1,self)

        if (self.movePosY != 0):
            newState = deepcopy(self.state)
            temp = newState[self.movePosX][self.movePosY]
            newState[self.movePosX][self.movePosY] = newState[self.movePosX][self.movePosY-1]
            newState[self.movePosX][self.movePosY-1] = temp
            yUp = n_puzzle(newState,self.movePosX,self.movePosY-1,self)
        
        # Setting up a priority queue so that they are all added to the list
        priorQ = PriorityQueue()
    
        if(None != xRight):
            priorQ.put((xRight.heuristicsValue,xRight))
        if(None != xLeft):
            priorQ.put((xLeft.heuristicsValue,xLeft))
        if(None != yDown):
            priorQ.put((yDown.heuristicsValue,yDown))
        if (None != yUp):
            priorQ.put((yUp.heuristicsValue,yUp))
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


if __name__ == "__main__":
    node = n_puzzle(import_file(textFile)) # Loads the text file and makes it the first state
    closed = [] # Says which combinations have already been tried 
    nextState = PriorityQueue()
    while True:
        closed.append(node.getState())  # Append the state, not the object
        newStates = node.move() # Gets the new States taht might be added
        for i in range(newStates.qsize()):
            if newStates.queue[i][1].getState() not in closed: # Only adds the new state if its not on the closed list
                nextState.put(newStates.queue[i])
        node = None
        while node == None: # Only loads in the new state if its not on the closed list
            if nextState.queue[0][1] not in closed:
                node = nextState.queue[0][1]
            nextState.get()
        
        if node.heuristicsValue == 0: # Once its done
            node.reverseCall() 
            break