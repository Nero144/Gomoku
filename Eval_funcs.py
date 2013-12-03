import Queue as q
import Board as b
import time
import random


def firstmove(board):
    """
    board : board object
    return: (int,int)

    If the AI gets to go first, it shouldn't
    even think- it should just pick the middle
    position
    """
    x = board.size/2
    return (x,x)

def secondmove(board):
    """
    board : board object
    return: (int,int)

    If the AI must go second, it shouldn't think,
    it should just go diagonal adjacent to the first
    placed tile; diagonal into the larger area of the
    board if one exists
    """
    (oy,ox) = board.black[0]
    if oy <= board.size/2:
        dy = 1
    else: dy = -1

    if ox <=board.size/2:
        dx = 1
    else: dx = -1
    return (oy+dy,ox+dx)

def randommove(board):
    """
    board : board object
    return: (int,int)

    Takes a board object, and (pseudo-)randomly
    returns an open coordinate on the board
    """
    t = True
    while t:
        y = random.randint(0,board.size-1)
        x = random.randint(0,board.size-1)
        t = not board._valid_move((y,x))
    return (y,x)



def _eval_func(board,position, attack):
    """
    board   : board object
    position: (int,int)
    attack  :  bool
    return  :  int

    Takes a board, and a position on that board,
    and evaluates the importance of that position on
    the board.  It does so by evaluating the number of 
    ways that that position can be used in making a
    board.connect, with an exponential weighting for 
    more pieces in a connection.  Extremely heavy weighting
    for making a full on board.connect- but the connection is
    weighted heavier if in attack mode than if in defense mode.
    That way, the function will always place taking a winning
    move over blocking another's winning move.
    """
    (y,x) = position
    color = board.turn() if attack else board.turn().getNot()
    total_consec = 0
    for pair in ((1,0),(0,1),(1,1),(1,-1)):
        (dy,dx) = pair
        pathlist =["."]
        for s in (1,-1):
            for i in range(1,board.connect):
                py = y+dy*i*s
                px = x+dx*i*s   #out of board, or enemy blocking(VVVBelowVVV)
                if (not board._inBoard((py,px)) or \
		    board[py][px] == color.getNot().symbol) or \
                   (i+1 == board.connect and \
		    board._inBoard((py+dy*s,px+dx*s)) and \
		    board[py+dy*s][px+dx*s] == color.symbol): #checking for overline rule
                    break
                elif s>0:#append to back if right of position
                    pathlist.append(board[py][px])
                elif s<0:#insert to front if left of position
                    pathlist.insert(0,board[py][px])

        paths_num = len(pathlist) - len(board) + 1 #number of ways you can make board.connect in a row using position
        if paths_num>0:
            for i in range(paths_num):
                consec = pathlist[i:i+board.connect].count(color.symbol)
                total_consec += consec**5 if consec!=board.connect-1 else 100**(9 if attack else 8) 
    return total_consec

def evaluate_position(board,position):
    """
    board   : board object
    position: (y,x)
    return  : int

    Takes a board and a position on that board,
    and if the position is a valid move, then returns _eval_func(attack=True) +_eval_func(attack=False).
    This is because _eval_func(True) evaluates the attack power of the position for whoever's turn it is,
    and _eval_func(False) evaluates the attack power for the other player, which is the defensive power
    of that position for the player whose turn it is.  Thus, the importance of a position is rated as
    it's attack power + it's defense power, which is attack power for you + attack power for them.
    If an invalid move is suggested, the move is rated as 0 importance.
    """

    return _eval_func(board,position,True)+_eval_func(board,position,False) \
    if board._valid_move(position) else 0


def attackArea((y,x), connect):
    """
    (y,x)  : (int,int)
    connect: int
    return : list of (int,int)

    Takes a coordinate, and returns a list of the coordinates
    within connect spaces of (y,x) that could be attacked by a
    Queen (in chess) sitting in space (y,x)
    """
    area = []
    for pair in ((1,0),(0,1),(1,1),(1,-1)):
        (dy,dx) = pair
        for s in (1,-1):
            for i in range(1,connect):
                py = y+dy*i*s
                px = x+dx*i*s
                area.append((py,px))
    return area
    
