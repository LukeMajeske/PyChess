from pygame import *
import os.path
filepath = os.path.dirname(__file__)


chessFiles = ['a','b','c','d','e','f','g','h']
chessRows = ['8','7','6','5','4','3','2','1']
chessPieces = ['Bishop','Knight','King','Queen','Pawn','Rook']
chessBoard = {'a8':'bRook','b8':'bKnight','c8':'bBishop','d8':'bQueen','e8':'bKing','f8':'bBishop','g8':'bKnight','h8':'bRook',
              'a7':'bPawn','b7':'bPawn','c7':'bPawn','d7':'bPawn','e7':' ','f7':' ','g7':'bPawn','h7':'bPawn',
              'a6':' ','b6':' ','c6':' ','d6':' ','e6':' ','f6':' ','g6':' ','h6':' ',
              'a5':' ','b5':' ','c5':' ','d5':' ','e5':' ','f5':' ','g5':' ','h5':' ',
              'a4':' ','b4':' ','c4':' ','d4':' ','e4':' ','f4':' ','g4':' ','h4':' ',
              'a3':' ','b3':' ','c3':' ','d3':' ','e3':' ','f3':' ','g3':' ','h3':' ',
              'a2':'wPawn','b2':'wPawn','c2':'wPawn','d2':' ','e2':'wPawn','f2':'wPawn','g2':'wPawn','h2':' ',
              'a1':'wRook','b1':'wKnight','c1':'wBishop','d1':'wQueen','e1':'wKing','f1':'wBishop','g1':'wKnight','h1':'wRook'}



class Piece:
    def __init__(self,square,color,piece):
        self.color = color
        self.square = square
        self.piece = piece
        self.img = image.load(color+piece+'.png')
        self.selected = False

    def draw(self):
        coord = get_xy(self.square)
        img = image.load(self.color+self.piece+'.png')
        img = transform.scale(img,(32,32))
        gameDisplay.blit(img,coord)

    def drawAlpha(self):
        coord = get_xy(self.square)
        img = image.load(self.color+self.piece+'.png')
        img = transform.scale(img,(32,32))
        img.set_alpha(100)
        gameDisplay.blit(img,coord)
        

    def drawAtMouse(self):
        coord = mouse.get_pos()
        coordX = coord[0]-16
        coordY = coord[1]-16
        img = image.load(self.color+self.piece+'.png')
        img = transform.scale(img,(32,32))
        gameDisplay.blit(img,(coordX,coordY))

    def move(self,square):
        global chessBoard
        if self.square != square:
            chessBoard[self.square]= BLANK
            
        chessBoard[square] = self
        self.square = square
        self.selected = False

    def delete(self):
        chessBoard[self.square] = BLANK

    def your_turn(self):
        global turn
        if self.color == 'w' and turn == True:
            return True
        elif self.color == 'b' and turn == False:
            return True
        else:
            return False
        
    
class Bishop(Piece):
    def moveSet(self,target):
        cur_column = chessFiles.index(self.square[0])
        cur_row = chessRows.index(self.square[1])
        tar_column = chessFiles.index(target[0])
        tar_row = chessRows.index(target[1])

        if self.square == target or not self.your_turn():
            return False

        diag_x = tar_column - cur_column
        diag_y =  tar_row - cur_row


        if abs(diag_x) == abs(diag_y):
            sign_x = sign(diag_x)
            sign_y = sign(diag_y)

           
            for dif in range(1,abs(diag_x)+1):
                #Check if squares between target and cur_square have pieces
                #in the way
                
                column = chessFiles[cur_column+(dif*sign_x)]
                row = chessRows[cur_row+(dif*sign_y)]
                
                piece = chessBoard[column+row]

                if piece != BLANK and dif != abs(diag_x):
                    return False
                elif dif == abs(diag_x) and capture(self.square,target):
                    self.move(target)
                elif dif == abs(diag_x) and not capture(self.square,target):
                    return False

            return False
        
