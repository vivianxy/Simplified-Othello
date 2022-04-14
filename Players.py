'''
    Erich Kramer - April 2017
    Apache License
    If using this code please cite creator.
'''
'''reference: https://github.com/aimacode/aima-python/blob/master/games.py and https://github.com/aimacode/aima-python/blob/master/games4e.py'''
# import OthelloBoard

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    #PYTHON: use obj.symbol instead
    def get_symbol(self):
        return self.symbol
    
    #parent get_move should not be called
    def get_move(self, board):
        raise NotImplementedError()


class HumanPlayer(Player):
    def __init__(self, symbol):
        Player.__init__(self, symbol)

    def clone(self):
        return HumanPlayer(self.symbol)
        
#PYTHON: return tuple instead of change reference as in C++
    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return  (col, row)


class MinimaxPlayer(Player):
    def __init__(self, symbol):
        Player.__init__(self, symbol)
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'

    def utility(self, board):
        b1=board.count_score(self.symbol)
        b2=board.count_score(self.oppSym)
        return b1-b2
    def terminal_test(self,board):
        if (board.has_legal_moves_remaining('0')==False) and (board.has_legal_moves_remaining('X')==False):
            return True
        else:
            return False
    def actions(self,symbol,board):
        possible_moves=[]
        for i in range(4):
            for j in range(4):
                if board.is_legal_move(j,i,symbol):
                    possible_moves.append((j,i))
        return possible_moves
    def result(self,board,col,row,oppSym):
        temp=board.cloneOBoard()
        temp.play_move(col,row,oppSym)
        return temp
    #function MAX_VALUE(state) return a utility value
    def max_value(self,board):
        if self.terminal_test(board):# if terminal_test(state) return UTILITY(state)
            return self.utility(board)
        v=-float('inf') # v<-negative infinity
        for j,i in self.actions(self.symbol,board): #for each a in actions(state) do
            v=max(v,self.min_value(self.result(board,j,i,self.oppSym))) #v <- MAX(v, MIN_VALUE(RESULT(s,a)))
        return v
    #function MIN_VALUE(state) return a utility value
    def min_value(self,board):
        if self.terminal_test(board):# if terminal_test(state) return UTILITY(state)
            return self.utility(board)    
        v=float('inf') # v<-positive infinity
        for j,i in self.actions(self.oppSym,board):#for each a in actions(state) do
            v=min(v,self.max_value(self.result(board,j,i,self.oppSym))) #v <- MIN(v, MAX_VALUE(RESULT(s,a)))
        return v
    def get_move(self,board):
        valid_moves=self.actions(self.symbol,board)
        v= -float('inf')
        for cols,rows in valid_moves:
            v=max(v,self.min_value(self.result(board,cols,rows,self.oppSym)))
            best_col=cols
            best_row=rows
        if v == -float('inf'):
            return cols,rows
        return (best_col,best_row)