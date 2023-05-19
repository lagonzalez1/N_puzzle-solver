from helpers import Node, NPuzzle, LEFT, RIGHT, UP, DOWN
import copy
import heapq


# Track the move and puzzle states.
def puzzle_move(puzzle, move, parent_node):
    pos_x, pos_y = puzzle.zero
    max_x = len(puzzle.puzzle) - 1
    max_y = len(puzzle.puzzle[0]) - 1

    if move == "UP":
        x = pos_x - 1
        y = pos_y
        if x <= max_x and x >= 0:
            new_node = Node(puzzle=puzzle, parent=parent_node, move=UP)
            new_node.state.swap(pos_x, pos_y, x, y)
            return new_node, UP
        else:
            return None, None
    elif move == "DOWN":
        x = pos_x + 1
        y = pos_y
        if x <= max_x and x >= 0:
            new_node = Node(puzzle=puzzle, parent=parent_node, move=DOWN)
            new_node.state.swap(pos_x, pos_y, x, y)
            return new_node, DOWN
        else:
            return None, None
    elif move == "RIGHT":
        x = pos_x
        y = pos_y + 1
        if y <= max_y and y >= 0:
            new_node = Node(puzzle=puzzle, parent=parent_node, move=RIGHT)
            new_node.state.swap(pos_x, pos_y, x, y)
            return new_node, RIGHT
        else:
            return None, None
    elif move == "LEFT":
        x = pos_x
        y = pos_y - 1
        if y <= max_y and y >= 0:
            new_node = Node(puzzle=puzzle, parent=parent_node, move=LEFT)
            new_node.state.swap(pos_x, pos_y, x, y)
            return new_node, LEFT
        else:
            return None, None
    else:
        print("Error")
        return None, None


def goalState(size):
    goal = [[(j*size)+i+1 for i in range(size)] for j in range(size)]
    goal[size-1][size-1] = 0
    return goal


# Param: Node
# Returns F(n) = G(n) + H(n)
def calculateCost(node):
    goal = goalState(node.state.size) 
    cost = 0
    for i in range(node.state.size):
        for j in range(node.state.size):
            if node.state.puzzle[i][j] == goal[i][j]:
                continue
            else:
                cost = cost + 1
    return cost + node.depth


def decreaseDoubleKey(node):
    return calculateCostTaxicab(node) + node.depth - 1

def calculateCostTaxicab(node):
    goal = goalState(node.state.size)
    wrong = [] # list of misplaced numbers
    positions = []
    d = []
    sum = 0
    for i in range(node.state.size) :
        for j in range(node.state.size) :
            if node.state.puzzle[i][j] == goal[i][j]:
                continue
            else:
                wrong.append(node.state.puzzle[i][j])
                positions.append((i,j)) #position of wrong node

    for i in range(node.state.size):
        for k in range(node.state.size):
            iter = 0
            for li in range(len(wrong) -1):
                iter += 1
                if wrong[li] == goal[i][k]:
                    x = positions[iter][0]
                    y = positions[iter][1]
                    sum += abs(x - i) + abs(y - k)
                else:
                    continue
                                      
    return sum + node.depth


def decreaseKey(node):
    goal = [[1,2,3], [4,5,6], [7,8,0]]
    cost = 0
    for i in node.state:
        for j in node.state[0]:
            if node.state[i][j] == goal[i][j]:
                continue
            else:
                cost += 1


    return cost + node.depth - 1



def findNodeInFrontier(node, frontier):
    found = False
    for i in frontier:
        if i[1].state == node.state:
            found = True
            break

    return found

depthLimit = 8

def BFS(puzzle):
    """
    Breadth-First Search.

    Arguments:
    - puzzle: Node object representing initial state of the puzzle

    Return:
    states_searched: An ordered list of all states searched.
    final_solution: An ordered list of moves representing the final solution.
    """

    possible_moves = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    states_searched = [Node(puzzle)]
    visited = []

    final_solution = []

    while states_searched:
        node = states_searched.pop(0)
        if node.state in visited:
            continue

        visited.append(node.state) # appending the puzzle not the node
        if node.state.check_puzzle():
            states_searched.append(node)
            final_solution = node.moves
            break
        puzz = copy.deepcopy(node.state)
        for move in possible_moves:
            leaf, m = puzzle_move(puzz, move, node)
            if leaf is None or m is None: # if the move is not avaialble then move to next iteration
                continue
            if leaf.state in visited or leaf in states_searched:
                continue
            else:
                states_searched.append(leaf)
    # TODO: WRITE CODE

    return states_searched, final_solution


