get_ipython().magic(u'matplotlib inline')

from __future__ import division

import matplotlib.pyplot as plt
import networkx as nx
import copy


# ## Constraint Satisfaction Problems: Map Coloring

connecticut = { "nodes": ["Fairfield", "Litchfield", "New Haven", "Hartford", "Middlesex", "Tolland", "New London", "Windham"],
                "edges": [(0,1), (0,2), (1,2), (1,3), (2,3), (2,4), (3,4), (3,5), (3,6), (4,6), (5,6), (5,7), (6,7)],
                "coordinates": [( 46, 52), ( 65,142), (104, 77), (123,142), (147, 85), (162,140), (197, 94), (217,146)]}
print connecticut


# The coordinates permit us to use NetworkX to draw the graph. We'll add a helper function for this, `draw_map`, which takes our planar_map, a figure size in abstract units, and a List of color assignments in the same order as the nodes in the planar_map.  The underlying drawings are made by matplotlib using NetworkX on top of it. Incidentally, the positions just make the map "work out" on NetworkX/matplotlib.
# 
# The size parameter is actually inches wide by inches tall (8, 10) is an 8x10 sheet of paper. Why doesn't a chart cover up the whole screen then? It's adjusted by dpi. On high resolution monitors, 300 dpi with 8x10 inches might only take up a fraction of that space. Use whatever you want to make the output look good. It doesn't matter for anything else but that.
# 
# A default value for `color_assignments` is provided, `None`, that simply colors all the nodes red. Otherwise, `color_assignments` must be a `List of Tuples` where each `Tuple` is a node name and assigned color. The order of `color_assignments` must be the same as the order of `"nodes"` in the `planar_map`.
def draw_map(planar_map, size, color_assignments=None):
    def as_dictionary(a_list):
        dct = {}
        for i, e in enumerate(a_list):
            dct[i] = e
        return dct
    
    G = nx.Graph()
    
    labels = as_dictionary(planar_map[ "nodes"])
    pos = as_dictionary(planar_map["coordinates"])
    
    # create a List of Nodes as indices to match the "edges" entry.
    nodes = [n for n in range(0, len(planar_map[ "nodes"]))]

    if color_assignments:
        colors = [c for n, c in color_assignments]
    else:
        colors = ['red' for c in range(0,len(planar_map[ "nodes"]))]

    G.add_nodes_from( nodes)
    G.add_edges_from( planar_map[ "edges"])

    plt.figure( figsize=size, dpi=600)

    nx.draw( G, node_color = colors, with_labels = True, labels = labels, pos = pos)


# Using this function, we can draw `connecticut`:
draw_map( connecticut, (5,4), [("Fairfield", "red"), ("Litchfield", "blue"), ("New Haven", "red"), ("Hartford", "blue"),
                               ("Middlesex", "red"), ("Tolland", "blue"), ("New London", "red"), ("Windham", "blue")])

#     backtracking: yes
#     forward checking: yes
#     minimum remaining values: yes
#     least contraining value: yes

# **isConsistent**
# 
# This function returns a boolean truth value that to represent whether or not the given node coloring in valid. It loops over all edges in the planar map to find all the edges that involve the given node and checks if the partner node has the same color. 
# 
# Returns false if there is a match and true if there is not.
def isConsistent(planar_map, domain_map, coloring, node, color, trace=False):
    for i, (a, b) in enumerate(planar_map["edges"]):
        if(a == node):
            (nameB, colorB) = coloring[b];
            if(color == colorB):
                if(trace): print "Found inconsistency with node, must backtrack", b
                return False;
        if(b == node):
            (nameA, colorA) = coloring[a];
            if(color == colorA):
                if(trace): print "Found inconsistency with node, must backtrack", a
                return False;

    return True;


# **chooseNextVariableBasic**
# 
# This function returns the index for the next node to be evaulated in teh CSP for a basic forward checking and backtracing sequence. It increments the given index.
# 
# Returns false if there is a match and true if there is not.
def chooseNextVariableBasic(planar_map, domain_map, explored, index, trace=False):
    if(trace): print "Increment index to find next node"
    return index+1;


# **chooseNextVariable**
# 
# This function returns the index for the next node to be evaulated in the CSP for minimum remaining values sequence. It loops over a map of the valid domains per node to search for the next unexplored node that has the least number of domain values.
def chooseNextVariable(planar_map, domain_map, explored, index, trace=False):    
    smallestValue = len(planar_map["nodes"]);
    smallestIndex = index;
    
    for i in range(len(domain_map)):
        if i not in explored:
            smallestValue = len(domain_map[smallestIndex]);
            thisValue = len(domain_map[i]);
                        
            if thisValue < smallestValue:
                if(trace): print "Found node with smaller domain using minimum remaining values sequence", thisValue
                smallestIndex = i;   
                
    return smallestIndex;


