
# This module should implement a logical agent and a world for it to explore.

import logic as logic
import inference

class WumpusWorldAgent(inference.KnowledgeBasedAgent):

  """
  Use two for loops to cycle through each of the squares on the board.
  Then, acquire a set of neighboring spaces using the get_neighbors 
  function provided. From here, we use another for loop to cycle through
  each neighbor, and make two expressions that we will feed to the 
  knowledge base. These expressions are co-implications that give the KB
  the knowledge that the squares adjacent to a pit have a breeze/one of
  the adjacent squares to a breeze has a pit and that the squares adjacent 
  to a wumpus have a stench/one of the adjacent squares to a stench has a 
  wumpus. The goal here is to give the KB the minimum amount of information
  necessary, while still providing enough so that it can resolve any
  information that it needs to obtain.
  """
  def __init__(self, cave_size):
    self.KB = logic.PropKB()
    self.size = cave_size
    for i in range(1, cave_size + 1):
      for j in range(1, cave_size + 1):
        neighbors = get_neighbors(i, j, cave_size)
        exp1 = 'B%d_%d <=> (' % (i,j)
        exp2 = 'S%d_%d <=> (' % (i,j)
        for k in range(len(neighbors)):
          if k == len(neighbors) - 1:
            exp1 += ' P%d_%d)' % neighbors[k]
            exp2 += ' W%d_%d)' % neighbors[k]
          else:
            exp1 += ' P%d_%d |' % neighbors[k]
            exp2 += ' W%d_%d |' % neighbors[k]
        self.KB.tell(logic.expr(exp1))
        self.KB.tell(logic.expr(exp2))
  """
  Create a set of safe spaces, and, using two for loops, go throuh every space.
  If we have safely visited the space, add it to the safe set. If we can resolve
  that the space does not have a wumpus and does not have a pit, add it to the 
  safe set.
  """
  def safe(self):
    ## AI Lab assignment 3.2
    safe_set=set() #set of all safe sets
    for i in range(1, self.size + 1):
      for j in range(1, self.size +1):
        curr_loc='{0}{1}_{2}'.format("CL",i,j) #current location
        no_pit='{0}{1}_{2}'.format("~P",i,j) #no pit sentence
        no_wumpus='{0}{1}_{2}'.format("~W",i,j) #no wumpus sentence
        no_stench='{0}{1}_{2}'.format("~S",i,j) #no stench sentence
        no_breeze='{0}{1}_{2}'.format("~B",i,j) #no breeze sentence
        alpha_1=logic.expr(curr_loc)
        alpha_2=logic.expr(no_pit)
        alpha_3=logic.expr(no_wumpus)
        alpha_4=logic.expr(no_stench)
        alpha_5=logic.expr(no_breeze)
        if (inference.resolution(self.KB,alpha_1)):
          safe_set.add((i,j)) #adding current location to the safe set
        if (inference.resolution(self.KB,alpha_2)) and (inference.resolution(self.KB,alpha_3)):
          safe_set.add((i,j)) #add if no pit and no wumpus at current location
        if (inference.resolution(self.KB,alpha_4)) and (inference.resolution(self.KB,alpha_5)):
          for k in get_neighbors(i,j,self.size): #add if no stench and no breeze at current location
            safe_set.add(k)
    return safe_set

  """
  Create a set of not unsafe spaces, and, using two for loops, go through every space.
  If we can resolve that the space does not contain a wumpus or a pit, add the space
  to the set of not unsafe spaces.
  """
  def not_unsafe(self):
    ## AI Lab assignment 3.2
    not_unsafe_set=set() #set of all not unsafe sets
    for i in range(1, self.size + 1):
      for j in range(1, self.size +1):
        curr_loc='{0}{1}_{2}'.format("CL",i,j) #current location
        is_pit='{0}{1}_{2}'.format("P",i,j) #is a pit sentence
        is_wumpus='{0}{1}_{2}'.format("W",i,j) #wumpus present sentence
        no_stench='{0}{1}_{2}'.format("~S",i,j)# stench present sentence
        no_breeze='{0}{1}_{2}'.format("~B",i,j)# breeze present sentence
        alpha_1=logic.expr(curr_loc)
        alpha_2=logic.expr(is_pit)
        alpha_3=logic.expr(is_wumpus)
        alpha_4=logic.expr(no_stench)
        alpha_5=logic.expr(no_breeze)
        if not (inference.resolution(self.KB,alpha_1)):
          not_unsafe_set.add((i,j))
        if (inference.resolution(self.KB,alpha_2)) or (inference.resolution(self.KB,alpha_3)):
          if (i,j) in not_unsafe_set: # if a pit or wumpus present in that location, remove from not unsafe set
            not_unsafe_set.remove((i,j))
        if (inference.resolution(self.KB,alpha_4)) and (inference.resolution(self.KB,alpha_5)):
          for k in get_neighbors(i,j,self.size): #if stench or breeze present, add to the not unsafe set
            not_unsafe_set.add(k)
    return not_unsafe_set
    """
    Create a set of unvisited spaces, and, using two for loops, go through every space.
    If the space does not appear in the KB as having been visited, add the space to
    the set of unvisited spaces.
    """
  def unvisited(self):
    unvisited = set([])
    for i in range(1, self.size + 1):
      for j in range(1, self.size +1):
        if logic.expr('L%d_%d' % (i,j)) not in self.KB.clauses:
          unvisited.add((i,j))
    return unvisited

