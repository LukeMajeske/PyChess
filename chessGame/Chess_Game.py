from pygame import *
import os.path
filepath = os.path.dirname(__file__)


chessFiles = ['a','b','c','d','e','f','g','h']
chessRows = ['8','7','6','5','4','3','2','1']
chessPieces = ['Bishop','Knight','King','Queen','Pawn','Rook']
chessBoard = {'a8':'bRook','b8':'bKnight','c8':'bBishop','d8':'bQueen','e8':'bKing','f8':'bBishop','g8':'bKnight','h8':'bRook',
              'a7':'bPawn','b7':'bPawn','c7':'bPawn','d7':'bPawn','e7':'bPawn','f7':'bPawn','g7':'bPawn','h7':'bPawn',
              'a6':' ','b6':' ','c6':' ','d6':' ','e6':' ','f6':' ','g6':' ','h6':' ',
              'a5':' ','b5':' ','c5':' ','d5':' ','e5':' ','f5':' ','g5':' ','h5':' ',
              'a4':' ','b4':' ','c4':' ','d4':' ','e4':' ','f4':' ','g4':' ','h4':' ',
              'a3':' ','b3':' ','c3':' ','d3':' ','e3':' ','f3':' ','g3':' ','h3':' ',
              'a2':'wPawn','b2':'wPawn','c2':'wPawn','d2':'wPawn','e2':'wPawn','f2':'wPawn','g2':'wPawn','h2':'wPawn',
              'a1':'wRook','b1':'wKnight','c1':'wBishop','d1':'wQueen','e1':'wKing','f1':'wBishop','g1':'wKnight','h1':'wRook'}



class Piece:
    def __init__(square,color,piece,chessBoard):
        self.color = color
        self.square = square
        chessBoard[square]= color+piece
        self.image = image.load(color+piece+'.png')
    
class Bishop(Piece):
    def moveSet(cur_square,target):
        cur_column = chessFiles.index(cur_square[0])
        cur_row = chessRows.index(cur_square[1])
        tar_column = chessFiles.index(target[0])
        tar_row = chessRows.index(target[1])

        if cur_square == target:
            return False

        diag_x = tar_column - cur_column
        diag_y =  tar_row - cur_row


        if abs(diag_x) == abs(diag_y):
            sign_x = sign(diag_x)
            sign_y = sign(diag_y)

            print(cur_column,tar_column)
            print(cur_row,tar_row)
            for dif in range(1,abs(diag_x)+1):
                #Check if squares between target and cur_square have pieces
                #in the way
                
                column = chessFiles[cur_column+(dif*sign_x)]
                row = chessRows[cur_row+(dif*sign_y)]
                
                piece = chessBoard[column+row]
                print(piece)
                print(dif,abs(diag_x))
                

                if piece != BLANK and dif != abs(diag_x):
                    return False
                elif dif == abs(diag_x) and capture(cur_square,target):
                    return True
                elif dif == abs(diag_x) and not capture(cur_square,target):
                    return False

            return False

def sign(num):
    if num < 0:
        return -1
    else:
        return 1

def bishop(cur_square,target):
    cur_column = chessFiles.index(cur_square[0])
    cur_row = chessRows.index(cur_square[1])
    tar_column = chessFiles.index(target[0])
    tar_row = chessRows.index(target[1])

    diag_x = tar_column - cur_column
    diag_y =  tar_row - cur_row
    
    if abs(diag_x) == abs(diag_y):
        sign_x = sign(diag_x)
        sign_y = sign(diag_y)

        print(cur_column,tar_column)
        print(cur_row,tar_row)
        for dif in range(1,abs(diag_x)+1):
            #Check if squares between target and cur_square have pieces
            #in the way
            
            column = chessFiles[cur_column+(dif*sign_x)]
            row = chessRows[cur_row+(dif*sign_y)]
            
            piece = chessBoard[column+row]
            print(piece)
            print(dif,abs(diag_x))
            

            if piece != BLANK and dif != abs(diag_x):
                return False
            elif dif == abs(diag_x) and capture(cur_square,target):
                return True
            elif dif == abs(diag_x) and not capture(cur_square,target):
                return False

        return False
     
                
def get_piece_color(square):
    piece = chessBoard[square]
    if piece == BLANK:
        return False
    else:
        return piece[0]