# **updateDomainMap**
# 
# This function updates the map of domains per node after a successful coloring. It removes the coloring from the neighbors in order to avoid matching colors. It loops over all edges in order to find the relevant nodes.
def updateDomainMap(planar_map, domain_map, node_index, color):
    numDeletes = 0;
    for i, (a, b) in enumerate(planar_map["edges"]):
        if(a == node_index):
            domainB = domain_map.pop(b);
            domainBCopy = copy.copy(domainB);
            if color in domainB:
                domainBCopy.remove(color);
                numDeletes += 1;
            domain_map.insert(b, domainBCopy);
        if(b == node_index):
            domainA = domain_map.pop(a);
            domainACopy = copy.copy(domainA);
            if color in domainA:
                domainACopy.remove(color);
                numDeletes += 1;
            domain_map.insert(a, domainACopy);
    
    return (domain_map, numDeletes);


# **chooseNextValueBasic**
# 
# This function returns the next color option in the basic order.
def chooseNextValueBasic(planar_map, domain_map, colors, i, node_index, exploredColors):    
    return colors[i];  


# **chooseNextValue**
# 
# This function returns the next color according to the least constraining value. It loops over all the neighbors to select the color, if chosen would result in the least amount of domain reduction.
def chooseNextValue(planar_map, domain_map, colors, i, node_index, exploredColors):  
    totalBest = len(colors) * len(planar_map["nodes"]);
    color = colors[i];
    
    for thisColor in colors:
        if(thisColor not in exploredColors):
            (domain_map, numDeletes) = updateDomainMap(planar_map, domain_map, node_index, thisColor);
            if(numDeletes < totalBest):
                color = thisColor
                totalBest = numDeletes;
                
    checkLoop = 0;
    while(color in exploredColors):
        color = colors[checkLoop];
        checkLoop += 1;

    return color;  


# **backtrack**
# 
# This function completes the backtracking algorithm. It receives a node of interest, then loops over all the color choices for the map to find a appropriate coloring. It has a recursive element which checks all the related nodes for valid values prior to assignment.
# 
# Returns a valid coloring map, or None if no solution found.
def backtrack(planar_map, coloring, colors, domain_map, explored, node_index=0, trace=False):
    if(trace): print "Start checking node at index", node_index
        
    if len(explored) == len(planar_map["nodes"]):
        return coloring;
    
    thisNode = planar_map["nodes"][node_index];
    
    exploredColors = [];
    for i in range(len(colors)):
        if(trace): print "Choose next color with least constraining value"
        thisColor = chooseNextValue(planar_map, domain_map, colors, i, node_index, exploredColors);
        if(trace): print "Test the following node coloring", node_index, thisColor
        exploredColors.append(thisColor);
        
        if(isConsistent(planar_map, domain_map, coloring, node_index, thisColor, trace)):    
            if(trace): print "Found consistent coloring for node ", node_index
            coloring.pop(node_index);
            coloring.insert(node_index, (thisNode, thisColor));
            
            explored.append(node_index);
            domain_map[node_index] = colors;
            
            (domain_map, numDeletes) = updateDomainMap(planar_map, domain_map, node_index, thisColor);
            
            nextIndex = chooseNextVariable(planar_map, domain_map, explored, node_index, trace);
            print "First index for search is", nextIndex;
            coloring = backtrack(planar_map, coloring, colors, domain_map, explored, nextIndex, trace);
                
            return coloring;
        
        if(trace): print "Color is inconsistent"  
        
    if(trace): print "No solution found"  
    return None;


# **color_map**
# 
# This is the main function for this assignment which uses the above helpers to color a given map. It initializes variables with initial colors and domain mapping per node.
def color_map(planar_map, colors, trace=False):
    coloring = [];
    domain_map = [];
    explored = [];

    for i in range(len(planar_map["nodes"])):
        thisNode = planar_map["nodes"][i];
        
        if(trace): print "Initialize map coloring and node domain."
        coloring.insert(i, (thisNode, "Red"));
        domain_map.insert(i, colors);
    
    nextIndex = chooseNextVariable(planar_map, domain_map, explored, 0, trace);
    coloring = backtrack(planar_map, coloring, colors, domain_map, explored, nextIndex, trace);
    
    return coloring;


# ## Problem 1. Color Connecticut Using Your Solution
connecticut_colors = color_map( connecticut, ["red", "blue", "green", "yellow"], trace=True)


