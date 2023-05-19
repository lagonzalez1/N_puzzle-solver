import copy

# ENUMS
UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3


class NPuzzle:
    """
    Class representing an Npuzzle.

    Puzzle is of size (size x size), with numbers 1 to N
    A solved puzzle has these numbers in ascending order
    # from left to right, top to bottom.
    0 represents the empty space, in a solved puzzle it is at the bottom right.

    Takes size as an initializtion argument.
    """
    def __init__(self, size):
        self.size = size
        self.puzzle = [[(j*size)+i+1 for i in range(size)] for j in range(size)]
        self.puzzle[size-1][size-1] = 0
        self.zero = (size - 1, size - 1)

    def read_puzzle(self, filename):
        """
        Helper to read a puzzle from a file.

        Arguments:
            filename: Name of file to read from.
        """
        file = open(filename, "r")
        row = 0
        for line in file:
            column = 0
            for i in line.split(" "):
                i = i.strip()
                if not i:
                    # Skip extra whitespace
                    continue
                self.puzzle[row][column] = int(i)
                if i == '0':
                    self.zero = (row, column)
                column = column + 1
            row = row + 1
        assert self.puzzle[self.zero[0]][self.zero[1]] == 0

    # Swap the contents of 2 cells
    def swap(self, x1, y1, x2, y2):
        """
        Helper function to swap the positions of 2 cells.

        Arguments:
            x1: X position of cell 1
            x2: X position of cell 2
            y1: Y position of cell 1
            y2: Y position of cell 2
        """
        temp = self.puzzle[x1][y1]
        self.puzzle[x1][y1] = self.puzzle[x2][y2]
        self.puzzle[x2][y2] = temp
        if self.puzzle[x1][y1] == 0:
            self.zero = (x1, y1)
        if self.puzzle[x2][y2] == 0:
            self.zero = (x2, y2)

    def print_puzzle(self):
        """
        Helper function to print current puzzle state.

        """
        for i in range(self.size):
            line = ""
            for j in range(self.size):
                line = line + "\t" + str(self.puzzle[i][j])
            print(line)
        print("")

    def check_puzzle(self):
        """
        Helper function to evaluate if the puzzle is solved.

        Returns:
            True if the puzzle is currently solved.
            False otherwise.

        """
        check = 1
        for i in range(self.size):
            for j in range(self.size):
                if i == self.size - 1 and j == self.size - 1:
                    return self.puzzle[i][j] == 0
                if self.puzzle[i][j] != check:
                    return False
                check = check + 1
        return True


class Node:
    """
    Class representing a Search Node.
    Tracks:
        a puzzle state,
        a parent node,
        the depth of the current node,
        and the moves taken on this path so far
    """
    def __init__(self, puzzle: NPuzzle, parent=None, move=None):
        self.state = copy.deepcopy(puzzle)
        self.parent = parent
        if parent is None:
            self.depth = 0
            self.moves = []
        else:
            self.depth = parent.depth+1
            self.moves = copy.deepcopy(parent.moves)
        if move is not None:
            self.moves.append(move)

    def print_moves(self):
        """
        Helper function to print current Node mooves.

        """
        move_string = " "
        if len(self.moves) == 0:
            return
        for move in self.moves:
            if move == UP:
                move_string = move_string + "U "
            elif move == LEFT:
                move_string = move_string + "L "
            elif move == DOWN:
                move_string = move_string + "D "
            elif move == RIGHT:
                move_string = move_string + "R "
            else:
                move_string = move_string + "INVALID "
        print(move_string)

    def print_puzzle(self):
        self.state.print_puzzle()
