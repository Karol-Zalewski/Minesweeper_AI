import random
from MinesweeperAI import Sentence, MinesweeperAI

class Board:
    def __init__(self, size, num_bombs):
        self.size = size
        self.num_bombs = num_bombs
        self.board = self.make_board()
        self.dug = set()
        self.ai = MinesweeperAI(size)



    def make_board(self):
        '''Creates the dictionary which is the representation of the board state
        '''
        board = {
            (row,col):None
            for row in range(self.size)
            for col in range(self.size)
        }

        # Plants the bomb
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
        
            random_row = random.randint(0, self.size - 1)
            random_col = random.randint(0, self.size - 1)

            if board[(random_row,random_col)] is None:
                board[(random_row,random_col)] = '*'
                bombs_planted += 1

        # For the locations without the bomb assign the value representing the number of the nearby bombs
        for row in range(self.size):
            for col in range(self.size):

                if board[(row,col)] is None:

                    bomb_count = 0

                    for r in range(row-1, row+2):
                        for c in range(col-1, col+2):

                            if (r,c) in board and board[(r,c)] == '*':
                                
                                bomb_count +=1
                
                    board[(row,col)] = bomb_count
        
        return board
    
    def dig(self, row, col):
        ''' Adds the field to the dug set and checks if it is a bomb
        '''
        self.dug.add((row,col))
        
        # If it is a bomb return False
        if self.board[(row,col)] == '*':
            return False

        # If it is not a bomb return True and if it is zero automatically dig nearby fields
        elif self.board[(row,col)] > 0:
            self.ai.add_knowledge((row, col), self.board[(row, col)])
            return True
        
        elif self.board[(row,col)] == 0:
            for r in range(row-1, row+2):
                for c in range(col-1, col+2):
                    if (r,c) in self.board and (r,c) not in self.dug:
                        self.dig(r,c)
            self.ai.add_knowledge((row, col), self.board[(row, col)])
            return True
        
    def ask(self):
        ''' Ask for an input from the user and proceed accordingly
        '''
        print(self)
        if 'a' == input("If you want an AI to make a move enter 'a', if not press enter. ").lower():
            row ,col = self.ai.make_safe_move()
            if row is not None:
                print(f"AI makes safe move to {row}, {col}")
                return row, col
            else:
                row, col = self.ai.make_random_move()
                print(f"AI makes random move to {row}, {col}")
                return row, col

        else:
            try:
                row_choice = int(input('In what row would you like to dig?\n'))
                col_choice = int(input('In what column would you like to dig?\n'))
                if (row_choice,col_choice) not in self.board or (row_choice,col_choice) in self.dug:
                    print('Wrong choice. Try again.')
                    self.ask()
            except ValueError:
                print('Wrong choice. Try again. ')
                self.ask()
            
            return row_choice, col_choice
        

    
    def __str__(self):
        shown_board = dict()
        for row in range(self.size):
            for col in range(self.size):

                if (row,col) in self.dug:
                    shown_board[(row,col)] = f'|{self.board[(row,col)]}|'

                else:
                    shown_board[(row,col)] = '|_|'

        print_board = ' '
        for col in range(self.size):
            print_board = print_board + f' {col} '
        for row in range(self.size):
            print_board = print_board + f'\n{row}'
            for col in range(self.size):
                print_board = print_board + f'{shown_board[(row,col)]}'
        
        return print_board

def play(size=10,num_bombs=10):
    board = Board(size, num_bombs)
    safe = True
    while safe and len(board.board) > len(board.dug) + num_bombs:
    
        row,col = board.ask()
        safe = board.dig(row,col)
    print(board)
    if safe:
        print('Gratulation, you have won! ')
    else:
        print('Unfortunately you lose. ')

if __name__ == '__main__':
    play()


    


