from tkinter import *

class CheckersSquare(Canvas):
    '''displays a square in the Checkers game'''

    def __init__(self,master,r,c,color,hcolor='color'):
        '''CheckersSquare(master,r,c,color,hcolor='color') -> CheckersSquare
        creates a new blank Checkers square at coordinate (r,c)'''
        # if hcolor was not defined
        if hcolor == 'color':
            # set it to the backgroud color
            hcolor = color
        # create and place the widget
        Canvas.__init__(self,master,width=53,\
                        height=53,bg=color,highlightbackground=hcolor,highlightthickness=4)
        self.grid(row=r,column=c)
        # set up the attributes
        self.is_king = False
        self.board = master
        self.position = (r,c)
        self.active = False
        self.hasPiece = False
        self.color = color
        self.pieceColor = 'None'
        # bind button click to selecting the square
        self.bind('<Button>',self.select)

    def get_position(self):
        '''CheckersSquare.get_position() -> (int,int)
        returns (row,column) of square'''
        return self.position

    def piece_color(self):
        '''CheckersSquare.piece_color() -> str
        preturns the color of the piece
        'None' if no piece'''
        return self.pieceColor

    def take_piece(self,color,king=False):
        '''CheckersSquare.take_piece(color,king=False)
        puts a color piece on square'''
        self.pieceColor = color
        self.hasPiece = True
        self.create_oval(9,9,50,50,fill=color)
        self.piece = color
        self.is_king = king
        # if the piece has become a king or is already a king
        if (self.position[0] == 0 and self.pieceColor == 'white') or \
           (self.position[0] == 7 and self.pieceColor == 'red') or self.is_king:
            self.is_king = True
            # draw the '*' over the piece
            self.create_text(30.49,39.3,font=('Arial',35,'bold'),fill='black',text='*')

    def remove_piece(self):
        '''CheckersSquare.remove_piece()
        deletes piece'''
        ovalList = self.find_all() # find piece
        for oval in ovalList:
            self.delete(oval) # delete it
        self.hasPiece = False
        self.pieceColor = 'None'
        self.is_king = False

    def set_active(self,tf):
        '''CheckersSquare.set_active(tf)
        sets active to tf where tf is a boolean'''
        self.active = tf

    def select(self,xy):
        '''CheckersSquare.select(xy)
        hadler for button
        if square is active, highlights and signals master board'''
        if self.active:
            self['highlightbackground'] = 'black'
            self.board.select_send(self.position) # call master

    def unhighlight(self):
        '''CheckersSquare.tunhighlight()
        unhighlights square'''
        self['highlightbackground'] = self.color