class Rook(Piece):
    def moveSet(self,target):
        
        if self.square == target:
            return False
        
        cur_column = chessFiles.index(self.square[0])
        cur_row = chessRows.index(self.square[1])
        tar_column = chessFiles.index(target[0])
        tar_row = chessRows.index(target[1])
        

        if cur_column == tar_column or cur_row == tar_row:
            dif_x = tar_column - cur_column
            dif_y = tar_row - cur_row

            if dif_x != 0:
                dif = dif_x
            else:
                dif = dif_y
            sign_x = sign(dif_x)
            sign_y = sign(dif_y)
            for dist in range(1,abs(dif)+1):
                #Check if squares between target and cur_square have pieces
                #in the way
                
                column = chessFiles[cur_column+(dist*sign_x)]
                row = chessRows[cur_row+(dist*sign_y)]
                piece = chessBoard[column+row]
                

                if piece != BLANK and dist != abs(dif):
                    return False
                elif dist == abs(dif) and piece != BLANK:
                    
                    canCapture = capture(self.square,piece.square)
                
                    if canCapture:
                        self.move(target)
                    else:
                        return False

            ##If for loop conditions pass, then rook can also move to the target square
            self.move(target)
        
class Knight(Piece):
    def moveSet(self,target):
        
        if self.square == target:
            return False
        
        cur_column = chessFiles.index(self.square[0])
        cur_row = chessRows.index(self.square[1])
        tar_column = chessFiles.index(target[0])
        tar_row = chessRows.index(target[1])
        
        dif_x = abs(tar_column - cur_column)
        dif_y = abs(tar_row - cur_row)

        if (dif_x == 1 and dif_y == 2) or (dif_x == 2 and dif_y == 1):
            piece = chessBoard[target]
            
            if piece != BLANK:
                canCapture = capture(self.square,piece.square)
                if canCapture:
                    self.move(target)
                else:
                    
                    return False
            else:
                self.move(target)

class King(Piece):
    def moveSet(self,target):
        
        if self.square == target:
            return False
        
        cur_column = chessFiles.index(self.square[0])
        cur_row = chessRows.index(self.square[1])
        tar_column = chessFiles.index(target[0])
        tar_row = chessRows.index(target[1])
        
        
        dif_x = abs(tar_column - cur_column)
        dif_y = abs(tar_row - cur_row)

        if (dif_x == 0 or dif_x == 1) and (dif_y == 0 or dif_y == 1):
            piece = chessBoard[target]
            
            if piece != BLANK:
                canCapture = capture(self.square,piece.square)
                if canCapture:
                    self.move(target)
                else:
                    return False
            else:
                self.move(target)

            
class Queen(Piece):
    def moveSet(self,target):
        
        if self.square == target:
            return False
        ##MOVE STRAIGHT
        cur_column = chessFiles.index(self.square[0])
        cur_row = chessRows.index(self.square[1])
        tar_column = chessFiles.index(target[0])
        tar_row = chessRows.index(target[1])
        
        
        dif_x = abs(tar_column - cur_column)
        dif_y = abs(tar_row - cur_row)

        if cur_column == tar_column or cur_row == tar_row:
            dif_x = tar_column - cur_column
            dif_y = tar_row - cur_row

            if dif_x != 0:
                dif = dif_x
            else:
                dif = dif_y
            sign_x = sign(dif_x)
            sign_y = sign(dif_y)
            for dist in range(1,abs(dif)+1):
                #Check if squares between target and cur_square have pieces
                #in the way
                
                column = chessFiles[cur_column+(dist*sign_x)]
                row = chessRows[cur_row+(dist*sign_y)]
                
                piece = chessBoard[column+row]
                

                if piece != BLANK and dist != abs(dif):
                    return False
                elif dist == abs(dif) and piece != BLANK:
                    canCapture = capture(self.square,piece.square)
                    if canCapture:
                        self.move(target)
                    else:
                        return False
            self.move(target)

        ##MOVE DIAGONALS
        diag_x = tar_column - cur_column
        diag_y =  tar_row - cur_row


        if abs(diag_x) == abs(diag_y):
            sign_x = sign(diag_x)
            sign_y = sign(diag_y)

           
            for dif in range(1,abs(diag_x)+1):
                #Check if squares between target and cur_square have pieces
                #in the way
                
                column = chessFiles[cur_column+(dif*sign_x)]
                row = chessRows[cur_row+(dif*sign_y)]
                
                piece = chessBoard[column+row]
                

                if piece != BLANK and dif != abs(diag_x):
                    return False
                elif dif == abs(diag_x) and capture(self.square,target):
                    self.move(target)
                elif dif == abs(diag_x) and not capture(self.square,target):
                    return False