# Using the "edges" list from the connecticut map, we can test to see if each pair of adjacent nodes is indeed colored differently:
edges = connecticut["edges"]
nodes = connecticut[ "nodes"]
colors = connecticut_colors
COLOR = 1

print colors

edges = connecticut["edges"]
nodes = connecticut[ "nodes"]
colors = connecticut_colors
COLOR = 1

for start, end in edges:
    try:
        assert colors[ start][COLOR] != colors[ end][COLOR]
    except AssertionError:
        print "%s and %s are adjacent but have the same color." % (nodes[ start], nodes[ end])


draw_map( connecticut, (5,4), connecticut_colors)

connecticut_colors = color_map( connecticut, ["red", "blue", "green", "purple"], trace=True)
if connecticut_colors:
    draw_map( connecticut, (5,4), connecticut_colors)


# ## Problem 2. Color Europe Using Your solution

europe = {
    "nodes":  ["Iceland", "Ireland", "United Kingdom", "Portugal", "Spain",
                 "France", "Belgium", "Netherlands", "Luxembourg", "Germany",
                 "Denmark", "Norway", "Sweden", "Finland", "Estonia",
                 "Latvia", "Lithuania", "Poland", "Czech Republic", "Austria",
                 "Liechtenstein", "Switzerland", "Italy", "Malta", "Greece",
                 "Albania", "Macedonia", "Kosovo", "Montenegro", "Bosnia Herzegovina",
                 "Serbia", "Croatia", "Slovenia", "Hungary", "Slovakia",
                 "Belarus", "Ukraine", "Moldova", "Romania", "Bulgaria",
                 "Cyprus", "Turkey", "Georgia", "Armenia", "Azerbaijan",
                 "Russia" ], 
    "edges": [(0,1), (0,2), (1,2), (2,5), (2,6), (2,7), (2,11), (3,4),
                 (4,5), (4,22), (5,6), (5,8), (5,9), (5,21), (5,22),(6,7),
                 (6,8), (6,9), (7,9), (8,9), (9,10), (9,12), (9,17), (9,18),
                 (9,19), (9,21), (10,11), (10,12), (10,17), (11,12), (11,13), (11,45), 
                 (12,13), (12,14), (12,15), (12,17), (13,14), (13,45), (14,15),
                 (14,45), (15,16), (15,35), (15,45), (16,17), (16,35), (17,18),
                 (17,34), (17,35), (17,36), (18,19), (18,34), (19,20), (19,21), 
                 (19,22), (19,32), (19,33), (19,34), (20,21), (21,22), (22,23),
                 (22,24), (22,25), (22,28), (22,29), (22,31), (22,32), (24,25),
                 (24,26), (24,39), (24,40), (24,41), (25,26), (25,27), (25,28),
                 (26,27), (26,30), (26,39), (27,28), (27,30), (28,29), (28,30),
                 (29,30), (29,31), (30,31), (30,33), (30,38), (30,39), (31,32),
                 (31,33), (32,33), (33,34), (33,36), (33,38), (34,36), (35,36),
                 (35,45), (36,37), (36,38), (36,45), (37,38), (38,39), (39,41),
                 (40,41), (41,42), (41,43), (41,44), (42,43), (42,44), (42,45),
                 (43,44), (44,45)],
    "coordinates": [( 18,147), ( 48, 83), ( 64, 90), ( 47, 28), ( 63, 34),
                   ( 78, 55), ( 82, 74), ( 84, 80), ( 82, 69), (100, 78),
                   ( 94, 97), (110,162), (116,144), (143,149), (140,111),
                   (137,102), (136, 95), (122, 78), (110, 67), (112, 60),
                   ( 98, 59), ( 93, 55), (102, 35), (108, 14), (130, 22),
                   (125, 32), (128, 37), (127, 40), (122, 42), (118, 47),
                   (127, 48), (116, 53), (111, 54), (122, 57), (124, 65),
                   (146, 87), (158, 65), (148, 57), (138, 54), (137, 41),
                   (160, 13), (168, 29), (189, 39), (194, 32), (202, 33),
                   (191,118)]}
print europe


draw_map( europe, (10, 8))

europe_colors = color_map( europe, ["red", "blue", "green", "yellow"], trace=True)


# Here we're testing to see if the adjacent nodes are colored differently:


edges = europe["edges"]
nodes = europe[ "nodes"]
colors = europe_colors
COLOR = 1

europe_colors = color_map( europe, ["red", "blue", "green"], trace=True)
if europe_colors:
     draw_map( europe, (10,8), europe_colors)