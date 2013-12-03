import copy
class Board:
    """
    A class that defines the board
    for a game of gomoku
    """
    def __init__(self,size,connect):
        """
        size: int
        connect: int

        defines the board as size by size
        connect defines the number of connections
        needed to win the game of gomoku
        """
        self.white = []#list of white's pieces
        self.black = []#list of black's pieces
        self.board = [["." for x in range(size)] for x in range(size)]
        self.size = size
        self.connect = connect #connect number needed to win
        self.win = False #win status
        self.winstatement = ""

    def __str__(self):
        string = ""
        if self.win:
            string += self.winstatement +"\n"
        string+="  "
        for i in range(self.size):
            string+="{0}{1}".format(i%10, " " if i<10 else "'")
        string +="\n"
        i = 0
        for x in self.board:
            string +="{0}{1}".format(i%10," " if i<10 else "'")
            i+=1
            for y in x:
                string+="{0} ".format(y)
            string+="\n"
        return string

    def __len__(self): return self.connect #len(board) returns connected number needed to win

    def __repr__(self): return str(self)

    def __getitem__(self,num): return self.board[num]

    def __eq__(self,other):
        return ( 
        type(self) == type(other) and \
        self.white == other.white and \
        self.black == other.black and \
        self.size  == other.size)

    def __ne__(self,other):
        return not (self == other)

    def turn(self): #returns the color object of whoever's turn it is
        return color(len(self.black)==len(self.white))

    def _valid_move(self, (y,x)):
        """
        (y,x) : (int,int)
        return: bool

        Takes a tuple, and returns True if
        the tuple represents a valid space
        in the board that is unoccupied.
        Else, False
        """
        return self._inBoard((y,x)) and\
           self.board[y][x] == "."
        
    def _inBoard(self,(y,x)):
        """
        (y,x) : (int,int)
        return: bool

        takes a tuple of ints, and returns
        True if it represents a valid coordinate
        in the board

        """
        return x >= 0 and \
               x < self.size and \
               y >= 0 and \
               y < self.size
       
    def move(self,(y,x)):
        """
        (y,x) : (int,int)
        return: board object

        Takes a coordinate, and returns a board object in which
        that move has been executed.  If self.win is True (the 
        board that move() is being executed on has already been
        won), then the move/piece-placement is not executed, and
        a copy of self is returned instead.
        If the coordinate entered is invalid (self._valid_move((y,x))==False)
        then the game is over, and win statement is set to explain that
        the opposite player wins by default
        """
        turn = self.turn()
        other = copy.deepcopy(self)
        if self.win:
            #print("The Game Is Already Over")
            return other
        if not other._valid_move((y,x)):
            turn.swap()
            other.winstatement = "Invalid Move ({1},{2}) Played: {0} Wins by Default\n".format(str(turn),y,x)
            other.win = True
            return other
        
        other.board[y][x] = turn.symbol
        other.black.append((y,x)) if turn.isBlack else other.white.append((y,x))
        other.checkWinningMove()
        return other

    def _checkPath(self, color, (y,x), (py,px), counter):
        """
        color  : color object
        (y,x)  : (int,int)
        (py,px): (int,int)
        counter: int
        return : int
    
        Returns the number of consecutive
        symbols of a given color along a path
        by incrementing (y,x) by (py,px) until
        counter ==0 or self.board[y][x] !=color.symbol
        """
        if not counter or \
       not self._inBoard((y,x)) or \
       self.board[y][x] != color.symbol:
            return 0
        return 1 + \
    (self._checkPath(color,(y+py,x+px),(py,px),counter -1) if self._inBoard((y+py,x+px)) else 0)


    def checkWinningMove(self):
        """
        return: void

        checkWinningMove retrieves the last move made,
        and checks if that move won the game.  If so,
        it sets self.win to True, and sets an appropriate
        message for the win statement
        """
        color = self.turn().getNot() #We need the player who JUST MADE a move, not whose turn it is
        pos = self.black[-1] if color.isBlack else self.white[-1]
        checklist = []
        depth = self.connect -1
        for move in ((1,0),(0,1),(1,1),(1,-1)):
            opp = tuple(map(lambda x: -x, move))
            checklist.append(1 +\
                      self._checkPath(color,tuple(sum(x) for x in zip(pos,move)),move,depth) +\
                      self._checkPath(color,tuple(sum(x) for x in zip(pos,opp)), opp,depth)
                      )
        if self.connect in checklist:
            self.winstatement = "{0} wins!".format(str(color))
            self.win = True
	elif len(self.black)+len(self.white) == self.size**2:
	    self.win = True
	    self.winstatement = "It's a Draw (Defensive win for WHITE)"
        return

class color:
    """
    A simple color class.
    Initializes with a bool argument:
    Arbitrarily, True->color is black
                 False->color is white
    """
    def __init__(self, isBlack):
        if isBlack:
            self.isBlack = True
            self.color = "BLACK"
            self.symbol = "x"
        else:
            self.isBlack = False
            self.color = "WHITE"
            self.symbol = "o"

    def __eq__(self, other):
        return type(self)==type(other) and \
           self.color==other.color

    def __ne__(self,other): return not (self == other)

    def __str__(self): return self.color

    def __repr__(self): return str(self)

    def swap(self): #swaps a color object from Black->White or reverse
        self.__init__(not self.isBlack)

    def getNot(self): #returns a color object != self
        return color(not self.isBlack)
