"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import copy
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

def depthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""

    node ={'state': problem.getStartState(),'cost':0}

    if problem.isGoalState(node['state']):
        return
    
    frontier =util.Stack()
    frontier.push(node)

    explored =set()

    while True:
        if frontier.isEmpty:
            raise Exception('Search failed!')
        
        node=frontier.pop()
        explored.add(node['state'])

        successors =problem.getSuccessors(node['state'])
        for successor in successors:
            child ={'state':successor[0],'action': successor[1],'cost':successor[2],'parent':successor[3]}
            if child['state'] not in explored:
                if problem.isGoalState(child['state']):
                    actions=[]
                    node = child
                    while 'parent' in node:
                        actions.append(node['parent'])
                        node =node['parent']
                    actions.reverse()
                    return actions
                frontier.push(child)

    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""

    node ={'state': problem.getStartState(),'cost':0}

    if problem.isGoalState(node['state']):
        return
    
    frontier =util.Queue()
    frontier.push(node,0)

    explored =set()

    while True:
        if frontier.isEmpty:
            raise Exception('Search failed!')
        
        node=frontier.pop()
        explored.add(node['state'])

        successors =problem.getSuccessors(node['state'])
        for successor in successors:
            child ={'state':successor[0],'action': successor[1],'cost':successor[2],'parent':successor[3]}
            if child['state'] not in explored:
                if problem.isGoalState(child['state']):
                    actions=[]
                    node = child
                    while 'parent' in node:
                        actions.append(node['parent'])
                        node =node['parent']
                    actions.reverse()
                    return actions
                frontier.push(child)
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""

    node ={'state': problem.getStartState(),'cost':0}

    if problem.isGoalState(node['state']):
        return
    
    frontier =util.PriorityQueue()
    frontier.push(node)

    explored =set()

    while True:
        if frontier.isEmpty:
            raise Exception('Search failed!')
        
        node=frontier.pop()
        explored.add(node['state'])
        end = node[-1]

        if end[0] not in explored or end[2] <= explored[end[0]]:
            if problem.isGoalState(end[0]):
                return [state[1] for state in node[1:]]

            successors = problem.getSuccessors(end[0])
            for successor in successors:
                if successor[0] not in explored or (end[2] + successor[2]) < explored[successor[0]]:
                    explored[successor[0]] = end[2] + successor[2]
                    new_node = copy.deepcopy(node)
                    new_succ = (successor[0], successor[1], end[2] + successor[2])
                    new_node.append(new_succ)
                    frontier.push(new_node, end[2] + successor[2])

    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = util.PriorityQueue()

    start_state = problem.getStartState()
    start = (start_state, "", (0, heuristic(start_state, problem)))
    frontier.push([start], start[2])

    visited_state = {start_state[0]: sum(start[2])}

    while not frontier.isEmpty():
        node = frontier.pop()

        if not frontier.isEmpty():
            next_node = frontier.pop()
            temp = [node, next_node]

            while not frontier.isEmpty() and sum(node[-1][2]) == sum(next_node[-1][2]):
                next_node = frontier.pop()
                temp.append(next_node)
            
            tie_nodes = temp if sum(node[-1][2]) == sum(next_node[-1][2]) else temp[:-1]

            for n in tie_nodes:
                if node[-1][2][0] < n[-1][2][0]:
                    node = n

            for n in temp:
                if node != n:
                    frontier.push(n, sum(n[-1][2]))

        end = node[-1]
        if end[0] not in visited_state or sum(end[2]) <= visited_state[end[0]]:
            if problem.isGoalState(end[0]):
                return [state[1] for state in node[1:]]

            successors = problem.getSuccessors(end[0])
            for successor in successors:
                gn_succ = end[2][0] + successor[2]
                hn_succ = heuristic(successor[0], problem)
                fn_succ = gn_succ + hn_succ
                if successor[0] not in visited_state or fn_succ < visited_state[successor[0]]:
                    visited_state[successor[0]] = fn_succ
                    new_node = copy.deepcopy(node)
                    new_succ = (successor[0], successor[1], (gn_succ, hn_succ))
                    new_node.append(new_succ)
                    frontier.push(new_node, fn_succ)
    return []

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