class CheckersBoard(Frame):
    '''object for a Checkers board'''
    def __init__(self,master):
        '''CheckersSquare(self,master) -> CheckersBoard
        creates a new blank Checkers board'''
        Frame.__init__(self,master,bg='white')
        self.grid()
        # set up variables
        self.playerColors = {1:'red', -1:'white'}
        self.playerNum = 1
        self.pieceToMove = None
        self.placeToMove = None
        # make label for turn
        self.turnLabel = Label(self,text="Turn:",font=('Arial',15),bg='white')
        self.turnLabel.grid(row=10,column=1, columnspan=1)
        self.turnIcon = CheckersSquare(self,10,2,'light grey',hcolor='white')
        self.turnIcon.active = False
        # make label for double jumping
        self.djl = Label(self,text='Must continue to jump!',font=('Arial',15),bg='white')
        self.djl.grid(row=10,column=4,columnspan=5)
        self.djl.grid_remove()
        # make draw button
        self.drawb = Button(self,text='Draw',command=self.draw)
        self.drawb.grid(row=10,column=0,columnspan=1)
        # create squares
        self.squares = {}
        for row in range(8):
            for column in range(8):
                if (row+column)%2==0:
                    color = "blanched almond"
                else:
                    color = "dark green"
                self.squares[(row,column)] = CheckersSquare(self,row,column,color)
        # give them pieces
        for pos in self.squares:
            if pos in [(0,1),(0,3),(0,5),(0,7),\
                       (1,0),(1,2),(1,4),(1,6),\
                       (2,1),(2,3),(2,5),(2,7)]:
                self.squares[pos].take_piece('red')
            if pos in [(5,0),(5,2),(5,4),(5,6),\
                       (6,1),(6,3),(6,5),(6,7),\
                       (7,0),(7,2),(7,4),(7,6)]:
                self.squares[pos].take_piece('white')
        self.update('find active pieces')

    def update(self,instructions,onlyJumps=False):
        '''update(instructions,onlyJumps=False)
        sets squares to be active or inactive, checks for end of game'''
        self.turnIcon.take_piece(self.playerColors[self.playerNum])
        if instructions == 'find active pieces':
            # finds pieces for the current player that have moves and makes them active
            ableToMove = False # for if no piece has a move
            ableToJump = False
            # looking for jumps
            for pos in self.squares:
                square = self.squares[pos]
                square.set_active(False)
                # if the square has a piece, can jump, and is the right color
                if square.hasPiece and square.pieceColor == self.playerColors[self.playerNum]:
                    if len(self.moves(pos,True)) != 0:
                        ableToJump = True
                        ableToMove = True # player does have a move
                        square.set_active(True)
            # looking for any move
            if not ableToJump:
                for pos in self.squares:
                    square = self.squares[pos]
                    square.set_active(False)
                    # if the square has a piece, can move, and is the right color
                    if square.hasPiece and square.pieceColor == self.playerColors[self.playerNum]:
                        if len(self.moves(pos,False)) != 0:
                            ableToMove = True # player does have a move
                            square.set_active(True)
            if not ableToMove:
                self.end_game('Congratulations -- '+self.playerColors[-self.playerNum]+' won!')
        elif instructions == 'find places':
            for pos in self.squares:
                self.squares[pos].set_active(False)
            # finds places that will take the piece to move and makes them active
            validPlaces = self.moves(self.pieceToMove,onlyJumps=True)
            if len(validPlaces) == 0:
                validPlaces = self.moves(self.pieceToMove,onlyJumps=False)
            for pos in validPlaces:
                self.squares[pos].set_active(True)

    def end_game(self,message):
        '''end_game(winner)
        opens pop-up window displaying message for winner'''
        messagebox.showinfo('Checkers',message,parent=self)

    def draw(self):
        self.end_game("It was a tie!")
            
    def moves(self,pos,onlyJumps=False):
        '''moves(pos,onlyJumps=False) -> list
        returns a list of possible moves for a square'''
        row = pos[0]
        column = pos[1]
        color = self.squares[pos].piece_color()
        if color == 'red':
            rChange = 1
        if color == 'white':
            rChange = -1
        validSteps = []
        validJumps = []
        simpleMoves = [(row+rChange,column+1),(row+rChange,column-1)]
        jumpingMoves = [(row+2*rChange,column+2),(row+2*rChange,column-2)]
        # if king add to simple and jumping moves
        if self.squares[pos].is_king:
            simpleMoves.append((row-rChange,column+1))
            simpleMoves.append((row-rChange,column-1))
            jumpingMoves.append((row-2*rChange,column+2))
            jumpingMoves.append((row-2*rChange,column-2))
        for i in range(len(simpleMoves)):
            # try simple move
            if simpleMoves[i] in self.squares:
                if self.squares[simpleMoves[i]].hasPiece:
                    # try jumping move
                    if jumpingMoves[i] in self.squares:
                        # if the square doesn't have a piece and
                        # the square that will be jumped over is the oppisite color
                        if (not self.squares[jumpingMoves[i]].hasPiece) and \
                           self.squares[simpleMoves[i]].pieceColor != self.playerColors[self.playerNum]:
                            # add square to valid jumping moves
                            validJumps.append(jumpingMoves[i])
                else: # if it doesn't have a piece
                    validSteps.append(simpleMoves[i])
        if len(validJumps) > 0 or onlyJumps:
            # if a square can jump, it has to
            # also can only return jumping moves for a double jump
            return validJumps
        else:
            return validSteps

    def select_send(self,pos):
        '''select_send(pos)
        processes a user's click to move a piece or select a piece to be moved'''
        if self.pieceToMove == None: # if no piece to move has been selected
            # set it to the position of the square that was clicked
            self.pieceToMove = pos
            # unhighlight and delete old placeToMove if it exists
            if self.placeToMove != None:
                self.squares[self.placeToMove].unhighlight()
                self.placeToMove = None
            # update squares in finding places for piece to move to go
            self.update('find places')
        else:
            self.placeToMove = pos
            # add a piece to one square and remove it from the other
            self.squares[self.placeToMove].take_piece(self.playerColors[self.playerNum],\
                                                      self.squares[self.pieceToMove].is_king)
            self.squares[self.pieceToMove].remove_piece()
            dj = False # if piece can double jump
            if abs(pos[0] - self.pieceToMove[0])==2:
                # it is a jump so remove the piece that was jumped over
                self.squares[((self.placeToMove[0]+self.pieceToMove[0])/2,\
                              (self.placeToMove[1]+self.pieceToMove[1])/2)].remove_piece()
                # look for moves in jump only mode
                if len(self.moves(self.placeToMove,True)) > 0:
                    # if there are moves, piece must double jump, so display message
                    dj = True
                    self.djl.grid()
                    self.squares[self.pieceToMove].unhighlight()
                    self.pieceToMove = self.placeToMove
                    self.update('find places',True)
            if not dj:
                self.squares[self.pieceToMove].unhighlight()
                self.pieceToMove = None
                self.playerNum *= -1
                self.update('find active pieces')
                self.djl.grid_remove()
        
def play_checkers():
    root = Tk()
    root.title('Checkers')
    CG = CheckersBoard(root)
    CG.mainloop()

play_checkers()
