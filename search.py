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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    # NORTH = 'North' SOUTH = 'South' EAST = 'East' WEST = 'West' STOP = 'Stop'
    "*** YOUR CODE HERE ***"
    search_stack = util.Stack()
    successors = problem.getSuccessors(problem.getStartState())
    for ea in successors:
        search_stack.push(ea)
    find_goal = False
    path_actions = []

    visited_pos = set()
    visited_pos.add(problem.getStartState())

    while search_stack.isEmpty() == False  and  find_goal == False:
        choice = search_stack.pop()
        if not problem.isGoalState(choice[0]):
            if choice[0]  not in visited_pos :
                visited_pos.add(choice[0])
                path_actions.append(choice)
            choice_successors = filter(lambda v: v[0] not in visited_pos, problem.getSuccessors(choice[0]))
            if not len(choice_successors):
                path_actions.pop(-1)
                if path_actions:
                    search_stack.push(path_actions[-1])
            else:
                for ea in choice_successors:
                    search_stack.push(ea)
        else:
            path_actions.append(choice)
            visited_pos.add(choice[0])
            find_goal = True
            print  choice
    #print  path_actions
    print path_actions
    return [ea[1] for ea in path_actions]
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    search_queue = util.Queue()
    successors = problem.getSuccessors(problem.getStartState())
    for ea in successors:
        search_queue.push(ea)
        print ea
    find_goal = False
    father_pos = dict()
    path_actions = []
    visited_pos = set()
    visited_pos.add(problem.getStartState())
    successors = problem.getSuccessors(problem.getStartState())
    for ea0 in successors:
        visited_pos.add(ea0[0])
    print visited_pos

    while search_queue.isEmpty()==False and find_goal == False:
        choice = search_queue.pop()
        print "pop:"
        print choice[0]
        if not problem.isGoalState(choice[0]):
            choice_successors = filter(lambda v: v[0] not in visited_pos, problem.getSuccessors(choice[0]))
            print "choice_sucessors:"
            print  problem.getSuccessors(choice[0])
            print  choice_successors
            for ea1 in choice_successors :
                print "ea1:"
                print ea1
                visited_pos.add(ea1[0])
                father_pos[ea1[0]]=choice
                print visited_pos
                search_queue.push(ea1)
                continue
        else:
            visited_pos.add(choice[0])
            path_actions.append(choice)
            find_goal = True
    print "father-pos:"
    print father_pos
    print "path-:"

    nodelist = path_actions[0]  #((1,1),'west',1)
    visited_pos2 = set()
    visited_pos2.add(nodelist[0])
    while nodelist not in problem.getSuccessors(problem.getStartState()):
        path_actions.append(father_pos[nodelist[0]])
        nodelist = father_pos[nodelist[0]]

    path_actions2 = path_actions[::-1]
    print path_actions2
    return [ea[1] for ea in path_actions2]



def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
