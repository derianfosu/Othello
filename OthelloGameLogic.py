#Fransiskus Derian 82691258. ICS 32 Project 4


#'''Classes that catches all the errors'''
class OthelloInvalidMoveError(Exception):
    pass
    
class OthelloGameOver(Exception):
    pass

#The Game

class OthelloGame:
    def __init__(self, rows: int, columns: int, topLeft: 'str', firstPlayer: 'str', winnerMethod: 'str'):
        self._BOARD_ROWS = rows
        self._BOARD_COLUMNS = columns
        self._black = 'B'
        self._white = 'W'
        self._topLeft = topLeft
        self._turn = firstPlayer.upper()
        self._whoWins = winnerMethod
        

        self._board = self._new_board()
        self._board = self._starting_board()
        self._blackPass = False
        self._whitePass = False
        


    def place_disc(self, specifiedRow: int, specifiedColumn: int) -> None:
        ''' Takes the specified row and column as the parameters, and check
        if the row and column are a valid coordinate and place the disc at
        the specified row and column. It changes the color of the current turn '''

        self._require_valid_col_num(specifiedColumn)
        self._require_valid_row_num(specifiedRow)
        self._require_game_not_over()
        
        if self._valid_coord(specifiedRow, specifiedColumn) and self._board[specifiedRow][specifiedColumn] == 0:
            self._board[specifiedRow][specifiedColumn] = self._turn
            self._flip_coords(self._flip_list(specifiedRow, specifiedColumn))
            
        self._turn = self.opposite_turn()

    def print_score(self)-> None:
        ''' Prints the current score of the game'''
        print("White: {}          Black: {}"
              .format(self.count_white(),
                      self.count_black()))
    
    def winning_player(self) -> 'winner':
        ''' Returns the winner of the game once the winning condition is True'''
        winner = None
        if self._winning_condition():
            if self._whoWins == 'MOST':  
                if self.count_black() < self.count_white():
                    winner = "The Winner is White!"
                elif self.count_black() > self.count_white():
                    winner = "The Winner is Black!"
                else:
                    winner = "The game is tie! "
            elif self._whoWins == 'LEAST':  
                if self.count_black() > self.count_white():
                    winner = "The Winner is White!"
                elif self.count_black() < self.count_white():
                    winner = "The Winner is Black!"
                else:
                    winner = "The game is tie! "
        return winner

    def is_legal_move(self, row:int, col:int) -> bool:
        ''' check if the specified row and column are a legal move, it returns
        True or False'''
        if self._flip_list(row, col) != [] and self._board[row][col] == 0:
            return True
        else:
            return False

    def opposite_turn(self)->'turn':
        ''' Change the color of the turn, if it's black, then change it
        into white, and if it's white, change it into black'''
        if self._turn == self._black:
            return self._white
        else:
            return self._black

    def black_pass(self)->bool:
        ''' check if black can not make any move and it has to pass its turn'''
        if self._turn == self._black and not self._at_least_one_move():
            self._blackPass = True
            self._turn = self.opposite_turn()
            return True
        self._blackPass = False
        return False

    def white_pass(self)->bool:
        ''' check if white can not make any move and it has to pass its turn'''
        if self._turn == self._white and not self._at_least_one_move():
            self._whitePass = True
            self._turn = self.opposite_turn()
            return True
        self._whitePass = False
        return False

    def _starting_board(self)->[[int and str]]:
        ''' returns a board with four discs in the middle of the board, and
        make the one at the top left of those four discs based on the user input'''
        if self._topLeft == self._white:
            self._board[int((self._BOARD_ROWS/2)-1)][int((self._BOARD_COLUMNS/2)-1)] = self._white
            self._board[int(self._BOARD_ROWS/2)][int(self._BOARD_COLUMNS/2)] = self._white
            self._board[int((self._BOARD_ROWS/2)-1)][int(self._BOARD_COLUMNS/2)] = self._black
            self._board[int(self._BOARD_ROWS/2)][int((self._BOARD_COLUMNS/2)-1)] = self._black
        elif self._topLeft == self._black:
            self._board[int((self._BOARD_ROWS/2)-1)][int((self._BOARD_COLUMNS/2)-1)] = self._black
            self._board[int(self._BOARD_ROWS/2)][int(self._BOARD_COLUMNS/2)] = self._black
            self._board[int((self._BOARD_ROWS/2)-1)][int(self._BOARD_COLUMNS/2)] = self._white
            self._board[int(self._BOARD_ROWS/2)][int((self._BOARD_COLUMNS/2)-1)] = self._white

        return self._board

    def _new_board(self) -> [[int]]:
        '''Create new board'''
        board = []
        for row in range(self._BOARD_ROWS):
            board.append([])
            for col in range(self._BOARD_COLUMNS):
                board[-1].append(0)
        
        return board


        

    def count_black(self)-> int:
        '''Returns the number of black discs in the game board'''
        black = 0
        for row in range(len(self._board)):
            for col in range(len(self._board[0])):
                if self._board[row][col] == 'B':
                    black += 1
        return black

    def count_white(self)-> int:
        '''Returns the number of white discs in the game board'''
        white = 0
        for row in range(len(self._board)):
            for col in range(len(self._board[0])):
                if self._board[row][col] == 'W':
                    white += 1
        return white


    
