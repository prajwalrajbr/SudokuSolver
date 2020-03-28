import requests
import json
from copy import deepcopy
from random import choice
from tkinter import *
#import timeit
#start = timeit.default_timer()

# api_URL = http://www.cs.utep.edu/cheon/ws/sudoku/new/[?size][&level]

class sudokuSolver:

    def getBoard(self):
        global board
        level = int(input("ENTER THE DIFFICULTY LEVEL:\n1 = EASY\n2 = MEDIUM\n3 = HARD\n"))

        if level in [1,2,3]:
            try:
                res = False
                api_request = requests.get("http://www.cs.utep.edu/cheon/ws/sudoku/new/?size=9&level="+str(level))
                api = json.loads(api_request.content)
                res = api['response']
            except:
                pass

            if res:
                if api['response']:
                    #Clear the content of board
                    for i in range(0,9):
                        for j in range(0,9):
                            board[i][j]=0

                    for i in range(0,len(api['squares'])):
                        board[api['squares'][i]['x']][api['squares'][i]['y']]=api['squares'][i]['value']
            
            else:
                values=[1,2,3,4,5,6,7,8,9]
                #Enter any random values from 1 to 9 for the 1st row
                for i in range(0,9):
                    board[0][i] = choice(values)
                    values.remove(board[0][i])
                #Right shift 3 times for both the 2nd and 3rd row
                for i in range(1,3):    
                    for j in range(0,9):
                        board[i][j] = board[i-1][(j+3)%9]
                #Right shift 1 time for 4th row
                for i in range(0,9):
                    board[3][i] = board[2][(i+1)%9]
                #Right shift 3 times for both the 5th and 6th row
                for i in range(4,6):    
                    for j in range(0,9):
                        board[i][j] = board[i-1][(j+3)%9]
                #Right shift 1 time for 7th row
                for i in range(0,9):
                    board[6][i] = board[5][(i+1)%9]
                #Right shift 3 times for both the 8th and 9th row
                for i in range(7,9):    
                    for j in range(0,9):
                        board[i][j] = board[i-1][(j+3)%9]
                
                #Rotate the board randomly to hide shifting
                tempBoard=deepcopy(board)
                for k in range(0,choice([1,2,3])):
                    for i in range(0,9):
                        for j in range(0,9):
                            board[i][j]=tempBoard[j][8-i]

                #Delete the variable tempboard
                del tempBoard

                values=[0,1,2,3,4,5,6,7,8]
                #No. of empty spaces = 30 for EASY
                if level==1:
                    for i in range(0,30):
                        r = choice(values)
                        c = choice(values)
                        if board[r][c]==0:
                            i = i-1
                        else:
                            board[r][c]=0
                #No. of empty spaces = 45 for MEDIUM
                elif level==2:
                    for i in range(0,45):
                        r = choice(values)
                        c = choice(values)
                        if board[r][c]==0:
                            i = i-1
                        else:
                            board[r][c]=0
                #No. of empty spaces = 60 for HARD
                else:
                    for i in range(0,60):
                        r = choice(values)
                        c = choice(values)
                        if board[r][c]==0:
                            i = i-1
                        else:
                            board[r][c]=0
   
    def findEmpty(self):
        #Check for the value 0
        for i in range(0,9):
            for j in range(0,9):
                if board[i][j]==0:
                    return i,j

    def solve(self):
        global board 
        x=self.findEmpty()
        if x:
            row,col=x
        else:
            return True

        #Insert 1 to 9 to the position of 0
        for i in range(1,10):
            if self.checkIfValid(i,row,col):
                board[row][col]=i
                if self.solve():
                    return True
                board[row][col]=0
        return False
                  
    def checkIfValid(self,value,row,col):
        global board
        #Row checker
        for i in range(0,9):
            if board[i][col]==value:
                return False

        #Column checker
        for i in range(0,9):
            if board[row][i]==value:
                return False

        #Corresponding 3X3 box checker
        if row%3==0:
            if col%3==0:
                for i in [row,row+1,row+2]:
                    for j in [col,col+1,col+2]:
                        if board[i][j]==value:
                            return False
            elif col%3==1:
                for i in [row,row+1,row+2]:
                    for j in [col-1,col,col+1]:
                        if board[i][j]==value:
                            return False
            else:
                for i in [row,row+1,row+2]:
                    for j in [col-2,col-1,col]:
                        if board[i][j]==value:
                            return False
        elif row%3==1:
            if col%3==0:
                for i in [row-1,row,row+1]:
                    for j in [col,col+1,col+2]:
                        if board[i][j]==value:
                            return False       
            elif col%3==1:
                for i in [row-1,row,row+1]:
                    for j in [col-1,col,col+1]:
                        if board[i][j]==value:
                            return False
            else:
                for i in [row-1,row,row+1]:
                    for j in [col-2,col-1,col]:
                        if board[i][j]==value:
                            return False
        else:
            if col%3==0:
                for i in [row-2,row-1,row]:
                    for j in [col,col+1,col+2]:
                        if board[i][j]==value:
                            return False       
            elif col%3==1:
                for i in [row-2,row-1,row]:
                    for j in [col-1,col,col+1]:
                        if board[i][j]==value:
                            return False
            else:
                for i in [row-2,row-1,row]:
                    for j in [col-2,col-1,col]:
                        if board[i][j]==value:
                            return False
        return True

    def showBoard(self):
        global board
        c1=0
        c2=0
        print("-------------------------")
        
        for i in board:
            for j in i:
                if c2%3==0:
                    print("|",end=" ")
                print(j,end=" ")            
                c2=c2+1
            print("|")
            c1=c1+1
            if c1%3==0:
                print("-------------------------")       

    def start(self):  
        self.getBoard()                      
        #self.showBoard()
        #self.solve()
        #self.showBoard()

