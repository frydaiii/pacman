# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    visited = set()
    path = []
    currentPath = util.Stack()

    stack = util.Stack()
    stack.push(problem.getStartState())
    while not stack.isEmpty():
        currentState = stack.pop()
        visited.add(currentState)

        if problem.isGoalState(currentState):
            break

        for successor in problem.getSuccessors(currentState):
            state = successor[0]
            direction = successor[1]
            if state not in visited:
                stack.push(state)
                currentPath.push(path+[direction])
        path = currentPath.pop()

    return path

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # visited = set()
    visited = []
    path = []
    currentPath = util.Queue()

    queue = util.Queue()
    queue.push(problem.getStartState())
    while not queue.isEmpty():
        currentState = queue.pop()
        if currentState not in visited:
            visited.append(currentState)

            if problem.isGoalState(currentState):
                break

            for successor in problem.getSuccessors(currentState):
                state = successor[0]
                direction = successor[1]

                queue.push(state)
                currentPath.push(path+[direction])
        path = currentPath.pop()

    return path

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    from util import Queue,PriorityQueue
    fringe = PriorityQueue()
    fringe.push(problem.getStartState(),0)
    visited = []
    tempPath=[]
    path=[]
    pathToCurrent=PriorityQueue()
    currState = fringe.pop()
    while not problem.isGoalState(currState):
        if currState not in visited:
            visited.append(currState)
            successors = problem.getSuccessors(currState)
            for child,direction,cost in successors:
                tempPath = path + [direction]
                costToGo = problem.getCostOfActions(tempPath)
                if child not in visited:
                    fringe.push(child,costToGo)
                    pathToCurrent.push(tempPath,costToGo)
        currState = fringe.pop()
        path = pathToCurrent.pop()    
    return path

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def calculateFn(problem, generatedState, heuristic):
    f_n = problem.getCostOfActions(generatedState[1]) + heuristic(generatedState[0], problem)
    return f_n 

from util import PriorityQueue, Stack

class MyPriorityQueueWithFunction(PriorityQueue):
    """
    Implements a priority queue with the same push/pop signature of the
    Queue and the Stack classes. This is designed for drop-in replacement for
    those two classes. The caller has to provide a priority function, which
    extracts each item's priority.
    """
    def  __init__(self, problem, priorityFunction):
        "priorityFunction (item) -> priority"
        self.priorityFunction = priorityFunction      # store the priority function
        PriorityQueue.__init__(self)        # super-class initializer
        self.problem = problem

    def push(self, item, heuristic):
        "Adds an item to the queue with priority from the priority function"
        PriorityQueue.push(self, item, self.priorityFunction(self.problem, item, heuristic))

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    path = []

    open_list = MyPriorityQueueWithFunction(problem, calculateFn)

    close_list = []

    if problem.isGoalState(problem.getStartState()):
        return []


    open_list.push((problem.getStartState(), []), heuristic)


    while (True):
        if open_list.isEmpty():
            return []

        currentState = open_list.pop()

        current_state = currentState[0]

        path = currentState[1]

        if current_state in close_list:
            continue

        if problem.isGoalState(current_state):
            return path

        generatedStates = problem.getSuccessors(current_state)
        close_list.append(current_state)

        for generatedState in generatedStates:
            if generatedState[0] not in close_list:
                open_list.push((generatedState[0], path + [generatedState[1]]), heuristic)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