# all the checking directions

    def _check_top(self, row: int, col:int)->list:
        ''' Check to the top direction of the board if the discs can be flipped and store
        it into a list'''
        coordList = []
        possibleCoord = []
        currRow = row
        currCol = col
        while True:
            if self._valid_coord(currRow-1, currCol):
                if self._board[currRow-1][currCol] == self._turn:
                    coordList.extend(possibleCoord)
                    break
                    
                elif self._board[currRow-1][currCol] == self.opposite_turn():
                    possibleCoord.append((currRow-1, currCol))
                    currRow -= 1
                elif self._board[currRow-1][currCol] == 0:
                    break
            else:
                break

        return coordList

    def _check_bottom(self, row: int, col: int)->list:
        ''' Check to the bottom direction of the board if the discs can be flipped and store
        it into a list'''
        coordList = []
        possibleCoord = []
        currRow = row
        currCol = col
        while True:
            if self._valid_coord(currRow+1, currCol):
                if self._board[currRow+1][currCol] == self._turn:
                    coordList.extend(possibleCoord)
                    break
                    
                elif self._board[currRow+1][currCol] == self.opposite_turn():
                    possibleCoord.append((currRow+1, currCol))
                    currRow += 1
                elif self._board[currRow+1][currCol] == 0:
                    break
            else:
                break
            
        return coordList

    def _check_left(self, row: int, col: int)-> list:
        ''' Check to the left side of the board if the discs can be flipped and store
        it into a list'''
        coordList = []
        possibleCoord = []
        currRow = row
        currCol = col
        while True:
            if self._valid_coord(currRow, currCol-1):
                if self._board[currRow][currCol-1] == self._turn:
                    coordList.extend(possibleCoord)
                    break
                    
                elif self._board[currRow][currCol-1] == self.opposite_turn():
                    possibleCoord.append((currRow, currCol-1))
                    currCol -= 1
                elif self._board[currRow][currCol-1] == 0:
                    break
            else:
                break

        return coordList

    def _check_right(self, row: int, col: int)->list:
        ''' Check to the right side of the board if the discs can be flipped and store
        it into a list'''
        coordList = []
        possibleCoord = []
        currRow = row
        currCol = col
        while True:
            if self._valid_coord(currRow, currCol+1):
                if self._board[currRow][currCol+1] == self._turn:
                    coordList.extend(possibleCoord)
                    break
                    
                elif self._board[currRow][currCol+1] == self.opposite_turn():
                    possibleCoord.append((currRow, currCol+1))
                    currCol += 1
                elif self._board[currRow][currCol+1] == 0:
                    break
            else:
                break
        return coordList

    def _check_top_right(self, row: int, col: int)->list:
        ''' Check to the top right direction of the board if the discs can be flipped and store
        it into a list'''
        coordList = []
        possibleCoord = []
        currRow = row
        currCol = col
        while True:
            if self._valid_coord(currRow-1, currCol+1):
                if self._board[currRow-1][currCol+1] == self._turn:
                    coordList.extend(possibleCoord)
                    break
                    
                elif self._board[currRow-1][currCol+1] == self.opposite_turn():
                    possibleCoord.append((currRow-1, currCol+1))
                    currRow -= 1
                    currCol += 1
                elif self._board[currRow-1][currCol+1] == 0:
                    break
            else:
                break
        return coordList

    def _check_bottom_right(self, row: int, col: int)-> list:
        ''' Check to the bottom right direction of the board if the discs can be flipped and store
        it into a list'''
        coordList = []
        possibleCoord = []
        currRow = row
        currCol = col
        while True:
            if self._valid_coord(currRow+1, currCol+1):
                if self._board[currRow+1][currCol+1] == self._turn:
                    coordList.extend(possibleCoord)
                    break
                    
                elif self._board[currRow+1][currCol+1] == self.opposite_turn():
                    possibleCoord.append((currRow+1, currCol+1))
                    currRow += 1
                    currCol += 1
                elif self._board[currRow+1][currCol+1] == 0:
                    break
            else:
                break
        return coordList

    def _check_top_left(self, row: int , col: int)-> list:
        ''' Check to the top left direction of the board if the discs can be flipped and store
        it into a list'''
        coordList = []
        possibleCoord = []
        currRow = row
        currCol = col
        while True:
            if self._valid_coord(currRow-1, currCol-1):
                if self._board[currRow-1][currCol-1] == self._turn:
                    coordList.extend(possibleCoord)
                    break
                    
                elif self._board[currRow-1][currCol-1] == self.opposite_turn():
                    possibleCoord.append((currRow-1, currCol-1))
                    currRow -= 1
                    currCol -= 1
                elif self._board[currRow-1][currCol-1] == 0:
                    break
            else:
                break
        return coordList

    def _check_bottom_left(self, row: int, col: int)-> list:
        ''' Check to the bottom left direction of the board if the discs can be flipped and store
        it into a list'''
        coordList = []
        possibleCoord = []
        currRow = row
        currCol = col
        while True:
            if self._valid_coord(currRow+1, currCol-1):
                if self._board[currRow+1][currCol-1] == self._turn:
                    coordList.extend(possibleCoord)
                    break
                    
                elif self._board[currRow+1][currCol-1] == self.opposite_turn():
                    possibleCoord.append((currRow+1, currCol-1))
                    currRow += 1
                    currCol -= 1
                elif self._board[currRow+1][currCol-1] == 0:
                    break
            else:
                break
        return coordList

