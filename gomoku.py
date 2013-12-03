import Board as b
import ast
import Eval_funcs as ef
import Queue as q
import time

def gomoku(board_size=0, connect_size=0, player=0, tlimit =0, tournament = False):
    """
    board_size: int (default 0)
    connect_size: int (default 0)
    player: int (default 0)
    tlimit  : int (default 0)
    tournament: bool (default False)

    board_size is the size of the board you want to play on.
    connect_size is the number of connections you need to win.
    player is the player mode
    tlimit is the amount of time given to make a move
    If tournament is set to true, then it will work with the tournament.sh scripts
    """
    if tournament: f = file("mypipe", "w")
    while not board_size:
        try:
            board_size = int(raw_input("Please input a positive integer board size: "))
        except ValueError:
            print("Invalid Board Size")
            continue;

    while not connect_size:
        try:
            connect_size = int(raw_input("Please input a positive integer connection length: "))
        except ValueError:
            print("Invalid Connection Length")
            continue;

    while (player > 6 or player < 1):
            print("Enter an integer to pick a mode of play:")
            print("1)Human vs Human")
            print("2)Human vs AI")
            print("3)AI vs Human")
            print("4)Random vs AI")
            print("5)AI vs Random")
            print("6)AI vs AI")
            try:
                player = int(raw_input())
            except ValueError:
                print("Invalid Play Mode, please enter a valid integer")
                continue
    if player in (2,3,4,5,6) and not tlimit:
        while True:
            try:
                tlimit =int(raw_input("Please input a time constraint as a number of seconds: "))
                break;
            except ValueError:
                continue
    
    board = b.Board(board_size, connect_size)
    print("Black moves first")
    print(board)
    
    if player in (3,5,6):
        move = ef.firstmove(board)
    elif player in (1,2):
        while True:
            try:
                move = ast.literal_eval(raw_input("Please enter your move in format '(y,x)': "))
                break
            except(ValueError,SyntaxError,TypeError):
                continue
    elif player == 4:
        move = ef.randommove(board)
    board = board.move(move)
    print("Black moved {0}".format(move))
    if tournament:
	f.write("{0}".format(move))
        f.flush()
    if player in (2,4,6):
        move = ef.secondmove(board)
    elif player in (1,3):
        print(board)
        while True:
            try:
                move = ast.literal_eval(raw_input("Please enter your move in format '(y,x)': "))
                break
            except(ValueError,SyntaxError,TypeError):
                continue
    elif player == 5:
        move = ef.randommove(board)
    board = board.move(move)
    if tournament:
        f.write("{0}".format(move))#DEBUG!!!!!
        f.flush()
    print(board)
    print("White moved {0}".format(move))
    
    

    while not board.win:
        #Black Moves
        if player in (3,5,6):
            t = time.time()
            move = ef.nextMove(board,tlimit,3)
            print(time.time() -t)
        elif player in (1,2):
            while not board.win:
                try:
                    move = ast.literal_eval(raw_input("Please enter your move in format '(y,x)': "))
                    break
                except (ValueError,SyntaxError,TypeError):
                    continue
        elif player == 4:
            move = ef.randommove(board)
        board = board.move(move)
        print(board)
        print("Black moves {0}".format(move))
	if tournament:
	    f.write("{0}".format(move))
	    f.flush()

        if player in (2,4,6):
            t= time.time()
            move = ef.nextMove(board,tlimit,3)
            print(time.time() -t)
        elif player in (1,3):
            while not board.win:
                try:
                    move = ast.literal_eval(raw_input("Please enter your move in format '(y,x)': "))
                    break
                except(ValueError,SyntaxError,TypeError):
                    continue
        elif player == 5:
            move = ef.randommove(board)
        board = board.move(move)
        print(board)
        print("White moves {0}".format(move))
	if tournament:
	    f.write("{0}".format(move))
	    f.flush()
    print("HEY THE GAME IS OVER YAYAYAYAYAY!!!!!!!!!!")
    if tournament: f.close()
    return

if __name__=="__main__":
    gomoku(15,5,3,60,True)