def DFS(puzzle):
    """
    Depth-First Search.

    Arguments:
    - puzzle: Node object representing initial state of the puzzle

    Return:
    states_searched: An ordered list of all states searched.
    final_solution: An ordered list of moves representing the final solution.
    This goes on forever
    """

    possible_moves = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    states_searched = [Node(puzzle)]
    visited = []
    final_solution = []
    max_depth = 5
    while states_searched:
        node = states_searched.pop(0)
        if node.depth >= max_depth:
            return states_searched, final_solution
        if node.state in visited:
            continue
        visited.append(node.state) # appending the puzzle not the node
        if node.state.check_puzzle():
            states_searched.append(node)
            final_solution = node.moves
            return states_searched, final_solution

        puzz = copy.deepcopy(node.state)
        for move in possible_moves:
            leaf, m = puzzle_move(puzz, move, node)
            if leaf is None or m is None: # if the move is not avaialble then move to next iteration
                continue
            if leaf.state not in visited or leaf not in states_searched:
                states_searched.insert(0,leaf)
                continue

    # TODO: WRITE CODE
    return states_searched, final_solution





# Hamming distance/misplaced tiles
# Just as the name suggests, this heuristics returns
# the number of tiles that are not in their final position. Let’s take this puzzle instance.

def A_Star_H1(puzzle):
    """
    A-Star with Heuristic 1

    Arguments:
    - puzzle: Node object representing initial state of the puzzle

    Return:
    states_searched: An ordered list of all states searched.
    final_solution: An ordered list of moves representing the final solution.
    """
    possible_moves = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    states_searched = [(0, Node(puzzle))]
    visited = []
    final_solution = []

    while states_searched:
        states_searched.sort(key=lambda y: y[0])

        node = states_searched.pop(0)

        if node[1] in visited:
            continue

        visited.append(node[1].state)  
        
        if node[1].state.check_puzzle():
            states_searched.append(node[1])
            final_solution = node[1].moves
            break
        puzz = copy.deepcopy(node[1].state)

        for move in possible_moves:
            leaf, m = puzzle_move(puzz, move, node[1])

            if leaf is None or m is None:
                continue
            if leaf.state not in visited :
                cost = calculateCost(leaf)
                states_searched.append( (cost, leaf) )
                continue
        
        

    # TODO: WRITE CODE

    return states_searched, final_solution


# Manhattan Distance/Taxicab gemoetry
# Find the misplaced numbers then calculate the distance from the correct square
# Manhattan Distance of a tile is the distance or the number of slides/tiles away it is 
# from it’s goal state.Thus, for a certain state the Manhattan distance will be the sum of 
# the Manhattan distances of all the tiles except the blank tile.


def A_Star_H2(puzzle):
    """
    A-Star with Heauristic 2

    Arguments:
    - puzzle: Node object representing initial state of the puzzle

    Return:
    states_searched: An ordered list of all states searched.
    final_solution: An ordered list of moves representing the final solution.
    """

    possible_moves = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    states_searched = [(0, Node(puzzle))]
    visited = []
    final_solution = []

    while states_searched:
        states_searched.sort(key=lambda y: y[0])
        node = states_searched.pop(0)

        if node[1] in visited:
            continue

        visited.append(node[1].state)  
        
        if node[1].state.check_puzzle():
            states_searched.append(node[1])
            final_solution = node[1].moves
            break
        puzz = copy.deepcopy(node[1].state)

        for move in possible_moves:
            leaf, m = puzzle_move(puzz, move, node[1])

            if leaf is None or m is None:
                continue
            if leaf.state not in visited :
                cost = calculateCostTaxicab(leaf)
                states_searched.append( (cost, leaf) )
                continue
            else :
                continue

            
        
        

    # TODO: WRITE CODE

    return states_searched, final_solution