import numpy as np
import heapq
from itertools import permutations,combinations
from copy import deepcopy
global MC # cost matrix
global CC # dash insertion cost
global V # vocabulary
global n # length of max string
global k # number of strings
global openlist
global closedlist
class State:
    def __init__(self, strings, col_cost, total_cost, col, parent,h=None):
        self.strings = strings
        self.col_cost = col_cost
        self.total_cost = total_cost
        self.col = col
        self.parent = parent
        self.heuristic_value = h

    def is_goal(self): #DONE
        # Checking if we have reached a leaf i.e we are in the last column for inserting dashes
        if self.col==n-1:
            return True
        else:
            return False
    def check(self): # checking if the current set of strings have all reached the maximum length n
        if all(len(s) ==n for s in self.strings):
           return True
        else:
           return False
    def generate_col_string(self,col): # generates the string of requested column 
      l=[] 
      for s in self.strings:
          l.append(s[col:col+1])
      return ''.join(l)
    
    def calculate_col_cost(self,s): # return the cost of pairwise comparison between the columns
      ccost=0
      for i in range(len(s)-1):
        ccost=ccost+MC[(s[i:i+1],s[i+1:i+2])]
      ccost=ccost+MC[(s[-1],s[0:1])]
      #print("cost for ",s," is ",cost)
      return ccost
    
    def calculate_full_cost(self): #for those achieving full length prematurely
        cost1=0
        cost2=0
        for s in self.strings:
           k=s.count("-")
           cost1=cost1+(k*CC)
        for i in range(n):
           temp=self.generate_col_string(i)
           #print(temp)
           cost2=cost2+self.calculate_col_cost(temp)
        #print(cost2)
        return cost1+cost2
    
    def reconstruct_strings(self,col,s): # reconstructing the string by adding the previously modified parts of the string to the currently modified part
      new_strings = []
      for i in range(len(self.strings)):
        if s[i]=='-':
          temp=self.strings[i][:col+1]+'-'+self.strings[i][col+1:]
          new_strings.append(temp)
        else:
          new_strings.append(self.strings[i])
      return new_strings
    
    def generate_child_states(self,col):
      # Generate child states by inserting dashes in the next column
      child_states = []
      generated_states=[]
      col_string = self.generate_col_string(col)
      if all(len(s) > col for s in self.strings):
        for num_dashes in range(len(self.strings) + 1):
            for dashes in combinations(range(len(self.strings)), num_dashes):
                new_col_string = list(col_string)
                #print(dashes)
                for dash in dashes:
                    #print(new_col_string)
                    #print(dash)
                    new_col_string[dash] = '-'
                child_states.append(''.join(new_col_string))
        if '-'*k in child_states:
          child_states.remove('-'*k)
        for s in child_states:
          temp_strings=self.reconstruct_strings(col,s)
          col_cost_temp=self.calculate_col_cost(s)
          total_cost_temp=self.total_cost+col_cost_temp
          if all(len(s) <= n for s in temp_strings):
            generated_states.append(State(temp_strings,col_cost_temp,total_cost_temp,col+1,None))      
      return generated_states
    
    def calculate_heuristic(self):
        # Estimate the cost of reaching a goal state from the current state
        h=self.total_cost
        for s in self.strings:
           k=s.count("-")
           h=h+(k*CC)
        return h
    
def branch_and_bound(strings):
    # Initialize the root state
    root_state = State(strings, col_cost=0, total_cost=0, col=0, parent=None)
    
    # Initialize the stack with the root state
    stack = [root_state]
    #print("Starting out......", root_state.strings)
    # Initialize the closed list
    closed_list = set() 
    # Initialize the best solution
    best_solution = State(strings,1000000,100000,0,None,100000)    
    # Loop until the stack is empty or all states have been explored
    while stack:
        # Popping from the stack
        current_state = stack.pop()
        #print("Currently exploring....",current_state.strings)
        
        # Check if the current state is a goal state
        if current_state.is_goal() or current_state.check(): #DONE
            # Update the best solution if necessary
            if current_state.check()==True:
               current_state.heuristic_value=current_state.calculate_full_cost()
            if current_state.total_cost==0 or current_state.heuristic_value < best_solution.heuristic_value:
                best_solution = current_state
                #print("Best solution found....",best_solution.strings," with cost ", best_solution.heuristic_value)
            else:
               continue
        else:
            # Generate child states by inserting dashes in the given column
            child_states = current_state.generate_child_states(current_state.col)
            #for i in child_states:
              #print(i.strings)
            # Add the child states to the open list if they haven't been explored yet
            for child_state in child_states:
                if child_state not in closed_list:
                    # Calculate the cost and heuristic value of the child state
                    child_state.parent=current_state
                    child_state.heuristic_value = child_state.calculate_heuristic()                    
                    # Add the child state to the open list
                    stack.append(child_state)            
            # Add the current state to the closed list
            stack.sort(key=lambda x: x.heuristic_value) #sorting on the basis of the heuristic value
            closed_list.add(current_state)
    
    # Return the best solution
    return best_solution    
MC={}
CC=0
with open("input.txt","r") as f:
    v_n=int(f.readline().strip())
    V=f.readline().strip().split(', ')
    k=int(f.readline().strip())
    X=[f.readline().strip() for i in range(k)]
    CC=int(f.readline().strip())
    for i in range(len(V)):
        temp=f.readline().split()
        for j in range(i,len(V)):
            MC[(V[i],V[j])] = MC[(V[j],V[i])]= int(temp[j])
        MC[(V[i],'-')]=MC[('-',V[i])]=int(temp[j])
    temp=f.readline().split()
    MC[('-', '-')] = int(temp[-1])
n=max([ len(x) for x in X])
state=branch_and_bound(X)
#print(state.strings)
print("cost: ",state.heuristic_value)
with open("output.txt", "w") as f:
    for i in state.strings:
        f.write(i+'\n')    
f.close()
print("Reading from file....")
with open("output.txt","r") as f:
   lines = f.readlines()
for line in lines:
   print(line.strip())
    