board=[
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]
        ]


s = sudokuSolver()
s.start()

root = Tk()

root.resizable(0,0)

if board[0][0]==0:
    label00 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label00 = Label(root, font=('Verdana',8), text=""+str(board[0][0])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[0][1]==0:
    label01 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:   
    label01 = Label(root, font=('Verdana',8), text=""+str(board[0][1])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[0][2]==0:
    label02 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:    
    label02 = Label(root, font=('Verdana',8), text=""+str(board[0][2])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[0][3]==0:
    label03 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:    
    label03 = Label(root, text=str(board[0][3]))
if board[0][4]==0:
    label04 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:    
    label04 = Label(root, text=str(board[0][4]))
if board[0][5]==0:
    label05 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:    
    label05 = Label(root, text=str(board[0][5]))
if board[0][6]==0:
    label06 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:    
    label06 = Label(root, font=('Verdana',8), text=""+str(board[0][6])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[0][7]==0:
    label07 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:    
    label07 = Label(root, font=('Verdana',8), text=""+str(board[0][7])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[0][8]==0:
    label08 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:    
    label08 = Label(root, font=('Verdana',8), text=""+str(board[0][8])+" ",bg='Grey', borderwidth=1, relief='groove')

if board[1][0]==0:
    label10 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label10 = Label(root, font=('Verdana',8), text=""+str(board[1][0])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[1][1]==0:
    label11 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:    
    label11 = Label(root, font=('Verdana',8), text=""+str(board[1][1])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[1][2]==0:
    label12 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:   
    label12 = Label(root, font=('Verdana',8), text=""+str(board[1][2])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[1][3]==0:
    label13 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:    
    label13 = Label(root, text=str(board[1][3]))
if board[1][4]==0:
    label14 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label14 = Label(root, text=str(board[1][4]))
if board[1][5]==0:
    label15 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label15 = Label(root, text=str(board[1][5]))
if board[1][6]==0:
    label16 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label16 = Label(root, font=('Verdana',8), text=""+str(board[1][6])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[1][7]==0:
    label17 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label17 = Label(root, font=('Verdana',8), text=""+str(board[1][7])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[1][8]==0:
    label18 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label18 = Label(root, font=('Verdana',8), text=""+str(board[1][8])+" ",bg='Grey', borderwidth=1, relief='groove')

if board[2][0]==0:
    label20 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label20 = Label(root, font=('Verdana',8), text=""+str(board[2][0])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[2][1]==0:
    label21 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label21 = Label(root, font=('Verdana',8), text=""+str(board[2][1])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[2][2]==0:
    label22 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label22 = Label(root, font=('Verdana',8), text=""+str(board[2][2])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[2][3]==0:
    label23 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label23 = Label(root, text=str(board[2][3]))
if board[2][4]==0:
    label24 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label24 = Label(root, text=str(board[2][4]))
if board[2][5]==0:
    label25 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label25 = Label(root, text=str(board[2][5]))
if board[2][6]==0:
    label26 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label26 = Label(root, font=('Verdana',8), text=""+str(board[2][6])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[2][7]==0:
    label27 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label27 = Label(root, font=('Verdana',8), text=""+str(board[2][7])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[2][8]==0:
    label28 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label28 = Label(root, font=('Verdana',8), text=""+str(board[2][8])+" ",bg='Grey', borderwidth=1, relief='groove')

if board[3][0]==0:
    label30 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label30 = Label(root, text=str(board[3][0]))
if board[3][1]==0:
    label31 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label31 = Label(root, text=str(board[3][1]))
if board[3][2]==0:
    label32 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label32 = Label(root, text=str(board[3][2]))
if board[3][3]==0:
    label33 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label33 = Label(root, font=('Verdana',8), text=""+str(board[3][3])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[3][4]==0:
    label34 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label34 = Label(root, font=('Verdana',8), text=""+str(board[3][4])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[3][5]==0:
    label35 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label35 = Label(root, font=('Verdana',8), text=""+str(board[3][5])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[3][6]==0:
    label36 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label36 = Label(root, text=str(board[3][6]))
if board[3][7]==0:
    label37 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label37 = Label(root, text=str(board[3][7]))
if board[3][8]==0:
    label38 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label38 = Label(root, text=str(board[3][8]))

if board[4][0]==0:
    label40 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label40 = Label(root, text=str(board[4][0]))
if board[4][1]==0:
    label41 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label41 = Label(root, text=str(board[4][1]))
if board[4][2]==0:
    label42 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label42 = Label(root, text=str(board[4][2]))
if board[4][3]==0:
    label43 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label43 = Label(root, font=('Verdana',8), text=""+str(board[4][3])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[4][4]==0:
    label44 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label44 = Label(root, font=('Verdana',8), text=""+str(board[4][4])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[4][5]==0:
    label45 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label45 = Label(root, font=('Verdana',8), text=""+str(board[4][5])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[4][6]==0:
    label46 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label46 = Label(root, text=str(board[4][6]))
if board[4][7]==0:
    label47 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label47 = Label(root, text=str(board[4][7]))
if board[4][8]==0:
    label48 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label48 = Label(root, text=str(board[4][8]))

if board[5][0]==0:
    label50 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label50 = Label(root, text=str(board[5][0]))
if board[5][1]==0:
    label51 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label51 = Label(root, text=str(board[5][1]))
if board[5][2]==0:
    label52 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label52 = Label(root, text=str(board[5][2]))
if board[5][3]==0:
    label53 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label53 = Label(root, font=('Verdana',8), text=""+str(board[5][3])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[5][4]==0:
    label54 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label54 = Label(root, font=('Verdana',8), text=""+str(board[5][4])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[5][5]==0:
    label55 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label55 = Label(root, font=('Verdana',8), text=""+str(board[5][5])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[5][6]==0:
    label56 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label56 = Label(root, text=str(board[5][6]))
if board[5][7]==0:
    label57 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label57 = Label(root, text=str(board[5][7]))
if board[5][8]==0:
    label58 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label58 = Label(root, text=str(board[5][8]))

if board[6][0]==0:
    label60 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label60 = Label(root, font=('Verdana',8), text=""+str(board[6][0])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[6][1]==0:
    label61 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label61 = Label(root, font=('Verdana',8), text=""+str(board[6][1])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[6][2]==0:
    label62 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label62 = Label(root, font=('Verdana',8), text=""+str(board[6][2])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[6][3]==0:
    label63 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label63 = Label(root, text=str(board[6][3]))
if board[6][4]==0:
    label64 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label64 = Label(root, text=str(board[6][4]))
if board[6][5]==0:
    label65 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label65 = Label(root, text=str(board[6][5]))
if board[6][6]==0:
    label66 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label66 = Label(root, font=('Verdana',8), text=""+str(board[6][6])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[6][7]==0:
    label67 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label67 = Label(root, font=('Verdana',8), text=""+str(board[6][7])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[6][8]==0:
    label68 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label68 = Label(root, font=('Verdana',8), text=""+str(board[6][8])+" ",bg='Grey', borderwidth=1, relief='groove')

if board[7][0]==0:
    label70 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label70 = Label(root, font=('Verdana',8), text=""+str(board[7][0])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[7][1]==0:
    label71 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label71 = Label(root, font=('Verdana',8), text=""+str(board[7][1])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[7][2]==0:
    label72 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label72 = Label(root, font=('Verdana',8), text=""+str(board[7][2])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[7][3]==0:
    label73 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label73 = Label(root, text=str(board[7][3]))
if board[7][4]==0:
    label74 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label74 = Label(root, text=str(board[7][4]))
if board[7][5]==0:
    label75 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label75 = Label(root, text=str(board[7][5]))
if board[7][6]==0:
    label76 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label76 = Label(root, font=('Verdana',8), text=""+str(board[7][6])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[7][7]==0:
    label77 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label77 = Label(root, font=('Verdana',8), text=""+str(board[7][7])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[7][8]==0:
    label78 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label78 = Label(root, font=('Verdana',8), text=""+str(board[7][8])+" ",bg='Grey', borderwidth=1, relief='groove')

if board[8][0]==0:
    label80 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label80 = Label(root, bd=2, font=('Verdana',8), text=""+str(board[8][0])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[8][1]==0:
    label81 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label81 = Label(root, bd=2, font=('Verdana',8), text=""+str(board[8][1])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[8][2]==0:
    label82 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label82 = Label(root, bd=2, font=('Verdana',8), text=""+str(board[8][2])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[8][3]==0:
    label83 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label83 = Label(root, bd=2, text=str(board[8][3]))
if board[8][4]==0:
    label84 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label84 = Label(root, bd=2, text=str(board[8][4]))
if board[8][5]==0:
    label85 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label85 = Label(root, bd=2, text=str(board[8][5]))
if board[8][6]==0:
    label86 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label86 = Label(root, bd=2, font=('Verdana',8), text=""+str(board[8][6])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[8][7]==0:
    label87 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label87 = Label(root, bd=2, font=('Verdana',8), text=""+str(board[8][7])+" ",bg='Grey', borderwidth=1, relief='groove')
if board[8][8]==0:
    label88 = Entry(root, bd=1, width=3, font=('Verdana',8), justify='center')
else:
    label88 = Label(root, bd=2, font=('Verdana',8), text=""+str(board[8][8])+" ",bg='Grey', borderwidth=1, relief='groove') 

#font=('Verdana',10))

#label90 = Entry(root, bd=1, width=3)
#label91 = Entry(root, bd=1, width=3)
#label92 = Entry(root, bd=1, width=3)
#label93 = Entry(root, bd=1, width=3)
#label94 = Entry(root, bd=1, width=3)
#label95 = Entry(root, bd=1, width=3)
#label96 = Entry(root, bd=1, width=3)
#label97 = Entry(root, bd=1, width=3)
#label98 = Entry(root, bd=1, width=3)


labels = [[label00,label01,label02,label03,label04,label05,label06,label07,label08],
          [label10,label11,label12,label13,label14,label15,label16,label17,label18],
          [label20,label21,label22,label23,label24,label25,label26,label27,label28],
          [label30,label31,label32,label33,label34,label35,label36,label37,label38],
          [label40,label41,label42,label43,label44,label45,label46,label47,label48],
          [label50,label51,label52,label53,label54,label55,label56,label57,label58],
          [label60,label61,label62,label63,label64,label65,label66,label67,label68],
          [label70,label71,label72,label73,label74,label75,label76,label77,label78],
          [label80,label81,label82,label83,label84,label85,label86,label87,label88],
          #[label90,label91,label92,label93,label94,label95,label96,label97,label98]
         ]

w=0
for i in range(0,len(labels)):
    for j in range(0,len(labels[i])):
        labels[i][j].grid(row=i, column=j, ipadx=6, ipady=5,padx=0,pady=0)


root.mainloop()

#stop = timeit.default_timer()
#print (stop-start)