class World:
  def __init__(self, size, gold, pits, wumpus):
    self.size = size
    self.gold = gold
    self.pits = pits
    self.wumpus = wumpus

# perceives the world and updates the KB
  def perceive(self, myTuple, KB):
    x,y = myTuple
    print(f"You enter room [{x},{y}]")
    KB.tell('L%d_%d' % (x, y))

    if (x, y) in self.pits:
      print("Oh no, you have fallen into a pit!")
      raise inference.GameOver(inference.RESULT_DEATH)
    else:
      KB.tell('~P%d_%d' % (x, y))

    if (x, y) == self.wumpus:
      print("Oh no, you have wandered into the Wumpus\' room!")
      raise inference.GameOver(inference.RESULT_DEATH)
    else:
      KB.tell('~W%d_%d' % (x, y))

    if any((x1, y1) in self.pits for x1, y1 in get_neighbors(x,y, self.size)):
      print('You feel a breeze')
      KB.tell('B%d_%d' % (x, y))
    else:
      KB.tell('~B%d_%d' % (x, y))

    if any((x1, y1) == self.wumpus for x1, y1 in get_neighbors(x,y, self.size)):
      print('You smell a stench')
      KB.tell('S%d_%d' % (x, y))
    else:
      KB.tell('~S%d_%d' % (x, y))

    if (x, y) == self.gold:
      print('You found the gold!')
      raise inference.GameOver(inference.RESULT_WIN)

NEIGHBOR_DELTAS = ((+1, 0), (-1, 0), (0, +1), (0, -1))

def get_neighbors(x, y, cave_size):
  possible_neighbors = [(x + dx, y + dy) for dx, dy in NEIGHBOR_DELTAS]
  return [(x1, y1) for x1, y1 in possible_neighbors if 
      1 <= x1 <= cave_size and 1 <= y1 <= cave_size]

# Explores the cave and wins if finds the gold
def play(world):
  agent = WumpusWorldAgent(world.size)
  location = 1, 1 # The agent starts at 1, 1

  try:
    while True:
      world.perceive(location, agent.KB)
      x ,y = location
      location = agent.choose_location(x , y, world.size)
      print(f"the next location chosen by the agent:{location}")
  except inference.GameOver as e:
    print("RESULT_WIN: You have won!, RESULT_DEATH: You have died :(, RESULT_GIVE_UP: You have left the cave without finding the gold :(")
    print(e.result)

def main(): 
  # Play a world with no Wumpus
  play(World(4, (2, 3), ((3, 1), (3, 3), (4, 4)), (-1, -1)))

  # Play a world with a Wumpus
  play(World(4, (2, 3), ((3, 1), (3, 3), (4, 4)), (1, 3)))
  # Feel free to make up additional worlds and see how your agent does at exploring them!

if __name__ == '__main__':
  main()