# all the flipping

    def _flip_list(self, row: int, column: int)-> list:
        ''' takes all the "flippable" discs for each direction
        and put it into one list'''
        coordList = []
        
        coordList.extend(self._check_top(row,column))
        coordList.extend(self._check_bottom(row,column))
        coordList.extend(self._check_left(row,column))
        coordList.extend(self._check_right(row,column))
        coordList.extend(self._check_top_right(row,column))
        coordList.extend(self._check_top_left(row,column))
        coordList.extend(self._check_bottom_right(row,column))
        coordList.extend(self._check_bottom_left(row,column))
                
        return coordList

    def _flip_coords(self, coordList : list):
        for coordNum in range(len(coordList)):
            for coord in coordList:
                self._board[coord[0]][coord[1]] = self._turn
            
# all the checking board full, possible-move, winning condition
    def _at_least_one_move(self)->bool:
        ''' check if there's at least one move to be made on the board'''
        for row in range(self._BOARD_ROWS):
            for col in range(self._BOARD_COLUMNS):
                if self._board[row][col] == 0:
                    if len(self._flip_list(row,col)) > 0:
                        return True

        return False

    def _board_full(self) -> bool:
        ''' check each coordinate of the board to know whether the board
        is full'''
        for row in range(self._BOARD_ROWS):
            for col in range(self._BOARD_COLUMNS):
                if self._board[row][col] == 0:
                    return False
        return True

            
    def _winning_condition(self) ->bool:
        ''' set the winning condition if the board is full or no further move
        can be made for both colors'''
        if self._board_full() or (self._blackPass and self._whitePass):
            return True
        return False

#valid coordinate containing column and row

    def _require_valid_col_num(self, column_number: int) -> None:
        ''' Raise an error if the column is invalid'''
        if type(column_number) != int or not self._valid_col_num(column_number):
            raise OthelloInvalidMoveError()
        
    def _require_valid_row_num(self, row_number: int) -> None:
        ''' Raise an error when the row is invalid'''
        if type(row_number) != int or not self._valid_row_num(row_number):
            raise OthelloInvalidMoveError()

    def _require_game_not_over(self)->None:
        ''' Raise game over error when there's a winner'''
        if self.winning_player() != None:
            raise OthelloGameOver()

    def _valid_col_num(self, column_number:int) -> bool:
        ''' makes sure that the given column is inside the board'''
        return 0 <= column_number < self._BOARD_COLUMNS

    def _valid_row_num(self, row_number:int) -> bool:
        ''' makes sure that the given row is inside the board'''
        return 0 <= row_number < self._BOARD_ROWS


    def _valid_coord(self, row: int, column: int)->bool:
        ''' check if both of the given row and column number are valid coordinate'''
        return self._valid_row_num(row) and self._valid_col_num(column)
