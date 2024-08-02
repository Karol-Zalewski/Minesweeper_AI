import random

class Sentence():
    """
    Logical statement about a Minesweeper game. 
    Consists of a set of board cells, and a count of the 
    numbers of those cells which are mines.
    """
    def __init__(self, cells, bombs):
        self.cells = set(cells)
        self.bombs = bombs
    
    def __eq__(self, other):
        return self.cells == other.cells and self.bombs == other.bombs
    
    def __str__(self):
        return f"{self.cells} = {self.bombs}"
    
    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.bombs and self.bombs != 0:
            return self.cells
        else:
            return set()
        
    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe
        """
        if self.bombs == 0:
            return self.cells
        else:
            return set()
        
    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.bombs -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)

class MinesweeperAI():
    """
    Minesweeper game player
    """
    def __init__(self, size):
        self.board_size = size

        self.moves_made = set()

        self.mines = set()
        self.safes = set()

        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
    
    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        """
        self.moves_made.add(cell)
        undetermined_cells = []
        mines_count = 0

        self.mark_safe(cell)

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) in self.mines:
                    mines_count += 1
                if 0 <= i < self.board_size and 0 <= j < self.board_size and (i, j) not in self.safes and (i, j) not in self.mines:
                    undetermined_cells.append((i, j))
        
        new_sentence = Sentence(undetermined_cells, count - mines_count)

        self.knowledge.append(new_sentence)

        for sentence in self.knowledge:
            if sentence.known_mines():
                for cell in sentence.known_mines().copy():
                    self.mark_mine(cell)
            if sentence.known_safes():
                for cell in sentence.known_safes().copy():
                    self.mark_safe(cell)
        
        for sentence in self.knowledge:
            if new_sentence.cells.issubset(sentence.cells) and sentence.bombs > 0 and new_sentence.bombs > 0 and new_sentence != sentence:
                new_subset = sentence.cells.difference(new_sentence.cells)
                new_subset_sentence = Sentence(list(new_subset), sentence.bombs - new_sentence.bombs)
                self.knowledge.append(new_subset_sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None, None
    
    def make_random_move(self):
        """
        Returns a move that is not known to be mine.
        """
        possible_moves = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    possible_moves.append((i, j))
        
        if len(possible_moves) != 0:
            return random.choice(possible_moves)
        
        else:
            return None, None




    