def topatoms(board,limit):
    """
    board : board object
    limit : int
    return: list of (int,(int,int))

    Takes a board object, and returns
    the top 'limit' number of moves, as
    valued by evaluate_position()
    """
    topqueue = q.PriorityQueue()
    spots = set()
    for t in board.black+board.white:
        for m in attackArea(t,len(board)):
            if board._inBoard(m):
                spots.add(m)
    for r in spots:
        topqueue.put((evaluate_position(board,r)*(-1),r))
    toplist = []       
    for x in range(limit):
        toplist.append(topqueue.get())
    return map(lambda (x,y): (-x,y), toplist)



def justBestMoves(board,limit):
    """
    board : board object
    limit : int
    return: list of (int,int)

    The same as topatoms(), but returns only
    moves valued equal to the best valued move
    as rated by evalutate_position(), and the
    list returned does not contain the values
    of the moves returned
    """
    toplist = topatoms(board,limit)
    topval = toplist[0][0]
    bestlist =[]
    for atom in toplist:
        (val,move) = atom
        if val ==topval:
            bestlist.append(move)
    return bestlist
            

    
def nextMove(board, tlimit, dive = 1):
    """
    board : board object
    tlimit: float
    dive  : int
    return: (int,int)

    Takes a board, a time limit (tlimit), and a dive number, and
    implements quiescent search dive_#.
    Returns a move where quiescent search predicts a win, or
    the best move according to evalute_position()
    """
    checkTOP_ = 10
    checkDEPTH_ = 20
    atomlist = topatoms(board,checkTOP_)
    mehlist = []
    bahlist = []
    
    tfract = (tlimit-((0.1)*(tlimit/10 +1)))/float(len(atomlist))
    for atom in atomlist:
        (val,move) = atom
        nextboard = board.move(move)
        if nextboard.win:
            return move
        if dive ==1:
            score = -dive_1(nextboard, checkDEPTH_-1)
        elif dive==2:
            score = -dive_2(nextboard,checkDEPTH_-1)
        elif dive==3:
            score = -dive_3(nextboard,checkDEPTH_-1, time.time(),tfract)
        elif dive==4:
            score = -dive_4(nextboard,time.time(),tfract)
        elif dive==5:
            score = -dive_5(nextboard,checkDEPTH_-1)

        if score ==1:
            #print("This move can force a win")#debug!!!!!!!
            return move
        elif score ==0:
            mehlist.append((score,move))
	elif score > -1:
	    bahlist.append((score,move))
    if len(mehlist): return mehlist[0][1]
    elif len(bahlist):
        bahlist.sort()
	return bahlist[-1][1]
    else: return atomlist[0][1]

########Different versions of quiescent searches below#######################


def dive_1(board, dlimit):
    bestmove = topatoms(board,1)[0][1]
    newboard = board.move(bestmove)
    if newboard.win: return 1
    elif not dlimit: return 0
    else:            return -dive_1(newboard,dlimit-1)

def dive_2(board,dlimit):
    bestmoves = justBestMoves(board,5) #maybe widen this window?
    overall = 0.0
    split_factor = 1.0/len(bestmoves)
    for bmove in bestmoves:
        newboard = board.move(bmove)
        if newboard.win: return 1
        elif not dlimit: continue
        else:
            score = -dive_2(newboard,dlimit-1)
            if score ==1: return 1
            else: overall += split_factor*score
    return overall

def dive_3(board,dlimit,start_tyme,tlimit):
    bestmove = topatoms(board,1)[0][1]
    newboard = board.move(bestmove)
    if newboard.win: return 1
    elif time.time()-start_tyme>tlimit or not dlimit: return 0
    else:            return -dive_3(newboard,dlimit-1,start_tyme,tlimit)

def dive_4(board,start_tyme,tlimit):
    bestmove = topatoms(board,1)[0][1]
    newboard = board.move(bestmove)
    if newboard.win: return 1
    elif time.time()-start_tyme>tlimit: return 0
    else:            return -dive_4(newboard,start_tyme,tlimit)

def dive_5(board,dlimit):
    TOPCHECK = 3
    bestmoves = topatoms(board,TOPCHECK)
    overall = 0.0
    split_factor = 1.0/len(bestmoves)
    for bmove in bestmoves:
        newboard = board.move(bmove[1])
        if newboard.win: return 1
        elif not dlimit: return 0
        else:
            score = -dive_5(newboard,dlimit-1)
            if score ==1: return 1
            elif not score: return 0
            else: overall +=split_factor
    return overall













    
    
    

    
    
