
# coding: utf-8

# ## Solving Normal Form Games

# In[1]:

from collections import deque


# **compare_two**
# 
# This function compares two choices for a player in the SED methodology. Returns one of the choices indexes or a -1 if no dominating solution. It examines the options via index of the game board.
# 
# ###### Parameters
#     *game* Represents game world
#     *weak* Boolean on whether to consider weakly dominated strategies
#     *player* 0 to represent player 1 and 1 to represent player 2
#     *choice1* First strategy to consider for comparison
#     *choice2* Second strategy to consider for comparison
#     *opponent_strategies* The current opponent strategies still available

# In[2]:

def compare_two(game, weak, player, choice1, choice2, opponent_strategies): 
    choice1_payoff = 0;
    choice2_payoff = 0;
    total = len(opponent_strategies);
    
    for opponent_strat in opponent_strategies:
        if(player == 0):
            c = int(game[choice1][opponent_strat][player]);
            d = int(game[choice2][opponent_strat][player]);
        elif(player == 1):
            c = int(game[opponent_strat][choice1][player]);
            d = int(game[opponent_strat][choice2][player]);
        if(c-d > 0):
            choice1_payoff += 1;
        elif(c-d < 0):
            choice2_payoff += 1;
    
    if(choice1_payoff == total or (weak and choice1_payoff > 0 and choice2_payoff == 0)):
        return choice1;
    elif(choice2_payoff == total or (weak and choice2_payoff > 0 and choice1_payoff == 0)):
        return choice2;
        
    return -1;


# **create_initial**
# 
# This function creates a initial set of indices for a particular player in a game. It is implemented for use as a FIFO queue.
# 
# ###### Parameters
#     *game* Represents game payoffs for each player choice
#     *player* 0 to represent player 1 and 1 to represent player 2

# In[3]:

def create_initial(game, player):  
    queue = deque();
    if(player == 0):
        for i in range(len(game)):
            queue.append(i);
    elif(player == 1):
        for i in range(len(game[0])):
            queue.append(i);
    return queue;


# 
# ---

# **solve_game**
# 
# This function uses Successive Elimination of Dominated Strategies (SEDS) to find the **pure strategy** Nash Equilibrium of a Normal Form Game. If a dominate strategy is found, it is returned; otherwise, this function returns "None." If the second parameter is False, this function will consider weakly dominate solutions; otherwise it will only report strongly dominate solutions.
# 
# It is implemented so that a set with elements representing each strategy is created for each player. These sets are examined via the SED method to systematically take 2 strategies from sets, comparing payoff depending on the remaining opponent strategies to find dominating stratgies. This loop switches between the first and second player until find solution or determine none exist.
# 
# Returns returns strategy indices of Nash equilibrium or None.
# 
# ###### Parameters
#     *game* Represents game payoffs for each player choice
#     *weak* Boolean on whether to consider weakly dominated strategies with False default

# In[4]:

def solve_game(game, weak=False):   
    player = 1;
    playerOther = 0;
    numberOfToggles = 3;

    strategies = [create_initial(game, player), create_initial(game, playerOther)];
    
    for i in range(numberOfToggles):
        for j in range(len(strategies[player]) - 1):
            choice1 = strategies[player].popleft();
            choice2 = strategies[player].popleft();

            ans = compare_two(game, weak, player, choice1, choice2, strategies[playerOther]);
        
            if(ans == -1):
                strategies[player].append(choice1);
                strategies[player].append(choice2);
            else:
                strategies[player].append(ans);
            
        player = (player + 1) % 2;
        playerOther = (playerOther + 1) % 2;
        
        if(len(strategies[player]) == 1 and len(strategies[playerOther]) == 1):
            ans1 = strategies[player].pop();
            ans2 = strategies[playerOther].pop();
            return (ans1,ans2);
        
    return None;


# ### Test Game 1. Create a 3x3 two player game
# 
# **that can only be solved using the Successive Elimintation of Strongly Dominated Strategies**
# 
# Player 1 / Player 2  | 0 | 1 | 2
# ---- | ---- | ----
# 0  | 2, 4 | 8, 6 | 8, 10
# 1  | 6, 8 | 12, 12 | 16, 10
# 2  | 10, 8 | 10, 12 | 14, 14
# 
# **Solution:** (1,1)

# In[5]:

# A game that can be solved by Successive Elimination of STRONGLY Dominated Strategies of at least 3x3

test_game_1 = [
 [( 2, 4), (8, 6), (8, 10)],
 [(6, 8), (12, 12), (16, 8)],
 [(10, 8), (10, 12), (14, 14)]];

solution = solve_game( test_game_1)


# In[6]:

assert solution == (1,1) # insert your solution from above.


# ### Test Game 2. Create a 3x3 two player game
# 
# **that can only be solved using the Successive Elimintation of Weakly Dominated Strategies**
# 
# Player 1 / Player 2  | 0 | 1 | 2
# ---- | ---- | ----
# 0  | 4, 4 | 6, 4 | 6, 2
# 1  | 4, 6 | 8, 10 | 12, 2
# 2  | 2, 6 | 4, 12 | 10, 10
# 
# **Solution:** (1,1)

# In[7]:

test_game_2 = [
 [(4, 4), (6, 4), (6, 2)],
 [(4, 6), (8, 10), (12, 2)],
 [(2, 6), (4, 12), (10, 10)]];

strong_solution = solve_game( test_game_2)
weak_solution = solve_game( test_game_2, weak=True)


# In[8]:

assert strong_solution == None
assert weak_solution == (1,1) # insert your solution from above.


# ### Test Game 3. Create a 3x3 two player game
# 
# **that cannot be solved using the Successive Elimintation of Dominated Strategies at all**
# 
# Player 1 / Player 2  | 0 | 1 | 2
# ---- | ---- | ----
# 0  | 2, 2 | 4, 4 | 2, 2
# 1  | 4, 2 | 2, 2 | 2, 2
# 2  | 2, 2 | 4, 4 | 4, 2
# 
# **Solution:** None

# In[9]:

test_game_3 = [
 [(2, 2), (4, 4), (2, 2)],
 [(4, 2), (2, 2), (2, 2)],
 [(2, 2), (4, 4), (4, 2)]];

strong_solution = solve_game(test_game_3)
weak_solution = solve_game(test_game_3, weak=True)


# In[10]:

assert strong_solution == None
assert weak_solution == None


# In[ ]:



