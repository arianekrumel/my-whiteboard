
# coding: utf-8

# # State Space Search with A* Search

# ## The World
# 
# Given a map like the one above, we can easily represent each row as a `List` and the entire map as `List of Lists`:

# In[169]:

full_world = [
  ['.', '.', '.', '.', '.', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], 
  ['.', '.', '.', '.', '.', '.', '.', '*', '*', '*', '*', '*', '*', '*', '*', '*', '.', '.', 'x', 'x', 'x', 'x', 'x', 'x', 'x', '.', '.'], 
  ['.', '.', '.', '.', 'x', 'x', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', 'x', 'x', 'x', '#', '#', '#', 'x', 'x', '#', '#'], 
  ['.', '.', '.', '.', '#', 'x', 'x', 'x', '*', '*', '*', '*', '~', '~', '*', '*', '*', '*', '*', '.', '.', '#', '#', 'x', 'x', '#', '.'], 
  ['.', '.', '.', '#', '#', 'x', 'x', '*', '*', '.', '.', '~', '~', '~', '~', '*', '*', '*', '.', '.', '.', '#', 'x', 'x', 'x', '#', '.'], 
  ['.', '#', '#', '#', 'x', 'x', '#', '#', '.', '.', '.', '.', '~', '~', '~', '~', '~', '.', '.', '.', '.', '.', '#', 'x', '#', '.', '.'], 
  ['.', '#', '#', 'x', 'x', '#', '#', '.', '.', '.', '.', '#', 'x', 'x', 'x', '~', '~', '~', '.', '.', '.', '.', '.', '#', '.', '.', '.'], 
  ['.', '.', '#', '#', '#', '#', '#', '.', '.', '.', '.', '.', '.', '#', 'x', 'x', 'x', '~', '~', '~', '.', '.', '#', '#', '#', '.', '.'], 
  ['.', '.', '.', '#', '#', '#', '.', '.', '.', '.', '.', '.', '#', '#', 'x', 'x', '.', '~', '~', '.', '.', '#', '#', '#', '.', '.', '.'], 
  ['.', '.', '.', '~', '~', '~', '.', '.', '#', '#', '#', 'x', 'x', 'x', 'x', '.', '.', '.', '~', '.', '#', '#', '#', '.', '.', '.', '.'], 
  ['.', '.', '~', '~', '~', '~', '~', '.', '#', '#', 'x', 'x', 'x', '#', '.', '.', '.', '.', '.', '#', 'x', 'x', 'x', '#', '.', '.', '.'], 
  ['.', '~', '~', '~', '~', '~', '.', '.', '#', 'x', 'x', '#', '.', '.', '.', '.', '~', '~', '.', '.', '#', 'x', 'x', '#', '.', '.', '.'], 
  ['~', '~', '~', '~', '~', '.', '.', '#', '#', 'x', 'x', '#', '.', '~', '~', '~', '~', '.', '.', '.', '#', 'x', '#', '.', '.', '.', '.'], 
  ['.', '~', '~', '~', '~', '.', '.', '#', '*', '*', '#', '.', '.', '.', '.', '~', '~', '~', '~', '.', '.', '#', '.', '.', '.', '.', '.'], 
  ['.', '.', '.', '.', 'x', '.', '.', '*', '*', '*', '*', '#', '#', '#', '#', '.', '~', '~', '~', '.', '.', '#', 'x', '#', '.', '.', '.'], 
  ['.', '.', '.', 'x', 'x', 'x', '*', '*', '*', '*', '*', '*', 'x', 'x', 'x', '#', '#', '.', '~', '.', '#', 'x', 'x', '#', '.', '.', '.'], 
  ['.', '.', 'x', 'x', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', 'x', 'x', 'x', '.', '.', 'x', 'x', 'x', '.', '.', '.', '.', '.'], 
  ['.', '.', '.', 'x', 'x', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', 'x', 'x', 'x', 'x', '.', '.', '.', '.', '.', '.', '.'], 
  ['.', '.', '.', 'x', 'x', 'x', '*', '*', '*', '*', '*', '*', '*', '*', '.', '.', '.', '#', '#', '.', '.', '.', '.', '.', '.', '.', '.'], 
  ['.', '.', '.', '.', 'x', 'x', 'x', '*', '*', '*', '*', '*', '*', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '~', '~', '~', '~'], 
  ['.', '.', '#', '#', '#', '#', 'x', 'x', '*', '*', '*', '*', '*', '.', 'x', '.', '.', '.', '.', '.', '~', '~', '~', '~', '~', '~', '~'], 
  ['.', '.', '.', '.', '#', '#', '#', 'x', 'x', 'x', '*', '*', 'x', 'x', '.', '.', '.', '.', '.', '.', '~', '~', '~', '~', '~', '~', '~'], 
  ['.', '.', '.', '.', '.', '.', '#', '#', '#', 'x', 'x', 'x', 'x', '.', '.', '.', '.', '#', '#', '.', '.', '~', '~', '~', '~', '~', '~'], 
  ['.', '#', '#', '.', '.', '#', '#', '#', '#', '#', '.', '.', '.', '.', '.', '#', '#', 'x', 'x', '#', '#', '.', '~', '~', '~', '~', '~'], 
  ['#', 'x', '#', '#', '#', '#', '.', '.', '.', '.', '.', 'x', 'x', 'x', '#', '#', 'x', 'x', '.', 'x', 'x', '#', '#', '~', '~', '~', '~'], 
  ['#', 'x', 'x', 'x', '#', '.', '.', '.', '.', '.', '#', '#', 'x', 'x', 'x', 'x', '#', '#', '#', '#', 'x', 'x', 'x', '~', '~', '~', '~'], 
  ['#', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#', '#', '#', '#', '#', '.', '.', '.', '.', '#', '#', '#', '.', '.', '.']]


# In[170]:

test_world = [
  ['.', '*', '*', '*', '*', '*', '*'],
  ['.', '*', '*', '*', '*', '*', '*'],
  ['.', '*', '*', '*', '*', '*', '*'],
  ['.', '.', '.', '.', '.', '.', '.'],
  ['*', '*', '*', '*', '*', '*', '.'],
  ['*', '*', '*', '*', '*', '*', '.'],
  ['*', '*', '*', '*', '*', '*', '.'],
]


# ## States and State Representation
# 
# The canonical pieces of a State Space Search problem are the States, Actions, Transitions and Costs. 
# 
# We'll start with the state representation. For the navigation problem, a state is the current position of the agent, `(x,y)`. The entire set of possible states is implicitly represented by the world map.

# ## Actions and Transitions
# 
# Actions are given by a movement model. One is given below but can be changed for different assumptions.
# 

# In[171]:

cardinal_moves = [(0,-1), (1,0), (0,1), (-1,0)]


# ## Costs
# 
# We can encode the costs described in a `Dict`. One is given below but can be changed for different assumptions.
# 
# ```
# token   terrain    cost 
# .       plains     1
# *       forest     3
# #       hills      5
# ~       swamp      7
# x       mountains  impassible
# ```

# In[172]:

costs = { '.': 1, '*': 3, '#': 5, '~': 7}


# ## A\* Search Implementation

# ## Helper Functions
# 
# 
# **retrieveBest**
# 
# Retrieves the best candidate from the frontier.
# 
# This function loops through all nodes in the frontier and returns a tuple of the candidate with the lowest f(n) = g(n) + h(n); g(n) is the cost of the step so far and h(n) is determined by the heuristic. This function removes the chosen tuple from the frontier.

# In[173]:

def retrieveBest(frontier, costs, heuristic):
    bestStats = frontier[frontier.keys()[0]];
    for candidate in frontier:
        existingF = bestStats['g'] + bestStats['h'];
        candidateF = frontier[candidate]['g'] + frontier[candidate]['h'];
        if(candidateF < existingF):
            bestStats = frontier[candidate];
            
    best = frontier.pop(bestStats['value'], None);
    return best;


# **successors**
# 
# Retrieves a valid child, if any, of current position in world given a particular movement.
# 
# This function returns a tuple, or a 0 integer if the potential child is invalid. Children can be invalid if the move is not legal in the world, it has already been explored or the next step is impassable (mountain).

# In[174]:

def successor(world, current, move, explored,currentAllStats, goal):
    col = current[0] + move[0];
    row = current[1] + move[1];
    child = (col, row);
    
    if(row<0 or row>(len(world)-1)):
        return 0;
    elif(col < 0 or col>(len(world[row]) - 1)):
        return 0;
    elif(child in explored):
        return 0;
    elif(world[child[1]][child[0]] == "x"):
        return 0;
    else:
        childType = world[child[1]][child[0]];
        childCost = costs[childType];
        g = currentAllStats['g'] + childCost;
        h = heuristic(world, goal, child);
        return {"value":(col, row), "g": g, "h": h};
    
    


# **create_path** 
# 
# Create the optimal path given explored set, start and goal.
# 
# This function traces back from the goal to the start using the explored set from the search algorithm.

# In[175]:

def create_path(explored, start, goal):
    path = [];
    parent = explored[goal]["parent"];
    move = explored[goal]["move"];
    path.append(move);
            
    while parent != start:
        current = parent;
        parent = explored[current]["parent"];
        move = explored[current]["move"];
        path.append(move);
            
    path = path[::-1];
    return path;


# **a_star_search**
# 
# The `a_star_search` function uses the A\* Search algorithm to solve a navigational problem for an agent in a grid world. It calculates a path from the start state to the goal state and returns the actions required to get from the start to the goal.
# 
# * **world** is the starting state representation for a navigation problem.
# * **start** is the starting location, `(x, y)`.
# * **goal** is the desired end position, `(x, y)`.
# * **costs** is a `Dict` of costs for each type of terrain.
# * **moves** is the legal movement model expressed in offsets.
# * **heuristic** is a heuristic function that returns an estimate of the total cost $f(x)$ from the start to the goal through the current node, $x$. The heuristic function might change with the movement model.
# 
# The function returns the offsets needed to get from start state to the goal as a `List`. For example, for the test world:
# 
# ```
#   ['.', '*', '*', '*', '*', '*', '*'],
#   ['.', '*', '*', '*', '*', '*', '*'],
#   ['.', '*', '*', '*', '*', '*', '*'],
#   ['.', '.', '.', '.', '.', '.', '.'],
#   ['*', '*', '*', '*', '*', '*', '.'],
#   ['*', '*', '*', '*', '*', '*', '.'],
#   ['*', '*', '*', '*', '*', '*', '.'],
# 
# ```
# 
# it would return:
# 
# `[(0,1), (0,1), (0,1), (1,0), (1,0), (1,0), (1,0), (1,0), (1,0), (0,1), (0,1), (0,1)]`
# 
# Do not make unwarranted assumptions. For example, do not assume the starting point is always `(0, 0)` or that the goal is always in the lower right hand corner. Do not make any assumptions about the movement model beyond the requirement that they be offsets (it could be offets of 2!).

# In[176]:

def a_star_search( world, start, goal, costs, moves, heuristic):
    frontier = {};
    g = costs[world[start[0]][start[1]]];
    h = heuristic(world, goal, start);
    frontier[start] = {'parent': start, 'g': g, 'h': h, 'value': start, 'move': (-1,-1)};
    
    explored = {};
    
    while (frontier):
        current = retrieveBest(frontier, costs, heuristic);
        
        if(current['value'] == goal):
            explored[current['value']] = current;
            path = create_path(explored, start, goal);
            return path;
        else:
            for move in moves:
                child = successor(world, current['value'], move, explored, current, goal);
                if(child):
                    frontier[child["value"]] = {'parent': current['value'], 'g': child["g"], 'h': child["h"], 'value': child["value"], 'move': move};
            
            explored[current['value']] = current;
    return;


# **pretty_print_ele**
# 
# Gets the appropriate symbol for the pretty print function representing map attributes.
# 
# Uses a elseif sequence to determine symbol character according to movement given.

# In[177]:

def pretty_print_ele(move):    
    col = move[0];
    row = move[1];
    
    if(col==1):
        symbol = ">";
    elif(col==-1):
        symbol = "^";
    elif(row==1):
        symbol = "v";
    elif(row==-1):
        symbol = "<";
    else:
        symbol = "*";
    
    return symbol;


# **pretty_print_solution**
# 
# The `pretty_print_solution` function prints an ASCII representation of the solution generated by the `a_star_search`. It uses the symbols `v`, `^`, `>`, `<` to represent actions and `G` to represent the goal. (Note the format of the output...there are no spaces, commas, or extraneous characters).
# 
# This function first loops over all the world rows and columns to fill and temporary data structure with default asterisks. Then, starting from the starting node, it follows the given path to fill in the appropriate symbols to denote the resulting path.

# In[178]:

def pretty_print_solution( world, path, start):
    pretty_world = [];
    rows = len(world);
    for row in range(rows):
        columns = len (world[row]);
        pretty_world_row = [];
        for col in range(columns):
            pretty_world_row.append("*");
        pretty_world.append(pretty_world_row);
        
    stepCol = start[0];
    stepRow = start[1];
    for move in path:
        currentStep = (stepCol, stepRow);
        stepCol += move[0];
        stepRow += move[1];
        nextStep = (stepCol, stepRow);
        pretty_world[currentStep[1]][currentStep[0]] = pretty_print_ele(move);
        
    move = path[-1];
    currentStep = (stepCol, stepRow);
    pretty_world[currentStep[1]][currentStep[0]] = "G";
    
    rows = len(pretty_world);
    for i in range(rows):
        print ''.join(map(str, pretty_world[i]))
    
    return None


# **heuristic**
# 
# Provides a heuristic, or a estimated cost to goal which is valid because it is equal to or less than the actual cost.
# 
# This function is created with the Euclidean distance formula to provide a rough estimate to goal. The arguments required are the world, goal and current node to test.

# In[179]:

# heuristic function
def heuristic(world, goal, current):
    #pass
    x = goal[0] - current[0];
    y = goal[1] - current[1];
    
    distance = (x**2+y**2)**0.5;
    return distance;


# # Execution
# 
# Executing search and print on test world and full world.

# In[180]:

test_path = a_star_search( test_world, (0, 0), (6, 6), costs, cardinal_moves, heuristic)
print test_path 


# In[181]:

pretty_print_solution( test_world, test_path, (0, 0))


# In[182]:

full_path = a_star_search( full_world, (0, 0), (26, 26), costs, cardinal_moves, heuristic)
print full_path


# In[183]:

pretty_print_solution( full_world, full_path, (0, 0))


# # Advanced/Future Work

# *This section is not required but it is well worth your time to think about the task*
# 
# Write a *general* `state_space_search` function that could solve any state space search problem using Depth First Search. One possible implementation would be to write `state_space_search` as a general higher order function that took problem specific functions for `is_goal`, `successors` and `path`. You would need a general way of dealing with states, perhaps as a `Tuple` representing the raw state and metadata: `(<state>, <metadata>)`.

# In[ ]:



