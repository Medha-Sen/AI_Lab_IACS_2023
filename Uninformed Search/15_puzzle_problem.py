import numpy as np
global openlist
global closedlist
global path
global initial
global goal
global n   
global l
class Node: #node creation for each puzzle configuration
    def __init__(self,m,p,ac,c,l,tc):
      self.mat=m #state matrix
      self.parent=p #contains parent node
      self.action=ac  #stores action name
      self.cost=c #stores the cost per node
      self.level=l #stores the level of every node
      self.total_cost=tc #stores total cost

def print_matrix(mat):  #prints matrix corresponding to a state
  for i in range(n):
    for j in range(n):
      if (mat[i][j] == 0):
        print("-", end="  ")  #prints the blank tile
      else:
        print(mat[i][j], end="  ") #prints non-blank tile
    print()
  print("********************************************")
    
def print_path(): # prints the path from initial to goal state
      print("Starting configuration:\n")
      print_matrix(initial)
      for i in range(len(path)-1):
        print("\n Action: ", path[i][0], "\n")
        print("Resulting configuration: \n")
        print_matrix(path[i][1])
      print("\nGoal configuration:\n")
      print_matrix(goal)

def goal_test(n): # goal test
    if(np.array_equal(n.mat,goal)): #checks whether config are equal
     return True
    else:
     return False

def get_blank(n1): #gets row and column position of blank tile
    i, j = np.where(n1.mat == 0)
    return (i[0],j[0])

def in_openlist(mat): #checks whether in openlist
    for n in openlist:
        if np.array_equal(n.mat, mat): 
            return True
    return False

def in_closedlist(mat): #checks whether in closed list
    for n in closedlist:
        if np.array_equal(n.mat, mat): 
            return True
    return False
def succ(n1):
     (r,c)=get_blank(n1)
     l=[]
     if c!=0: #checking if leftmost column
        n2 = np.copy(n1.mat) #makes a copy of original state
        (n2[r][c],n2[r][c-1])=(n2[r][c-1],0) #swaps tiles
        l.append(('left',n2)) #stores action and resulting config
     if c!=n-1:#checking if rightmost column
        n2 = np.copy(n1.mat) 
        (n2[r][c],n2[r][c+1])=(n2[r][c+1],0)
        l.append(('right',n2))
     if r!=0: #checking if topmost row
         n2 =  np.copy(n1.mat)
         (n2[r][c],n2[r-1][c])=(n2[r-1][c],0)
         l.append(('up',n2))
     if r!=n-1:#checking if bottom most row
        n2 = np.copy(n1.mat)
        (n2[r][c],n2[r+1][c])=(n2[r+1][c],0)
        l.append(('down',n2))
     return l #returns list of potential successors

def get_cost(mat): #counts the number of misplaced tiles except blank tile
    count = 0
    for i in range(n):
        for j in range(n):
            if ((mat[i][j]) and (mat[i][j] != goal[i][j])):
                count += 1                 
    return count

def Tree_Search(initial):
    cost = get_cost(initial)
    n=Node(initial,None,None,cost,0,cost) #starting node
    openlist.append(n) #nodes encountered but not explored
    while(len(openlist)>0):
        n1=openlist.pop(0)
       # print_matrix(n1.mat) #uncomment to view the configurations that the algorithm is checking 
        if(goal_test(n1)==True):
          while n1.parent is not None: #path reconstruction
            path.insert(0,(n1.action,n1.mat))
            n1 = n1.parent
          return True
        for i in succ(n1):
          if not in_openlist(i[1]) and not in_closedlist(i[1]): #checking for repititions 
            cst=get_cost(i[1])
            n2= Node(i[1], n1,i[0],cst,n1.level+1,cst+n1.level+1) # cretaes the next node to be explored
            openlist.append(n2)
            openlist.sort(key=lambda x: x.total_cost) # sorted in terms of total cost
        closedlist.append(n1) #list of explored states
    return False

openlist=[]
closedlist=[]
path=[]
l=[]
n=int(input("Enter the value of n\n"))
print("Please enter the elements of the starting matrix in a single line and separated by a space, represent the blank with a zero:") 
entries = list(map(int, input().split()))
initial = np.array(entries).reshape(n, n)
print("Please enter the elements of the goal matrix in a single line and separated by a space, represent the blank with a zero:") 
entries = list(map(int, input().split()))
goal = np.array(entries).reshape(n, n)
if(Tree_Search(initial)):
    print_path()
else:
    print("No solution is available")