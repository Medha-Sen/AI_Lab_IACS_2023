"""
Search (Chapters 3-4)
The way to use this code is to subclass Problem to create a class of problems,
then create problem instances and solve them with calls to the various search
functions.
"""
import copy
from random import randint
import numpy as np
from utils import *

class Problem:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value. Hill Climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError


# ______________________________________________________________________________


class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_graph_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        return hash(self.state)


# ______________________________________________________________________________
def hill_climbing(problem):
    """
    [Figure 4.2]
    From the initial node, keep choosing the neighbor with highest value,
    stopping when no neighbor is better.
    """
    action_count=0 #counts the number of moves taken by the local search algorithm 
    current = Node(problem.initial)
    while True:
        neighbors = current.expand(problem)
        if not neighbors:
            break
        neighbor = argmin_random_tie(neighbors, key=lambda node: problem.value(node)) #neighbor minimizing obj function
        if problem.value(neighbor) > problem.value(current): #local minima reached
            print("No. of actions taken ",action_count) #print the total number of actions taken
            print("Final state:")
            return current.state #returns the final state
        current = neighbor #next to be expanded
        action_count=action_count+1 #new neighbor selected-action increases by 1
        print("Objective function in action ",action_count," is ",problem.value(neighbor)) #prints objective function
    print("No. of actions taken ",action_count) #prints total number of actions taken
    print("Final state:")
    return current.state

class nQueens(Problem):
    def __init__(self, n):
        self.N = n
        l=[-1]*n # temporary list to hold the state tuple
        for i in range(n):
            l[i] = randint(0, 100000) % n #selecting random row(0-n) for placing the queen in each column
        self.initial=tuple(i for i in l)
        print("Initial state:")
        self.board(self.initial)
        Problem.__init__(self, self.initial)#call to the parent class Problem

    def actions(self, state):
        act=[] #returns a list of tuples of actions
        for col in range(len(state)):
            for row in range(self.N):
                if row != state[col]: #selecting every row except the one which is currently filled in each column of state
                    act.append((row,col)) # append to the list of tuples of actions
        return act

    def result(self, state, action):
        """Place the next queen at the given row."""
        new_state = list(state[:]) #copies the state
        new_state[action[1]] = action[0] #makes the necessary changes as per the action given in the argument
        return new_state

    def two_coord_conflict(self, row1, col1, row2, col2):
        #checks if the queens placed at two co-ordinates conflict
        if (row1 == row2) or (col1 == col2) or ((row1 - col1) == (row2 - col2)) or ((row1 + col1) == (row2 + col2)):
            return True
        else:
            return False
        
    def board(self,state): #prints the board 
        board_mat=np.zeros((self.N,self.N))
        for i in range(self.N):
            board_mat[state[i]][i]=1
        for i in range(self.N):
            for j in range(self.N):
                if board_mat[i][j]==1:
                    print('Q',end=' ')
                else:
                    print('-',end=' ')
            print()
    
    def value(self, node):
        conflicts = 0 #counts the number of conflicting queens in the current node state
        for (r1, c1) in enumerate(node.state):
            for (r2, c2) in enumerate(node.state):
                if (r1, c1) != (r2, c2):
                    conflicts += self.two_coord_conflict(r1, c1, r2, c2)
        return conflicts #returns the number of conflicting queens
print("Enter the value of n")
n=int(input())
if n!=2 and n!=3:
    ob=nQueens(n)
    ob.board(hill_climbing(ob))
else:
    print("No solution available")