class Pawn(Piece):
    def promote(self,target):
        queen = Queen(target,self.color,"Queen")
        chessBoard[target] = queen
        self.delete()
        
    def moveSet(self,target):
        global chessBoard
        if self.color == "w":
            direction = -1
            home = 6
            promote = 0
        else:
            direction = 1
            home = 1
            promote = 7
        
        if self.square == target:
            return False
        
        cur_column = chessFiles.index(self.square[0])
        cur_row = chessRows.index(self.square[1])
        tar_column = chessFiles.index(target[0])
        tar_row = chessRows.index(target[1])
        
        
        dif_x = tar_column - cur_column
        dif_y = tar_row - cur_row

        ##MOVE FORWARD 1
        if dif_y == direction and dif_x == 0:
            piece = chessBoard[target]
            
            if piece != BLANK:
                return False
            else:
                if tar_row == promote:
                    self.promote(target)
                    
                else:
                    self.move(target)
                
        ##MOVE 2 FROM HOME SQUARE
        elif dif_y == 2*direction and dif_x == 0 and cur_row == home:
            piece = chessBoard[target]
            
            if piece != BLANK:
                return False
            else:
                self.move(target)
        ##CAPTURE PIECE
        elif dif_y == direction and abs(dif_x) == 1:
            piece = chessBoard[target]
            
            if piece != BLANK:
                canCapture = capture(self.square,target)
                if canCapture:
                    if tar_row == promote:
                        self.promote(target)
                    else:
                        self.move(target)
                else:
                    return False

        
        

def sign(num):
    if num < 0:
        return -1
    elif num == 0:
        return 0
    else:
        return 1


def boardInit(chessBoard):
    for square in chessBoard:
        piece = chessBoard[square]
        if piece[1:] == "Bishop":
            pieceObj = Bishop(square,piece[0],piece[1:])
            chessBoard[square] = pieceObj
        elif piece[1:] == "Rook":
            pieceObj = Rook(square,piece[0],piece[1:])
            chessBoard[square] = pieceObj
        elif piece[1:] == "Knight":
            pieceObj = Knight(square,piece[0],piece[1:])
            chessBoard[square] = pieceObj
        elif piece[1:] == "King":
            pieceObj = King(square,piece[0],piece[1:])
            chessBoard[square] = pieceObj
        elif piece[1:] == "Queen":
            pieceObj = Queen(square,piece[0],piece[1:])
            chessBoard[square] = pieceObj
        elif piece[1:] == "Pawn":
            pieceObj = Pawn(square,piece[0],piece[1:])
            chessBoard[square] = pieceObj
            
                
def get_piece_color(square):
    piece = chessBoard[square]
    if piece == BLANK:
        return False
    else:
        return piece.color

def capture(sqr1,sqr2):
#Returns True if attacking piece can capture piece on sqr2
#sqr1 is attacking piece's square on the board, used to access the piece to find out what color it is
#sqr2 is the piece that is being attacked
    clr1 = get_piece_color(sqr1)
    clr2 = get_piece_color(sqr2)
    if sqr2 == BLANK:
        return True
    #if the pieces are different colors, then the attacking piece can capture
    if clr1 != clr2:
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
        else:
            try:
                color = piece[0]
                piece = piece[1:]
                coord = get_xy(square)
                if coord == BLANK:
                    continue
                img = image.load(color+piece+'.png')
                img = transform.scale(img,(32,32))
                gameDisplay.blit(img,coord)
            except TypeError:
                piece.draw()
                

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
            
            
            
            cur_piece = piece[0]
            cur_piece.drawAtMouse()
            
            return cur_piece
    else:
        piece_up.drawAtMouse()
        return piece_up
        
def put_down(chessBoard):
    global cur_piece
    global turn
    target = pieceAtMousePos(chessBoard)
    target = target[1]

    if cur_piece.your_turn():
        cur_piece.moveSet(target)
        turn = not turn
    
    cur_piece = BLANK

    
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
cur_piece = BLANK


##MAIN PROGRAM
boardInit(chessBoard)
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
        
        
    
   
    display.update()
        
