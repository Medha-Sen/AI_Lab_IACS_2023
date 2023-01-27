import numpy as np
from copy import deepcopy
global waitq  # global waiting queue
global sol  # list of solution states
global non_attack  # list of non-attacking states


class state:  # creates a state node

  def __init__(self, len):
    self.n = len
    self.mat = np.zeros((len, len))  # matrix of zeros


def print_matrix(s):  #prints matrix corresponding to a state
  for i in range(s.n):
    for j in range(s.n):
      if (s.mat[i][j] == 1):
        print("Q", end=" ")  #prints the queen
      else:
        print("-", end=" ")
    print()


def print_sol():  #prints a "state"
  for s in sol:
    print_matrix(s)
    print("************************************")  #demarcation


def goal(s1):  # checks whether the current state is the goal state
  if (np.sum(s1.mat) == s1.n):  #checks if all queens are placed
    return True
  else:
    return False


def is_safe(s1,r,c,):  # checks whether current state is safe
  if 1 in s1.mat[r]:  #queen in same row?
    return False

  for i in range(0, s1.n):  #queen in same column?
    if (s1.mat[i][c] == 1):
      return False

  for i in range(0, s1.n):  # queen in the diagonals?
    for j in range(0, s1.n):
      if (i + j == r + c) or (i - j == r - c):
        if s1.mat[i][j] == 1:
          return False
  return True


def repeated_state(s2):  # checks whether the current state is already in the wait queue
  for s in waitq:
    if np.array_equal(s.mat, s2.mat):  #checking the matrix
      return True
  return False


def last_queen(s1):  # returns the row number of the last placed queen in previous row iteration
  k = -1
  for i in range(n):
    for j in range(n):
      if s1.mat[i][j] == 1:
        k = i
  return k


def succ(s1):  # adds safe successors to the wait queue
  r = last_queen(s1)  #gets row number of the last placed queen in previous row iteration
  if r != -1 and r != s1.n - 1:  #excluding cases where no queen is present and the case where all queens are placed
    for i in range(r + 2):
      for j in range(s1.n):
        if (s1.mat[i][j] == 0 and is_safe(s1, i, j) == True):  # checks whether safe state or not
          s2 = deepcopy(s1)  # deep copies the state
          s2.mat[i][j] = 1
          if (repeated_state(s2) == False):  # checks whether repeated state or not
            waitq.append(s2)
            non_attack.append(s2)
  else:  
    if r != s1.n - 1:  # excluding the case where all queens are filled
      for i in range(n):
        s2 = deepcopy(s1)
        s2.mat[0][i] = 1
        waitq.append(s2)
        non_attack.append(s2)


def Tree_Search(x):  # implements DFS
  s = state(x)
  waitq.append(s)  #appending to the wait queue
  while (len(waitq) > 0):
    s1 = waitq.pop(0)  # popping from the wait queue
    if (goal(s1)):  #checking whether goal is met or not
      sol.append(s1)  # appending to the list of solutions
    succ(s1)  # adding the successors to the wait queue


# initializing all the global lists
sol = []
waitq = []
non_attack = []
n = int(input("Enter the value of n \n"))
Tree_Search(n)
if (len(sol) > 0):
  print_sol()  #prints solutions
  print("Number of solutions: ", len(sol))
  print("Number of non attacking states excluding the state with 0 queens on the board: ", len(non_attack))
  print("Number of non attacking states including the state with 0 queens on the board: ", len(non_attack)+1)
else:
  print("No solution is possible")