def capture(sqr1,sqr2):
#Returns True if attacking piece can capture piece on sqr2
#sqr1 is attacking piece's square on the board, used to access the piece to find out what color it is
#sqr2 is the piece that is being attacked
    clr1 = get_piece_color(sqr1)
    clr2 = get_piece_color(sqr2)
    #if the pieces are different colors, then the attacking piece can capture
    if clr1 != clr2:
        print(clr1, clr2)
        return True
    else:
        return False
    
    
    
def remove_piece(chessBoard,square):
    chessBoard[square] = BLANK

def get_xy(square):
    if square == BLANK:
        return BLANK
    else:
        column = square[0]
        row = square[1]

        column = chessFiles.index(column)
        row = chessRows.index(row)

        x=column*squareWidth+boardTopLeftX
        y=row*squareHeight+boardTopLeftY

        return(x,y)
        
    
def boardDraw(chessBoard):
    gameDisplay.blit(board,(0,0))
    for square in chessBoard:
        piece = chessBoard[square]
        if piece == BLANK:
            continue
        elif cur_square == square:
            color = piece[0]
            piece = piece[1:]
            coord = get_xy(square)
    
            img = image.load(color+piece+'.png')
            img = transform.scale(img,(32,32))
            img.set_alpha(100)
            gameDisplay.blit(img,coord)
        else:
            
            color = piece[0]
            piece = piece[1:]
            coord = get_xy(square)
            if coord == BLANK:
                continue
            img = image.load(color+piece+'.png')
            img = transform.scale(img,(32,32))
            gameDisplay.blit(img,coord)

def pieceAtMousePos(chessBoard):
    #when mouse is clicked, pick up the piece in the square
    #the mouse is on.
    coord = mouse.get_pos()
    coordX = coord[0]
    coordY = coord[1]

    columnNum = (coordX - boardTopLeftX) // squareWidth 
    rowNum = (coordY - boardTopLeftY) // squareHeight 
    
    try:
        column = chessFiles[columnNum]
        row = chessRows[rowNum]
    except IndexError:
        return BLANK

    square = column+row
    
    return (chessBoard[square],square)
    

def pick_up():
    piece = pieceAtMousePos(chessBoard)
    global cur_square
    global cur_piece
    if piece_up == False:
        if piece[0] == BLANK:
            return False
        else:
            coord = mouse.get_pos()
            coordX = coord[0]-16
            coordY = coord[1]-16
            
            #remove_piece(chessBoard,piece[1])
            
            cur_square = piece[1]
            cur_piece = piece[0]
            img = image.load(piece[0]+'.png')
            img = transform.scale(img,(32,32))
            gameDisplay.blit(img,(coordX,coordY))
            return img
    else:
        coord = mouse.get_pos()
        coordX = coord[0]-16
        coordY = coord[1]-16
        
        gameDisplay.blit(piece_up,(coordX,coordY))
        return piece_up
        
def put_down(chessBoard):
    global cur_piece
    global cur_square
    target = pieceAtMousePos(chessBoard)
    target = target[1]

    can_move = bishop(cur_square,target)
    print(can_move)
    if can_move == True:
        chessBoard[target] = cur_piece
        remove_piece(chessBoard,cur_square)
    else:
        chessBoard[cur_square] = cur_piece
    
    cur_piece = BLANK
    cur_square = BLANK

    
display.init()
gameDisplay = display.set_mode([400,400])
board = image.load('chessBoard.png')
board = transform.scale(board,(400,400))

#GLOBAL VARS
BLANK = ' '
turn = True #True = white, False = black

boardTopLeftX = 48
boardTopLeftY = 48
squareWidth = 39
squareHeight = 39

#Is a piece currently being picked up?
piece_up = False

#If yes, what piece? What Square was it on?
cur_square = BLANK
cur_piece = BLANK


while True:
    event.get()
    MOUSE_STATE = mouse.get_pressed()
    LEFT_MOUSE = MOUSE_STATE[0]
    boardDraw(chessBoard)

    if LEFT_MOUSE:
        
        piece_up = pick_up()
        
    elif piece_up != False and LEFT_MOUSE == False:
        piece_up = False
        put_down(chessBoard)
        print(cur_square)
        
    
   
    display.update()
        
