# noughts and crosses

import random 
#  board layout
#  3 * * *
#  2 * * * 
#  1 * * *
#    A B C
# We are using a bitboard representation

NOUGHTS = -1
CROSSES = 1

board = (0,0,NOUGHTS) # NOUGHTS, CROSSES, side-to-move

# bit pattern constants
A1 = 1
B1 = 2
C1 = 4
A2 = 8
B2 = 16
C2 = 32
A3 = 64
B3 = 128
C3 = 256
vals = [A1,B1,C1,A2,B2,C2,A3,B3,C3]

move_map = {
    "A1": 0,
    "B1": 1,
    "C1": 2,
    "A2": 3,
    "B2": 4,
    "C2": 5,
    "A3": 6,
    "B3": 7,
    "C3": 8,
}
move_map_reverse = {
    0: "A1",
    1: "B1",
    2: "C1",
    3: "A2",
    4: "B2",
    5: "C2",
    6: "A3",
    7: "B3",
    8: "C3"
}


FULLBOARD = 511

# three in a row patterns
THREE_A = 73 # file A
THREE_B = 146 # file B
THREE_C = 292 # file C
THREE_1 = 7 # rank 1
THREE_2 = 56 # rank 2
THREE_3 = 448 # rank 3
THREE_D1 = 84 # diag A3-B2-C1
THREE_D2 = 273 # diag A1-B2-C3

def is_won(bitmap):
    if bitmap & THREE_A == THREE_A:
        return True
    if bitmap & THREE_B == THREE_B:
        return True
    if bitmap & THREE_C == THREE_C:
        return True
    if bitmap & THREE_1 == THREE_1:
        return True
    if bitmap & THREE_2 == THREE_2:
        return True
    if bitmap & THREE_3 == THREE_3:
        return True
    if bitmap & THREE_D1 == THREE_D1:
        return True
    if bitmap & THREE_D2 == THREE_D2:
        return True

    return False

def make_move(move):
    '''
    execute the move on the board
    '''
    global board
    (noughts, crosses, stm) = board
    if stm == NOUGHTS:
        noughts = noughts | move[1]
        stm = CROSSES
    else:
        crosses = crosses | move[1]
        stm = NOUGHTS 
    board = (noughts,crosses,stm)

def unmake_move(move):
    '''
    undo the move on the board
    '''
    global board
    (noughts, crosses, stm) = board
    if stm == NOUGHTS:
        crosses = crosses & (~move[1])
        stm = CROSSES
    else:
        noughts = noughts & (~move[1])
        stm = NOUGHTS 
    board = (noughts,crosses,stm)
    
def score():
    '''
    calculate a score for the current position
    '''
    global board
    (noughts, crosses, stm) = board
    # if opponent has won, return win score for opponent
    if stm == NOUGHTS and is_won(crosses):
        return CROSSES
    if stm == CROSSES and is_won(noughts):
        return NOUGHTS
    # if no moves available, return 0 (draw)
    populated = noughts | crosses 
    if populated == FULLBOARD:
        return 0
    # otherwise generate moves and recurse
    moves = FULLBOARD & (~populated)
    movelist = list_moves(moves)
    if stm == NOUGHTS: # set a minimum score
        eval = CROSSES
    else:
        eval = NOUGHTS
    for move in movelist:
        make_move(move)
        new_eval = score()
        unmake_move(move)
        if eval == stm: # I can win on this move
            return eval
        if stm == NOUGHTS: # is this a better move?
            if new_eval < eval:
                eval = new_eval
        else:
            if new_eval > eval:
                eval = new_eval 
    return eval

def best_move():
    '''
    calculate a score for the current position
    '''
    global board
    (noughts, crosses, stm) = board
    populated = noughts | crosses 
    moves = FULLBOARD & (~populated)
    movelist = list_moves(moves)
    #return random.choice(movelist)
    if stm == NOUGHTS: # set a minimum score
        eval = CROSSES
    else:
        eval = NOUGHTS
    best_move = movelist[0]
    for move in movelist:
        make_move(move)
        new_eval = score()
        unmake_move(move)
        if stm == NOUGHTS: # is this a better move?
            if new_eval < eval:
                eval = new_eval
                best_move = move
        else:
            if new_eval > eval:
                eval = new_eval 
                best_move = move
    return best_move

def list_moves(move_bb):
    '''
    generates a list of moves from a legal moves bitboard
    '''
    movelist = [] # each move is (pos, bb)
    for i in range(0,9):
        val = vals[i]
        if (val & move_bb) == val:
            movelist.append( (i, val) )
    return movelist

def getpiece(pos):
    '''
    gets piece (O, X or blank) at the specified position (0 - 8)
    '''
    val = vals[pos]
    (noughts, crosses, stm) = board
    if (noughts & val) == val:
        return "O"
    elif (crosses & val) == val:
        return "X"
    else:
        return " "

def show_board():
    '''
    displays the given board
    '''
    rank_3 = "3 |{} {} {}".format(getpiece(6), getpiece(7), getpiece(8))
    rank_2 = "2 |{} {} {}".format(getpiece(3), getpiece(4), getpiece(5))
    rank_1 = "1 |{} {} {}".format(getpiece(0), getpiece(1), getpiece(2))
    rank_0 = "  +------"
    rank__ = "   A B C"
    if board[2] == NOUGHTS:
        stm = "Side to move: noughts"
    else:
        stm = "Side to move: crosses"
    repr = rank_3 + "\n" + rank_2 + "\n" + rank_1 + "\n" + rank_0 + "\n" + rank__ + "\n" + stm
    return repr
    
def string_to_move(move_string):
    pos = move_map[move_string]
    val = vals[pos]
    return (pos,val)

def move_to_string(move):
    movestr = move_map_reverse[move[0]]
    return movestr

def compmove():
    print("Thinking... ")
    move = best_move()
    print("I move {}".format(move_to_string(move)))
    make_move(move)

comp_stm = 0
while True:
    print(show_board())
    print()
    cmd = input("> ")

    cmd_bits = cmd.split(' ')

    # move command
    if (len(cmd_bits) == 2) and cmd_bits[0] == "move":
        move = string_to_move(cmd_bits[1])
        # TODO check that the move is legal
        make_move(move)
        # TODO check end - turn off compmove

        # if comp is now on move, move
        if comp_stm == board[2]:
            compmove()
            # TODO check end - turn off compmove
        
    # go command - force computer move
    if (len(cmd_bits) == 1) and cmd_bits[0] == "go":
        compmove()
        

    # new command - start new game
    if (len(cmd_bits) == 1) and cmd_bits[0] == "new":
        print("Initialising new game.")
        print()
        board = (0,0,NOUGHTS) # NOUGHTS, CROSSES, side-to-move
        comp_stm = 0

    # auto command - auto O | auto X - computer will play that side
    if (len(cmd_bits) == 2) and cmd_bits[0] == "auto":
        if cmd_bits[1] == "O":
            comp_stm = NOUGHTS
        elif cmd_bits[1] == "X":
            comp_stm = CROSSES 
        else:
            comp_stm = 0
        # if comp is now on move, move
        if comp_stm == board[2]:
            compmove()
            # TODO check end - turn off compmove
        



    # test 
    if (len(cmd_bits) == 1) and cmd_bits[0] == "test":
        moves = list_moves(FULLBOARD)
        for move in moves:
            print("----------------------------------------")
            print(show_board())
            print("test move {}".format(move_to_string(move)))
            make_move(move)
            print(show_board())
            print("unmake move")
            unmake_move(move)
            print(show_board())

