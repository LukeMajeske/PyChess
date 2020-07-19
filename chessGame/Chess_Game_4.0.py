from pygame import *
import copy
import logging 
import os.path

logging.basicConfig(level = logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
#logging.disable(logging.DEBUG)



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
    def __init__(self,square,color,piece):
        self.color = color
        self.square = square
        self.piece = piece
        self.img = image.load(color+piece+'.png')
        self.selected = False
        self.blockable = True

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

    def move(self,square,possible = False):
        #if possible is True, then do not make the move. Only return True if the move is "Possible" to make
        global chessBoard
        global cur_piece, turn
        
        prevBoardState = copy.copy(chessBoard)
        prev_square = self.square
            
            
        if self.square != square:
            chessBoard[self.square]= BLANK
            
        chessBoard[square] = self
        self.square = square
        self.selected = False

        check = checkForChecks()
        if check == True:
            self.square = prev_square
            chessBoard = prevBoardState
            return False
        else:
            if possible == True:
                self.square = prev_square
                chessBoard = prevBoardState
                return True
            else:
                if self.piece == "King":
                    self.moved == True
                turn = not turn
                cur_piece = BLANK
                return True   

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

        if self.square == target:
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
                    #self.move(target)
                    return True
                elif dif == abs(diag_x) and not capture(self.square,target):
                    return False
        else:
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
                        #self.move(target)
                        return True
                    else:
                        return False

            ##If for loop conditions pass, then rook can also move to the target square
            #self.move(target)
            return True
        else:
            return False
        
class Knight(Piece):
    def __init__(self,square,color,piece):
        super().__init__(square,color,piece)
        self.blockable = False
        
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
                    #self.move(target)
                    return True
                else:
                    
                    return False
            else:
                #self.move(target)
                return True
        else:
            return False


class King(Piece):
    def __init__(self,square,color,piece):
        super().__init__(square,color,piece)
        self.moved = False
        self.castleMove = False
        
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
                logging.debug(canCapture)
                if canCapture:
                    #self.move(target)
                    return True
                else:
                    return False
            else:
                #self.move(target)
                return True
        else:
            ##CHECK IF MOVE IS FOR CASTLING
            castling = self.castle(target)

            return castling

    def move(self,square,possible = False):
        #if possible is True, then do not make the move. Only return True if the move is "Possible" to make
        global chessBoard
        global cur_piece, turn
        
        prevBoardState = copy.copy(chessBoard)
        prev_square = self.square
            
            
        if self.square != square:
            chessBoard[self.square]= BLANK
            
        chessBoard[square] = self
        self.square = square
        self.selected = False

        check = checkForChecks()
        if check == True:
            self.square = prev_square
            chessBoard = prevBoardState
            return False
        else:
            if possible == True:
                self.square = prev_square
                chessBoard = prevBoardState
                return True
            else:
                if self.castleMove == False:
                    pass
                elif self.castleMove[1] == 1:
                    rook = self.castleMove[0]
                    leftOfKing = "f"+self.square[1]
                    chessBoard[leftOfKing] = rook
                    chessBoard[rook.square] = BLANK
                    rook.square = leftOfKing
                    

                elif self.castleMove[1] == -1:
                    rook = self.castleMove[0]
                    rightOfKing = "d"+self.square[1]
                    chessBoard[rightOfKing] = rook
                    chessBoard[rook.square] = BLANK
                    rook.square = rightOfKing
                    
                    
                self.moved == True
                turn = not turn
                cur_piece = BLANK
                return True   

    def inCheck(self):
        #Returns True if king is in check
        global chessBoard
        for piece in chessBoard.values():
            
            if piece == BLANK:
                continue
            elif piece.color != self.color and piece.piece != "King":
                check = piece.moveSet(self.square)
                if check == True:
                    return True
                else:
                    continue
        return False
    
    def checkingPieces(self):
        #Returns all pieces that are checking the king in a list
        global chessBoard
        pieces = []
        for piece in chessBoard.values():
            
            if piece == BLANK:
                continue
            elif piece.color != self.color:
                check = piece.moveSet(self.square)
                if check == True:
                    pieces.append(piece)
                else:
                    continue
        return pieces

    def checkmate(self):
        global chessBoard

        if not self.inCheck():
            return False

        #Check squares around King, if king can move to any one then it is not checkmate
        cur_row = chessRows.index(self.square[1])
        cur_column = chessFiles.index(self.square[0])

        for row in range(-1,2):
            for column in range(-1,2):
                if row == 0 and column == 0:
                    continue
                #Target row in column in number form
                tar_row = cur_row + row
                tar_column = cur_column + column
                
                #Convert to string
                try:
                    tar_row = chessRows[tar_row]
                    tar_column = chessFiles[tar_column]
                except IndexError:
                    continue

                target = tar_column + tar_row

                #If king is able to move to the target square and not be in check, then there is no checkmate
                if self.moveSet(target):
                    if self.move(target, True):
                        logging.debug("King can move to "+target)
                        return False
                    

        #If king cant move, then check if the checking piece can be captured
        #If there are 2+ pieces checking the king then the king is in checkmate
        cpieces = self.checkingPieces()
        if len(cpieces) >= 2:
            return True

        cpiece_square = cpieces[0].square

        for piece in chessBoard.values():
            if piece == BLANK:
                continue
            if piece.color == self.color:
                if piece.moveSet(cpiece_square):
                    if piece.move(cpiece_square,True):
                        logging.debug("CHECKING PIECE CAN BE CAPTURED!!")
                        return False

                else:
                    continue

        #Can the checking piece be blocked?
        if cpieces[0].blockable == False:
            logging.debug("Attack cannot be blocked")
            return True

        block_column = chessFiles.index(self.square[0])
        block_row = chessRows.index(self.square[1])
        cpiece_column = chessFiles.index(cpiece_square[0])
        cpiece_row = chessRows.index(cpiece_square[1])

        blockingSquares = []
        while block_column != cpiece_column and block_row != cpiece_row:
        
            if block_column == cpiece_column:
                pass
            elif block_column > cpiece_column:
                block_column -= 1
            else:
                block_column += 1

            if block_row == cpiece_row:
                pass
            elif block_row > cpiece_row:
                block_row -= 1
            else:
                block_row += 1

            blockSquare = chessFiles[block_column] + chessRows[block_row]
            blockingSquares.append(blockSquare)
            logging.debug(blockingSquares)

        for piece in chessBoard.values():
            if piece == BLANK:
                continue
            if piece.color == self.color:
                for block in blockingSquares:
                    if piece.moveSet(block):
                        if piece.move(block,True):
                            logging.debug("CHECKING PIECE CAN BE BLOCKED!!")
                            return False

            else:
                continue
            
        return True
                        

    def castle(self,target):
        global chessBoard
        
        if self.moved == True:
            return False

        elif self.inCheck() == True:
            return False

        cur_row = chessRows.index(self.square[1])
        cur_column = chessFiles.index(self.square[0])
        tar_row = chessRows.index(target[1])
        tar_column = chessFiles.index(target[0])

        dif = tar_column - cur_column
        direction = sign(dif)
        
        if cur_row == tar_row and abs(dif) == 2:
            
            squares= []
            for colCheck in range(1,3):
                column = cur_column
                column = column + (direction*colCheck)
                columnControlled = chessFiles[column]
                square = columnControlled + target[1]
                logging.debug(colCheck)
                if chessBoard[square] != BLANK:
                    logging.debug("CAN'T CASTLE, PIECE IN THE WAY ON SQUARE "+square)
                    return False
                squares.append(square)

                

            for piece in chessBoard.values():
                for square in squares:
                    if piece == BLANK:
                        continue
                    if piece.color != self.color and piece.piece != "King":
                        controlled = piece.moveSet(square)

                        if controlled == True:
                            return False
                        else:
                            continue
            ##RETURN ROOK TO CASTLE WITH
            if direction == 1:
                rookColumn = chessFiles[cur_column + 3]
                rookSquare = rookColumn + self.square[1]
                rook = chessBoard[rookSquare]
            if direction == -1:
                rookColumn = chessFiles[cur_column - 4]
                rookSquare = rookColumn + self.square[1]
                rook = chessBoard[rookSquare]
                
            if rook != BLANK and rook.piece == "Rook" and rook.color == self.color:
                self.castleMove = (rook,direction)
                return True

            else:
                return False     
                
        else:
            return False
        
        
    
                
                 


            
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
                        #self.move(target)
                        return True
                    else:
                        return False

            ##If for loop conditions pass, then queen can also move to the target square
            return True

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
                    #self.move(target)
                    return True
                elif dif == abs(diag_x) and not capture(self.square,target):
                    return False
        else:
            return False

    
class Pawn(Piece):
    def __init__(self,square,color,piece):
        super().__init__(square,color,piece)
        self.blockable = False
        self.enpassant = False #Is true if you can perform enpassant
        if self.color == "w":
            self.direction = -1
            self.home = 6
            self.promoteRow = 0
        else:
            self.direction = 1
            self.home = 1
            self.promoteRow = 7
        
    def promote(self,target):
        queen = Queen(target,self.color,"Queen")
        chessBoard[target] = queen
        
        
    def moveSet(self,target):
        global chessBoard
        
        
        if self.square == target:
            return False
        
        cur_column = chessFiles.index(self.square[0])
        cur_row = chessRows.index(self.square[1])
        tar_column = chessFiles.index(target[0])
        tar_row = chessRows.index(target[1])
        
        
        dif_x = tar_column - cur_column
        dif_y = tar_row - cur_row

        ##MOVE FORWARD 1
        if dif_y == self.direction and dif_x == 0:
            piece = chessBoard[target]
            
            if piece != BLANK:
                return False
            else:
                return True
                
        ##MOVE 2 FROM HOME SQUARE
        elif dif_y == 2*self.direction and dif_x == 0 and cur_row == self.home:
            piece = chessBoard[target]
            
            if piece != BLANK:
                return False
            else:
                return True
        #ENPASSANT
        elif self.enpassant != False:
            logging.debug("ENPASSANT")
            epawn = self.enpassant
            epawnRow = chessRows.index(epawn.square[1])
            if epawnRow - epawn.direction == tar_row:
                return True
            else:
                return False
            
        
        ##CAPTURE PIECE
        elif dif_y == self.direction and abs(dif_x) == 1:
            piece = chessBoard[target]
            
            if piece != BLANK:
                canCapture = capture(self.square,target)
                if canCapture:  
                    return True
                else:
                    return False

        else:
            return False
    def enpassantMove(self,target):
        global chessBoard
        tar_row = chessRows.index(target[1])
        if self.enpassant != False:
            logging.debug("ENPASSANT")
            epawn = self.enpassant
            epawnRow = chessRows.index(epawn.square[1])
            if epawnRow - epawn.direction == tar_row:
                chessBoard[epawn.square] = BLANK
                return True
            else:
                return False
        
    def move(self,square,possible = False):
            #if possible is True, then do not make the move. Only return True if the move is "Possible" to make
            global chessBoard
            global cur_piece, turn
            
            prevBoardState = copy.copy(chessBoard)
            prev_square = self.square
                
            logging.debug("MOVING") 
            if self.square != square:
                chessBoard[self.square]= BLANK
                
            chessBoard[square] = self
            self.square = square
            self.selected = False

            check = checkForChecks()

            #If your king is in check after you move, then you can't move
            if check == True:
                self.square = prev_square
                chessBoard = prevBoardState
                return False
            else:
                   
                if possible == True:
                    self.square = prev_square
                    chessBoard = prevBoardState
                    return True

                
                
                
                cur_row = self.square[1]
                cur_row = chessRows.index(cur_row)
                prev_row = chessRows.index(prev_square[1])
                #Did the pawn move 2 squares? If yes, then check for enpassant
                if abs(cur_row - prev_row) == 2:
                    cur_column = self.square[0]
                    cur_column= chessFiles.index(cur_column)
                    cur_row = self.square[1]
                    
                    try:
                        right = chessFiles[cur_column+1] + cur_row
                    except IndexError:
                        right = None
                    
                    try:
                        left = chessFiles[cur_column-1] + cur_row
                    except IndexError:
                        left = None
                    
                    if  left == None or  chessBoard[left] == BLANK :
                        logging.debug("BLANK")
                    elif chessBoard[left].piece == 'Pawn' and chessBoard[left].color != self.color:
                        chessBoard[left].enpassant = self

                    if right == None or chessBoard[right] == BLANK:
                        logging.debug("BLANK")
                    elif chessBoard[right].piece == 'Pawn' and chessBoard[right].color != self.color:
                        chessBoard[right].enpassant = self
                    
                    

                #Can this pawn perform enpassant?
                self.enpassantMove(square)
                #Can the Pawn promote?
                if cur_row == self.promoteRow:
                    logging.debug("PROMOTE!!!")
                    self.promote(self.square)

                self.enpassant = False
                turn = not turn
                cur_piece = BLANK
                return True   
       

        
        

def sign(num):
    if num < 0:
        return -1
    elif num == 0:
        return 0
    else:
        return 1


def boardInit(chessBoard):
    global whiteKing
    global blackKing
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
            if piece[0] == 'w':
                whiteKing = pieceObj
            else:
                blackKing = pieceObj
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
        logging.debug("Blank Square")
        return True
    #if the pieces are different colors, then the attacking piece can capture
    if clr1 != clr2:
        logging.debug("Different Colors")
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


def checkForChecks():
    global turn
    if turn == True:
        return whiteKing.inCheck()
    else:
        return blackKing.inCheck()
    

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
        
def put_down():
    global chessBoard
    global cur_piece
    global turn
    target = pieceAtMousePos(chessBoard)
    target = target[1]

    if cur_piece.your_turn():
        cur_square = cur_piece.square
        move = cur_piece.moveSet(target)
        assert move == True or move == False
        if move == True:
            cur_piece.move(target)
            return True
        else:
            return False
        
           




  
display.init()
gameDisplay = display.set_mode([400,400])
board = image.load('chessBoard.png')

board = transform.scale(board,(400,400))

#GLOBAL VARS
BLANK = ' '
turn = True #True = white, False = black
whiteKing = 0
blackKing = 0
checkmate = False

boardTopLeftX = 48
boardTopLeftY = 48
squareWidth = 39
squareHeight = 39

#Is a piece currently being picked up?
piece_up = False

#If yes, what piece? What Square was it on?
cur_piece = BLANK


##MAIN PROGRAM
logging.debug('Start of Program')
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
        moveWasMade = put_down()

        if moveWasMade == True:
            if turn == True:
                checkmate = whiteKing.checkmate()
                win = "Black"
            else:
                checkmate = blackKing.checkmate()
                win = "White"
        if checkmate == True:
            print(win + " wins by checkmate!")
        
    
   
    display.update()
        
