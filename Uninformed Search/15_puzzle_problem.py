import numpy as np
from copy import deepcopy
global openlist
global closedlist
global path
global initial
global goal
global n   
global l
class Node:
    def __init__(self,m,p,ac,c):
      self.mat=m
      self.parent=p
      self.action=ac
      self.cost=c

def print_matrix(mat):  #prints matrix corresponding to a state
  for i in range(n):
    for j in range(n):
      if (mat[i][j] == 0):
        print("-", end="  ")  #prints the queen
      else:
        print(mat[i][j], end="  ")
    print()
  print("********************************************")
    
def print_path():
      print("Starting configuration:\n")
      print_matrix(initial)
      for i in path:
        print("\n Action: ", i[0], "\n")
        print("Resulting configuration: \n")
        print_matrix(i[1])
      print("\nGoal configuration:\n")
      print_matrix(goal)

def goal_test(n):
    if(np.array_equal(n.mat,goal)):
     return True
    else:
     return False

def get_blank(mat):
    i, j = np.where(mat == 0)
    return (i[0],j[0])

def in_openlist(mat):
    for n in openlist:
        if np.array_equal(n.mat, mat):  #checking the matrix
            return True
    return False

def in_closedlist(mat):
    for n in closedlist:
        if np.array_equal(n.mat, mat):  #checking the matrix
            return True
    return False
def succ(n1):
     (r,c)=get_blank(n1.mat)
     l=[]
     if c!=0:
        n2 = np.copy(n1.mat)
        (n2[r][c],n2[r][c-1])=(n2[r][c-1],0)
        l.append(('left',n2))
     if c!=n-1:
        n2 = np.copy(n1.mat)
        (n2[r][c],n2[r][c+1])=(n2[r][c+1],0)
        l.append(('right',n2))
     if r!=0:
         n2 =  np.copy(n1.mat)
         (n2[r][c],n2[r-1][c])=(n2[r-1][c],0)
         l.append(('up',n2))
     if r!=n-1:
        n2 = np.copy(n1.mat)
        (n2[r][c],n2[r+1][c])=(n2[r+1][c],0)
        l.append(('down',n2))
     return l

def get_cost(mat):
    count = 0
    for i in range(n):
        for j in range(n):
            if ((mat[i][j]) and (mat[i][j] != goal[i][j])):
                count += 1                 
    return count

def Tree_Search(initial):
    cost = get_cost(initial)
    n=Node(initial,None,None,cost)
    openlist.append(n)
    while(len(openlist)>0):
        n1=openlist.pop(0)
        print_matrix(n1.mat)
        if(goal_test(n1)==True):
          while n1.parent is not None:
            path.insert(0,(n1.action,n1.mat))
            n1 = n1.parent
          return True
        for i in succ(n1):
          if not in_openlist(i[1]) and not in_closedlist(i[1]):
            cst=get_cost(i[1])
            n2= Node(i[1], n1,i[0],cst)
            openlist.append(n2)
            openlist.sort(key=lambda x: x.cost)
        closedlist.append(n1)
    return False
def parity_checker(mat): #checks the parity
  temp = []
  inv=0
  for i in range(n):
    for j in range(n):
        temp.append(mat[i][j])
  for i in range(len(temp)):
      x = i+1
      for j in range(x, len(temp)):
          if(temp[i] and temp[j] and (temp[i] > temp[j])):
              inv+=1 #counting no. of inversions
  if n%2!=0:# odd n
    if inv%2==0:
      return 1
    else:
      return 0
  else: #even n
    (r,c)=get_blank(mat)
    inv=inv+r
    if inv%2==0:
      return 1
    else:
      return 0
      
def solvable():
  if n%2!=0 and parity_checker(initial)!=parity_checker(goal):
    return False
  if n%2==0 and parity_checker(initial)!=parity_checker(goal):
    return False
  return True

openlist=[]
closedlist=[]
path=[]
l=[]
n=int(input("Enter the value of n\n"))
print("Please enter the elements of the starting matrix in a single line and separated by a space, represent the blank with a zero:") 
entries = list(map(int, input().split()))
initial = np.array(entries).reshape(n, n)
#print(initial)
#initial = np.array([[1, 3, 4], [7, 0, 6], [8, 5, 2]])
print("Please enter the elements of the goal matrix in a single line and separated by a space, represent the blank with a zero:") 
entries = list(map(int, input().split()))
goal = np.array(entries).reshape(n, n)
#print(goal)
#goal = np.array([[0, 1, 3], [4, 7, 6], [8, 5, 2]])
if (solvable()==True):
    if(Tree_Search(initial)):
        print_path()
    else:
        print("No solution is available")
else:
     print("Not solvable")
