# Python Class 1011
# Lesson 10 Problem 1
# Author: cinamon (172094)

from tkinter import *
import random
import sys
sys.setrecursionlimit(56000)

class MinesweeperCell(Label):
    '''represents a Minesweeper cell'''

    def __init__(self,master,coord):
        '''MinesweeperCell(master,coord) -> MinesweeperCell
        creates a new blank MinesweeperCell with (row,column) coord'''
        Label.__init__(self,master,height=1,width=2,text='',\
                       bg='white',font=('Arial',18), relief='raised')
        self.grid(row=coord[0], column=coord[1])
        # create starting variables
        self.master = master
        self.coord = coord
        self.colormap = ['gray','blue','darkgreen','red','purple',\
                         'maroon','cyan','black','yellow']
        self.num = 0
        self.isBomb = False
        self.isRevealed = False
        self.isFlagged = False
        # set up listeners
        self.bind('<Button-1>',self.reveal)
        self.bind('<Button-3>',self.flag)
        
    def get_num(self):
        '''MinesweeperCell.get_num() -> int
        returns the number of bombs near cell and sets that to self.num'''
        self.num = 0
        # get the list of cells that surround self
        self.surrounding = self.master.get_surrounding(self.coord)
        for cell in self.surrounding:
            # add 1 if the cell is a bomb
            if cell.is_bomb():
                self.num += 1
        return self.num

    def make_bomb(self):
        '''MinesweeperCell.make_bomb()
        turns cell into a bomb'''
        self.isBomb = True

    def flag(self, coord):
        '''MinesweeperCell.flag()
        if cell is not revealed
        will add a * if cell does not have one
        will take away * if cell does have one'''
        # will only allow you to flag if it isn't revealed
        if not self.isRevealed:
            # if it is already flagged
            if self['text']=='*':
                # unflag and add 1 back to bomb count
                self['text'] = ''
                self.master.bomb_count(1)
                self.isFlagged = False
            else:
                # flag and subtract 1 from bomb count
                self['text'] = '*'
                self.master.bomb_count(-1)
                self.isFlagged = True

    def reveal(self,coord='place holder'):
        '''MinesweeperCell.reveal(coord='place holder')
        if not a bomb
        reveals its number
        if its number is 0
        reveals surrounding cells'''
        # if the player has clicked a bomb the player loses
        if self.isBomb:
            self.master.lose()
        # if the cell is valid to reveal
        elif not self.isRevealed and not self.isFlagged:
            self['text'] = self.num # show the number of bombs near it
            self['relief'] = 'sunken'
            self['fg'] = self.colormap[self.num]
            self['bg'] = 'gray'
            self.isRevealed = True
            self.master.check_win()
            if self.num == 0:
                self.reveal_surrounding()

    def reveal_surrounding(self):
        '''MinesweeperCell.reveal_surrounding()
        reveals the numbers on surrounding cells'''
        for cell in self.surrounding:
            cell.reveal()

    def get_coord(self):
        '''MinesweeperCell.get_coord() -> tuple
        returns cell's coordinates in the grid'''
        return self.coord

    def is_bomb(self):
        '''MinesweeperCell.is_bomb() -> boolean
        returns True if cell is a bomb, False if not'''
        return self.isBomb

    def is_flagged(self):
        '''MinesweeperCell.is_flagged() -> boolean
        returns True if cell is flagged, False if not'''
        return self.isFlagged

    def is_revealed(self):
        '''MinesweeperCell.is_revealed() -> boolean
        returns True if cell is revealed, False if not'''
        return self.isRevealed
    
class MinesweeperGrid(Frame):
    '''object for a Minesweeper grid'''
    def __init__(self,master,width,height,numBombs):
        '''MinesweeperGrid(self,master,width,height,numBombs) -> MinesweeperGrid
        creates a width by height window for Minesweeper with numBombs hidden bombs'''
        Frame.__init__(self,master,bg='black')
        # set up variables
        self.grid()
        self.width = width
        self.height = height
        self.numBombs = numBombs
        self.bombsLeft = numBombs
        # make label for bomb count
        self.countLabel = Label(self,text=self.numBombs,font=('Arial',24))
        self.countLabel.grid(row=height+1,column=0, columnspan=width)
        # create cells
        self.cells = []
        for row in range(self.height):
            for column in range(self.width):
                coord = (row,column)
                self.cells.append(MinesweeperCell(self,coord))
        # make some of them bombs
        toBeBombs = random.sample(self.cells, numBombs)
        for cell in toBeBombs:
            cell.make_bomb()
        # now that there are bombs, calculate each cells number
        for cell in self.cells:
            cell.get_num()

    def get_surrounding(self,coord):
        '''MinesweeperGrid.get_surrounding(coord) -> list
        returns a list of surrounding MinesweeperCells'''
        surrounding = []
        # get the row and column separately
        r = coord[0]
        c = coord[1]
        # create a match list, a list of coordinates that surround the cell,
        # including the cell's coordinates
        matchList = []
        for row in [r-1,r,r+1]:
            for column in [c-1,c,c+1]:
                matchList.append((row,column))
        # check each cell to see if its coordinates match that in matchList
        for cell in self.cells:
            # if it does, add it to surrounding list
            if cell.get_coord() in matchList:
                surrounding.append(cell)
        return surrounding

    def bomb_count(self,num):
        '''MinesweeperGrid.bomb_count(num)
        adds num to bombsLeft and displays'''
        self.bombsLeft += num # add num
        self.countLabel['text'] = str(self.bombsLeft) # display

    def check_win(self):
        '''MinesweeperGrid.check_win()
        checks for win, if player has won, shows winning window'''
        # used to have if bombsleft=0
        revealed = 0
        # count the number of revealed cells
        for cell in self.cells:
            if cell.is_revealed():
                revealed += 1
        # if that is equall to the number of cells that are not bombs 
        if revealed == self.width*self.height-self.numBombs:
            self.win() # show winning message

    def lose(self):
        '''MinesweeperGrid.lose()
        shows losing window and shows bombs in red'''
        # show losing message window
        messagebox.showerror('Minesweeper','KABOOM! You lose.',parent=self)
        # show bombs in red
        for cell in self.cells:
            if cell.is_bomb():
                cell['text'] = '*'
                cell['bg'] = 'red'
        
    def win(self):
        '''MinesweeperGrid.win()
        shows winningwindow'''
        messagebox.showinfo('Minesweeper','Congratulations -- you won!',parent=self)

def play_minesweeper(width, height, numBombs):
    root = Tk()
    root.title('Minesweeper')
    mg = MinesweeperGrid(root,width,height,numBombs)
    root.mainloop()

play_minesweeper(12,10,15)
