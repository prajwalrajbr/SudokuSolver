import requests
import json
import sys
from copy import deepcopy
from random import choice
from tkinter import Button,Entry,Tk,IntVar,END,Label,DISABLED,NORMAL,messagebox,Radiobutton,Toplevel
#import timeit
#start = timeit.default_timer()

# api_URL = http://www.cs.utep.edu/cheon/ws/sudoku/new/[?size][&level]

root = Tk()
root.resizable(0,0)

root.protocol('WM_DELETE_WINDOW',lambda : sys.exit())

levelTk = IntVar()
levelTk.set(2)

Radiobutton(root, text="Easy", variable=levelTk, value=1, bg='#90EE90', font=('Verdana',10), padx=50, pady=3).grid(row=2, column=0, columnspan=1)
Radiobutton(root, text="Medium", variable=levelTk, value=2,bg='#FFFF9E', font=('Verdana',10), padx=50, pady=3).grid(row=2, column=1, columnspan=1)
Radiobutton(root, text="Hard", variable=levelTk, value=3, bg='#FF6961', font=('Verdana',10), padx=50, pady=3).grid(row=2, column=2, columnspan=1)



introText = "Sudoku originally called Number Place\n is a logic-based combinatorial number-placement puzzle.\nThe objective is to fill a 9×9 grid with digits so that\n each column, each row, and each of the nine 3×3 subgrids\n that compose the grid (also called \"boxes\", \"blocks\",\n or \"regions\") contain all of the digits from 1 to 9.\nThe puzzle setter provides a partially completed grid,\n which for a well-posed puzzle has a single solution."

introLabel = Label(root, text=introText, font=('Verdana',12))
introLabel.grid(row=0, column=0, padx=7, pady=3, columnspan=3)

root.bind('<Return>', lambda *args : root.destroy())

stButton = Button(root, text="Start",width=45, font=('Verdana',13), bg='#000000', fg='#FFFFFF', command=lambda : root.destroy())
stButton.grid(row=3, column=0, ipady=5, pady=5, columnspan=3)


root.mainloop()

class sudokuSolver:

    def getBoard(self, board):
        global level

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
                for _ in range(0,choice([1,2,3])):
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
   
    def findEmpty(self, board):
        #Check for the value 0
        for i in range(0,9):
            for j in range(0,9):
                if board[i][j]==0:
                    return i,j

    def solve(self, board):
        x=self.findEmpty(board)
        if x:
            row,col=x
        else:
            return True

        #Insert 1 to 9 to the position of 0
        for i in range(1,10):
            if self.checkIfValid(i,row,col,board):
                board[row][col]=i
                if self.solve(board):
                    return True
                board[row][col]=0
        return False

    def solveGUI(self, board):
        global algorithm
        x=self.findEmpty(board)
        if x:
            row,col=x
        else:
            return True

        #Insert 1 to 9 to the position of 0
        for i in range(1,10):
            if self.checkIfValid(i,row,col,board):
                board[row][col]=i
                li=[True,row,col,i]
                algorithm.append(li)
                if self.solveGUI(board):
                    return True
                board[row][col]=0
                li=[False,row,col,0]
                algorithm.append(li)
        return False

    def checkIfValid(self,value,row,col,board):
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

    def showBoard(self, board):
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

    def noOfEmpty(self,board):
        count=0
        for i in range(0,9):
            for j in range(0,9):
                if board[i][j] == 0:
                    count += 1
        return count

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

level = levelTk.get()
submitButtonCount = -1
solveButtonCount = -1
count = 0
s = sudokuSolver()
s.getBoard(board)
noOfEmpty = s.noOfEmpty(board)
solved = False
algorithm = []
sec=0
min=0
hour=0
attempt=0

root = Tk()

root.resizable(0,0)

label00Value = IntVar() 
label01Value = IntVar()
label02Value = IntVar() 
label03Value = IntVar()
label04Value = IntVar() 
label05Value = IntVar()
label06Value = IntVar() 
label07Value = IntVar()
label08Value = IntVar()

label10Value = IntVar() 
label11Value = IntVar()
label12Value = IntVar() 
label13Value = IntVar()
label14Value = IntVar() 
label15Value = IntVar()
label16Value = IntVar() 
label17Value = IntVar()
label18Value = IntVar()

label20Value = IntVar() 
label21Value = IntVar()
label22Value = IntVar() 
label23Value = IntVar()
label24Value = IntVar() 
label25Value = IntVar()
label26Value = IntVar() 
label27Value = IntVar()
label28Value = IntVar()

label30Value = IntVar() 
label31Value = IntVar()
label32Value = IntVar() 
label33Value = IntVar()
label34Value = IntVar() 
label35Value = IntVar()
label36Value = IntVar() 
label37Value = IntVar()
label38Value = IntVar()

label40Value = IntVar() 
label41Value = IntVar()
label42Value = IntVar() 
label43Value = IntVar()
label44Value = IntVar() 
label45Value = IntVar()
label46Value = IntVar() 
label47Value = IntVar()
label48Value = IntVar()

label50Value = IntVar() 
label51Value = IntVar()
label52Value = IntVar() 
label53Value = IntVar()
label54Value = IntVar() 
label55Value = IntVar()
label56Value = IntVar() 
label57Value = IntVar()
label58Value = IntVar()

label60Value = IntVar() 
label61Value = IntVar()
label62Value = IntVar() 
label63Value = IntVar()
label64Value = IntVar() 
label65Value = IntVar()
label66Value = IntVar() 
label67Value = IntVar()
label68Value = IntVar()

label70Value = IntVar() 
label71Value = IntVar()
label72Value = IntVar() 
label73Value = IntVar()
label74Value = IntVar() 
label75Value = IntVar()
label76Value = IntVar() 
label77Value = IntVar()
label78Value = IntVar()

label80Value = IntVar() 
label81Value = IntVar()
label82Value = IntVar() 
label83Value = IntVar()
label84Value = IntVar() 
label85Value = IntVar()
label86Value = IntVar() 
label87Value = IntVar()
label88Value = IntVar()


if board[0][0]==0:  
    def keyPress00(event):
        label00.delete(0, END)
    label00 = Entry(root, bd=1, bg='#C0C0C0', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label00Value)    
    label00.bind('<KeyPress>', keyPress00)
else:
    label00 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[0][0])+" ", borderwidth=1, relief='groove')
if board[0][1]==0:
    def keyPress01(event):
        label01.delete(0, END)
    label01 = Entry(root, bd=1, bg='#C0C0C0', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label01Value)
    label01.bind('<KeyPress>', keyPress01)
else:   
    label01 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[0][1])+" ", borderwidth=1, relief='groove')
if board[0][2]==0:
    def keyPress02(event):
        label02.delete(0, END)
    label02 = Entry(root, bd=1, bg='#C0C0C0', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label02Value)
    label02.bind('<KeyPress>', keyPress02)
else:    
    label02 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[0][2])+" ", borderwidth=1, relief='groove')
if board[0][3]==0:
    def keyPress03(event):
        label03.delete(0, END)
    label03 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label03Value)
    label03.bind('<KeyPress>', keyPress03)
else:    
    label03 = Label(root, text=str(board[0][3]))
if board[0][4]==0:
    def keyPress04(event):
        label04.delete(0, END)
    label04 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label04Value)
    label04.bind('<KeyPress>', keyPress04)
else:    
    label04 = Label(root, text=str(board[0][4]))
if board[0][5]==0:
    def keyPress05(event):
        label05.delete(0, END)
    label05 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label05Value)
    label05.bind('<KeyPress>', keyPress05)
else:    
    label05 = Label(root, text=str(board[0][5]))
if board[0][6]==0:
    def keyPress06(event):
        label06.delete(0, END)
    label06 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label06Value)
    label06.bind('<KeyPress>', keyPress06)
else:    
    label06 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[0][6])+" ", borderwidth=1, relief='groove')
if board[0][7]==0:
    def keyPress07(event):
        label07.delete(0, END)
    label07 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label07Value)
    label07.bind('<KeyPress>', keyPress07)
else:    
    label07 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[0][7])+" ", borderwidth=1, relief='groove')
if board[0][8]==0:
    def keyPress08(event):
        label08.delete(0, END)
    label08 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label08Value)
    label08.bind('<KeyPress>', keyPress08)
else:    
    label08 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[0][8])+" ", borderwidth=1, relief='groove')

if board[1][0]==0:
    def keyPress10(event):
        label10.delete(0, END)
    label10 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label10Value)
    label10.bind('<KeyPress>', keyPress10)
else:
    label10 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[1][0])+" ", borderwidth=1, relief='groove')
if board[1][1]==0:
    def keyPress11(event):
        label11.delete(0, END)
    label11 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label11Value)
    label11.bind('<KeyPress>', keyPress11)
else:    
    label11 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[1][1])+" ", borderwidth=1, relief='groove')
if board[1][2]==0:
    def keyPress12(event):
        label12.delete(0, END)
    label12 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label12Value)
    label12.bind('<KeyPress>', keyPress12)
else:   
    label12 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[1][2])+" ", borderwidth=1, relief='groove')
if board[1][3]==0:
    def keyPress13(event):
        label13.delete(0, END)
    label13 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label13Value)
    label13.bind('<KeyPress>', keyPress13)
else:    
    label13 = Label(root, text=str(board[1][3]))
if board[1][4]==0:
    def keyPress14(event):
        label14.delete(0, END)
    label14 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label14Value)
    label14.bind('<KeyPress>', keyPress14)
else:
    label14 = Label(root, text=str(board[1][4]))
if board[1][5]==0:
    def keyPress15(event):
        label15.delete(0, END)
    label15 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label15Value)
    label15.bind('<KeyPress>', keyPress15)
else:
    label15 = Label(root, text=str(board[1][5]))
if board[1][6]==0:
    def keyPress16(event):
        label16.delete(0, END)
    label16 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label16Value)
    label16.bind('<KeyPress>', keyPress16)
else:
    label16 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[1][6])+" ", borderwidth=1, relief='groove')
if board[1][7]==0:
    def keyPress17(event):
        label17.delete(0, END)
    label17 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label17Value)
    label17.bind('<KeyPress>', keyPress17)
else:
    label17 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[1][7])+" ", borderwidth=1, relief='groove')
if board[1][8]==0:
    def keyPress18(event):
        label18.delete(0, END)
    label18 = Entry(root, bg='#C0C0C0', fg='#000000', bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label18Value)
    label18.bind('<KeyPress>', keyPress18)
else:
    label18 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[1][8])+" ", borderwidth=1, relief='groove')

if board[2][0]==0:
    def keyPress20(event):
        label20.delete(0, END)
    label20 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label20Value)
    label20.bind('<KeyPress>', keyPress20)
else:
    label20 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[2][0])+" ", borderwidth=1, relief='groove')
if board[2][1]==0:
    def keyPress21(event):
        label21.delete(0, END)
    label21 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label21Value)
    label21.bind('<KeyPress>', keyPress21)
else:
    label21 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[2][1])+" ", borderwidth=1, relief='groove')
if board[2][2]==0:
    def keyPress22(event):
        label22.delete(0, END)
    label22 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label22Value)
    label22.bind('<KeyPress>', keyPress22)
else:
    label22 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[2][2])+" ", borderwidth=1, relief='groove')
if board[2][3]==0:
    def keyPress23(event):
        label23.delete(0, END)
    label23 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label23Value)
    label23.bind('<KeyPress>', keyPress23)
else:
    label23 = Label(root, text=str(board[2][3]))
if board[2][4]==0:
    def keyPress24(event):
        label24.delete(0, END)
    label24 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label24Value)
    label24.bind('<KeyPress>', keyPress24)
else:
    label24 = Label(root, text=str(board[2][4]))
if board[2][5]==0:
    def keyPress25(event):
        label25.delete(0, END)
    label25 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label25Value)
    label25.bind('<KeyPress>', keyPress25)
else:
    label25 = Label(root, text=str(board[2][5]))
if board[2][6]==0:
    def keyPress26(event):
        label26.delete(0, END)
    label26 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label26Value)
    label26.bind('<KeyPress>', keyPress26)
else:
    label26 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[2][6])+" ", borderwidth=1, relief='groove')
if board[2][7]==0:
    def keyPress27(event):
        label27.delete(0, END)
    label27 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label27Value)
    label27.bind('<KeyPress>', keyPress27)
else:
    label27 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[2][7])+" ", borderwidth=1, relief='groove')
if board[2][8]==0:
    def keyPress28(event):
        label28.delete(0, END)
    label28 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label28Value)
    label28.bind('<KeyPress>', keyPress28)
else:
    label28 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[2][8])+" ", borderwidth=1, relief='groove')

if board[3][0]==0:
    def keyPress30(event):
        label30.delete(0, END)
    label30 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label30Value)
    label30.bind('<KeyPress>', keyPress30)
else:
    label30 = Label(root, text=str(board[3][0]))
if board[3][1]==0:
    def keyPress31(event):
        label31.delete(0, END)
    label31 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label31Value)
    label31.bind('<KeyPress>', keyPress31)
else:
    label31 = Label(root, text=str(board[3][1]))
if board[3][2]==0:
    def keyPress32(event):
        label32.delete(0, END)
    label32 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label32Value)
    label32.bind('<KeyPress>', keyPress32)
else:
    label32 = Label(root, text=str(board[3][2]))
if board[3][3]==0:
    def keyPress33(event):
        label33.delete(0, END)
    label33 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label33Value)
    label33.bind('<KeyPress>', keyPress33)
else:
    label33 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[3][3])+" ", borderwidth=1, relief='groove')
if board[3][4]==0:
    def keyPress34(event):
        label34.delete(0, END)
    label34 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label34Value)
    label34.bind('<KeyPress>', keyPress34)
else:
    label34 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[3][4])+" ", borderwidth=1, relief='groove')
if board[3][5]==0:
    def keyPress35(event):
        label35.delete(0, END)
    label35 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label35Value)
    label35.bind('<KeyPress>', keyPress35)
else:
    label35 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[3][5])+" ", borderwidth=1, relief='groove')
if board[3][6]==0:
    def keyPress36(event):
        label36.delete(0, END)
    label36 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label36Value)
    label36.bind('<KeyPress>', keyPress36)
else:
    label36 = Label(root, text=str(board[3][6]))
if board[3][7]==0:
    def keyPress37(event):
        label37.delete(0, END)
    label37 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label37Value)
    label37.bind('<KeyPress>', keyPress37)
else:
    label37 = Label(root, text=str(board[3][7]))
if board[3][8]==0:
    def keyPress38(event):
        label38.delete(0, END)
    label38 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label38Value)
    label38.bind('<KeyPress>', keyPress38)
else:
    label38 = Label(root, text=str(board[3][8]))

if board[4][0]==0:
    def keyPress40(event):
        label40.delete(0, END)
    label40 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label40Value)
    label40.bind('<KeyPress>', keyPress40)
else:
    label40 = Label(root, text=str(board[4][0]))
if board[4][1]==0:
    def keyPress41(event):
        label41.delete(0, END)
    label41 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label41Value)
    label41.bind('<KeyPress>', keyPress41)
else:
    label41 = Label(root, text=str(board[4][1]))
if board[4][2]==0:
    def keyPress42(event):
        label42.delete(0, END)
    label42 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label42Value)
    label42.bind('<KeyPress>', keyPress42)
else:
    label42 = Label(root, text=str(board[4][2]))
if board[4][3]==0:
    def keyPress43(event):
        label43.delete(0, END)
    label43 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label43Value)
    label43.bind('<KeyPress>', keyPress43)
else:
    label43 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[4][3])+" ", borderwidth=1, relief='groove')
if board[4][4]==0:
    def keyPress44(event):
        label44.delete(0, END)
    label44 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label44Value)
    label44.bind('<KeyPress>', keyPress44)
else:
    label44 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[4][4])+" ", borderwidth=1, relief='groove')
if board[4][5]==0:
    def keyPress45(event):
        label45.delete(0, END)
    label45 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label45Value)
    label45.bind('<KeyPress>', keyPress45)
else:
    label45 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[4][5])+" ", borderwidth=1, relief='groove')
if board[4][6]==0:
    def keyPress46(event):
        label46.delete(0, END)
    label46 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label46Value)
    label46.bind('<KeyPress>', keyPress46)
else:
    label46 = Label(root, text=str(board[4][6]))
if board[4][7]==0:
    def keyPress47(event):
        label47.delete(0, END)
    label47 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label47Value)
    label47.bind('<KeyPress>', keyPress47)
else:
    label47 = Label(root, text=str(board[4][7]))
if board[4][8]==0:
    def keyPress48(event):
        label48.delete(0, END)
    label48 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label48Value)
    label48.bind('<KeyPress>', keyPress48)
else:
    label48 = Label(root, text=str(board[4][8]))

if board[5][0]==0:
    def keyPress50(event):
        label50.delete(0, END)
    label50 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label50Value)
    label50.bind('<KeyPress>', keyPress50)
else:
    label50 = Label(root, text=str(board[5][0]))
if board[5][1]==0:
    def keyPress51(event):
        label51.delete(0, END)
    label51 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label51Value)
    label51.bind('<KeyPress>', keyPress51)
else:
    label51 = Label(root, text=str(board[5][1]))
if board[5][2]==0:
    def keyPress52(event):
        label52.delete(0, END)
    label52 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label52Value)
    label52.bind('<KeyPress>', keyPress52)
else:
    label52 = Label(root, text=str(board[5][2]))
if board[5][3]==0:
    def keyPress53(event):
        label53.delete(0, END)
    label53 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label53Value)
    label53.bind('<KeyPress>', keyPress53)
else:
    label53 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[5][3])+" ", borderwidth=1, relief='groove')
if board[5][4]==0:
    def keyPress54(event):
        label54.delete(0, END)
    label54 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label54Value)
    label54.bind('<KeyPress>', keyPress54)
else:
    label54 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[5][4])+" ", borderwidth=1, relief='groove')
if board[5][5]==0:
    def keyPress55(event):
        label55.delete(0, END)
    label55 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label55Value)
    label55.bind('<KeyPress>', keyPress55)
else:
    label55 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[5][5])+" ", borderwidth=1, relief='groove')
if board[5][6]==0:
    def keyPress56(event):
        label56.delete(0, END)
    label56 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label56Value)
    label56.bind('<KeyPress>', keyPress56)
else:
    label56 = Label(root, text=str(board[5][6]))
if board[5][7]==0:
    def keyPress57(event):
        label57.delete(0, END)
    label57 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label57Value)
    label57.bind('<KeyPress>', keyPress57)
else:
    label57 = Label(root, text=str(board[5][7]))
if board[5][8]==0:
    def keyPress58(event):
        label58.delete(0, END)
    label58 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label58Value)
    label58.bind('<KeyPress>', keyPress58)
else:
    label58 = Label(root, text=str(board[5][8]))

if board[6][0]==0:
    def keyPress60(event):
        label60.delete(0, END)
    label60 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label60Value)
    label60.bind('<KeyPress>', keyPress60)
else:
    label60 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[6][0])+" ", borderwidth=1, relief='groove')
if board[6][1]==0:
    def keyPress61(event):
        label61.delete(0, END)
    label61 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label61Value)
    label61.bind('<KeyPress>', keyPress61)
else:
    label61 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[6][1])+" ", borderwidth=1, relief='groove')
if board[6][2]==0:
    def keyPress62(event):
        label62.delete(0, END)
    label62 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label62Value)
    label62.bind('<KeyPress>', keyPress62)
else:
    label62 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[6][2])+" ", borderwidth=1, relief='groove')
if board[6][3]==0:
    def keyPress63(event):
        label63.delete(0, END)
    label63 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label63Value)
    label63.bind('<KeyPress>', keyPress63)
else:
    label63 = Label(root, text=str(board[6][3]))
if board[6][4]==0:
    def keyPress64(event):
        label64.delete(0, END)
    label64 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label64Value)
    label64.bind('<KeyPress>', keyPress64)
else:
    label64 = Label(root, text=str(board[6][4]))
if board[6][5]==0:
    def keyPress65(event):
        label65.delete(0, END)
    label65 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label65Value)
    label65.bind('<KeyPress>', keyPress65)
else:
    label65 = Label(root, text=str(board[6][5]))
if board[6][6]==0:
    def keyPress66(event):
        label66.delete(0, END)
    label66 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label66Value)
    label66.bind('<KeyPress>', keyPress66)
else:
    label66 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[6][6])+" ", borderwidth=1, relief='groove')
if board[6][7]==0:
    def keyPress67(event):
        label67.delete(0, END)
    label67 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label67Value)
    label67.bind('<KeyPress>', keyPress67)
else:
    label67 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[6][7])+" ", borderwidth=1, relief='groove')
if board[6][8]==0:
    def keyPress68(event):
        label68.delete(0, END)
    label68 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label68Value)
    label68.bind('<KeyPress>', keyPress68)
else:
    label68 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[6][8])+" ", borderwidth=1, relief='groove')

if board[7][0]==0:
    def keyPress70(event):
        label70.delete(0, END)
    label70 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label70Value)
    label70.bind('<KeyPress>', keyPress70)
else:
    label70 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[7][0])+" ", borderwidth=1, relief='groove')
if board[7][1]==0:
    def keyPress71(event):
        label71.delete(0, END)
    label71 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label71Value)
    label71.bind('<KeyPress>', keyPress71)
else:
    label71 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[7][1])+" ", borderwidth=1, relief='groove')
if board[7][2]==0:
    def keyPress72(event):
        label72.delete(0, END)
    label72 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label72Value)
    label72.bind('<KeyPress>', keyPress72)
else:
    label72 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[7][2])+" ", borderwidth=1, relief='groove')
if board[7][3]==0:
    def keyPress73(event):
        label73.delete(0, END)
    label73 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label73Value)
    label73.bind('<KeyPress>', keyPress73)
else:
    label73 = Label(root, text=str(board[7][3]))
if board[7][4]==0:
    def keyPress74(event):
        label74.delete(0, END)
    label74 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label74Value)
    label74.bind('<KeyPress>', keyPress74)
else:
    label74 = Label(root, text=str(board[7][4]))
if board[7][5]==0:
    def keyPress75(event):
        label75.delete(0, END)
    label75 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label75Value)
    label75.bind('<KeyPress>', keyPress75)
else:
    label75 = Label(root, text=str(board[7][5]))
if board[7][6]==0:
    def keyPress76(event):
        label76.delete(0, END)
    label76 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label76Value)
    label76.bind('<KeyPress>', keyPress76)
else:
    label76 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[7][6])+" ", borderwidth=1, relief='groove')
if board[7][7]==0:
    def keyPress77(event):
        label77.delete(0, END)
    label77 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label77Value)
    label77.bind('<KeyPress>', keyPress77)
else:
    label77 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[7][7])+" ", borderwidth=1, relief='groove')
if board[7][8]==0:
    def keyPress78(event):
        label78.delete(0, END)
    label78 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label78Value)
    label78.bind('<KeyPress>', keyPress78)
else:
    label78 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[7][8])+" ", borderwidth=1, relief='groove')

if board[8][0]==0:
    def keyPress80(event):
        label80.delete(0, END)
    label80 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label80Value)
    label80.bind('<KeyPress>', keyPress80)
else:
    label80 = Label(root, bd=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[8][0])+" ", borderwidth=1, relief='groove')
if board[8][1]==0:
    def keyPress81(event):
        label81.delete(0, END)
    label81 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label81Value)
    label81.bind('<KeyPress>', keyPress81)
else:
    label81 = Label(root, bg='#C0C0C0', fg='#000000', bd=2, font=('Verdana',8), text=""+str(board[8][1])+" ", borderwidth=1, relief='groove')
if board[8][2]==0:
    def keyPress82(event):
        label82.delete(0, END)
    label82 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label82Value)
    label82.bind('<KeyPress>', keyPress82)
else:
    label82 = Label(root, bg='#C0C0C0', fg='#000000', bd=2, font=('Verdana',8), text=""+str(board[8][2])+" ", borderwidth=1, relief='groove')
if board[8][3]==0:
    def keyPress83(event):
        label83.delete(0, END)
    label83 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label83Value)
    label83.bind('<KeyPress>', keyPress83)
else:
    label83 = Label(root, bd=2, text=str(board[8][3]))
if board[8][4]==0:
    def keyPress84(event):
        label84.delete(0, END)
    label84 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label84Value)
    label84.bind('<KeyPress>', keyPress84)
else:
    label84 = Label(root, bd=2, text=str(board[8][4]))
if board[8][5]==0:
    def keyPress85(event):
        label85.delete(0, END)
    label85 = Entry(root, bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label85Value)
    label85.bind('<KeyPress>', keyPress85)
else:
    label85 = Label(root, bd=2, text=str(board[8][5]))
if board[8][6]==0:
    def keyPress86(event):
        label86.delete(0, END)
    label86 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label86Value)
    label86.bind('<KeyPress>', keyPress86)
else:
    label86 = Label(root, bg='#C0C0C0', fg='#000000', bd=2, font=('Verdana',8), text=""+str(board[8][6])+" ", borderwidth=1, relief='groove')
if board[8][7]==0:
    def keyPress87(event):
        label87.delete(0, END)
    label87 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label87Value)
    label87.bind('<KeyPress>', keyPress87)
else:
    label87 = Label(root, bg='#C0C0C0', fg='#000000', bd=2, font=('Verdana',8), text=""+str(board[8][7])+" ", borderwidth=1, relief='groove')
if board[8][8]==0:
    def keyPress88(event):
        label88.delete(0, END)
    label88 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label88Value)
    label88.bind('<KeyPress>', keyPress88)
else:
    label88 = Label(root, bg='#C0C0C0', fg='#000000', bd=2, font=('Verdana',8), text=""+str(board[8][8])+" ", borderwidth=1, relief='groove') 

def newWin():
    global attempt,sec,hour,min
    newWin = Toplevel(root)
    
    newWin.bind('<Return>', lambda *args : sys.exit())
    newWin.resizable(0,0)
    at = "Attempt : "+str(int(attempt))
    attemptLabel = Label(newWin, text=at, padx=10, pady=10)
    attemptLabel.grid(row=0, column=0)
    t = "Time taken : "
    if hour<10:
        t += "0"+str(hour) 
    else:
        t += str(hour)
    if min<10:
        t += ":0"+str(min)
    else:
        t += ":"+str(min)
    if sec<10:
        t += ":0"+str(sec)
    else:
        t += ":"+str(sec)
    timeLabel = Label(newWin, text=t, padx=10, pady=10)
    timeLabel.grid(row=1, column=0)
    okButtton = Button(newWin, text='Ok', command=lambda : sys.exit())
    okButtton.grid(row=2, column=0, columnspan=1)
    
def askForConfirm():
    msg = messagebox.askokcancel("Confirmation!!!", "Are you sure you want to EXIT ?", icon="warning")
    if msg:
        root.destroy()

root.protocol('WM_DELETE_WINDOW',askForConfirm)

labels = [[label00,label01,label02,label03,label04,label05,label06,label07,label08],
          [label10,label11,label12,label13,label14,label15,label16,label17,label18],
          [label20,label21,label22,label23,label24,label25,label26,label27,label28],
          [label30,label31,label32,label33,label34,label35,label36,label37,label38],
          [label40,label41,label42,label43,label44,label45,label46,label47,label48],
          [label50,label51,label52,label53,label54,label55,label56,label57,label58],
          [label60,label61,label62,label63,label64,label65,label66,label67,label68],
          [label70,label71,label72,label73,label74,label75,label76,label77,label78],
          [label80,label81,label82,label83,label84,label85,label86,label87,label88],
         ]

entryValues = [[label00Value,label01Value,label02Value,label03Value,label04Value,label05Value,label06Value,label07Value,label08Value],
               [label10Value,label11Value,label12Value,label13Value,label14Value,label15Value,label16Value,label17Value,label18Value],
               [label20Value,label21Value,label22Value,label23Value,label24Value,label25Value,label26Value,label27Value,label28Value],
               [label30Value,label31Value,label32Value,label33Value,label34Value,label35Value,label36Value,label37Value,label38Value],
               [label40Value,label41Value,label42Value,label43Value,label44Value,label45Value,label46Value,label47Value,label48Value],
               [label50Value,label51Value,label52Value,label53Value,label54Value,label55Value,label56Value,label57Value,label58Value],
               [label60Value,label61Value,label62Value,label63Value,label64Value,label65Value,label66Value,label67Value,label68Value],
               [label70Value,label71Value,label72Value,label73Value,label74Value,label75Value,label76Value,label77Value,label78Value],
               [label80Value,label81Value,label82Value,label83Value,label84Value,label85Value,label86Value,label87Value,label88Value]
              ]

for i in range(0,len(labels)):
    for j in range(0,len(labels[i])):
        labels[i][j].grid(row=i, column=j, ipadx=6, ipady=5, padx=0, pady=0)

def call_submit(*args):
    global submitButtonCount,attempt
    attempt += 1
    submitButtonCount += 1
    submit()

def changeColor(): 
    if not solved:
        submitButton.configure(state=NORMAL)

    if solveButtonCount==1:
        solveButton.configure(state=DISABLED)
    for i in range(0,9):
        for j in range(0,9):
            if i in [0,1,2,6,7,8]:
                if j in [0,1,2,6,7,8]:
                    labels[i][j].configure(bg='#C0C0C0', fg='#000000')
                else:
                    labels[i][j].configure(bg='#FFFFFF', fg='#000000')
            elif i in [3,4,5]:
                if j in [3,4,5]:
                    labels[i][j].configure(bg='#C0C0C0', fg='#000000')
                else:
                    labels[i][j].configure(bg='#FFFFFF', fg='#000000')
            else:
                labels[i][j].configure(bg='#FFFFFF', fg='#000000')

def submit():
    temp=deepcopy(board)
    t = sudokuSolver()
    t.solve(temp)
    global count,submitButtonCount,noOfEmpty,attempt
    if submitButtonCount%2==0:
        changeColor()
        k=0
        for i in range(0,9):
            for j in range(0,9):
                if board[i][j] == 0: 
                    if k <= count:
                        try:
                            if entryValues[i][j].get() == temp[i][j]:
                                labels[i][j].configure(bg='#90EE90')
                            else:
                                labels[i][j].configure(bg='#FFCCCB')
                        except:       
                            labels[i][j].configure(bg='#FFCCCB')
                        k += 1
        count += 1
        if noOfEmpty==count:
            count=0
            root.after(3000,changeColor)
            submitButtonCount=-1
        else:
            root.after(100,submit)
    else:
        if submitButtonCount==9999:
            changeColor()
        else:
            attempt -= .5
            submitButton.configure(state=DISABLED)
            for i in range(0,9):
                for j in range(0,9):
                    if board[i][j] == 0: 
                        try:
                            if entryValues[i][j].get() == temp[i][j]:
                                labels[i][j].configure(bg='#90EE90')
                            else:
                                labels[i][j].configure(bg='#FFCCCB')
                        except:       
                            labels[i][j].configure(bg='#FFCCCB')
            count=0
            root.after(3000,changeColor)
    del temp
    del t

def solve():
    global algorithm
    if len(algorithm)==0:
        
        solveButton.configure(state=DISABLED)
        newWin()

        return
    if algorithm[0][0]==True:
        entryValues[algorithm[0][1]][algorithm[0][2]].set(algorithm[0][3])
        labels[algorithm[0][1]][algorithm[0][2]].configure(bg='#87CEEB', fg='#000000')
    else:
        entryValues[algorithm[0][1]][algorithm[0][2]].set(algorithm[0][3])
        labels[algorithm[0][1]][algorithm[0][2]].configure(bg='#FFCCCB', fg='#000000')
    algorithm.pop(0)
    if(solveButtonCount==0):
        root.after(500,solve)
        root.after((len(algorithm)*500+3000),changeColor)
    else:
        root.after(500,call_solve)
        
def call_solve(*args):
    global solved,solveButtonCount,submitButtonCount
    if not solved:
        submitButton.configure(state=DISABLED)
    solved = True
    submitButtonCount = 9999
    temp=deepcopy(board)
    t = sudokuSolver()
    changeColor()
    solveButtonCount += 1
    if solveButtonCount == 0:
        t.solveGUI(temp)
        root.after(100,solve)
    else:
        t.solve(temp)
        for i in range(0,9):
            for j in range(0,9):
                if board[i][j]==0:
                    entryValues[i][j].set(temp[i][j])
                    labels[i][j].configure(bg='#87CEEB', fg='#000000')        
        root.after(3000,changeColor)  
        algorithm.clear()   
        solveButton.configure(state=DISABLED)  
    del temp
    del t

timeLapse = Label()

def timeTaken():
    if solved:
        return
    global hour,min,sec,timeLapse
    root.after(1000,timeTaken)
    t = ""
    if hour<10:
        t += "0"+str(hour) 
    else:
        t += str(hour)
    if min<10:
        t += ":0"+str(min)
    else:
        t += ":"+str(min)
    if sec<10:
        t += ":0"+str(sec)
    else:
        t += ":"+str(sec)
    if sec%2!=0:
        timeLapse.configure(text=t, fg="#FFFFFF", bg="#000000")
    else:
        timeLapse.configure(text=t, fg="#000000", bg="#FFFFFF")
    sec+=1
    if sec==60:
        min += 1
        sec = 0
    if min==60:
        hour += 1
        min = 0
    return t

submitButton = Button(root, text="Submit", padx=23, pady=10, font=('Verdana',8), bg='#FFCCCB',fg='#000000', command=call_submit)
submitButton.grid(row=10, column=0, columnspan=3)

solveButton = Button(root, text="Solve", padx=23, pady=10, font=('Verdana',8), bg='#87CEEB', fg='#000000', command=call_solve)
solveButton.grid(row=10, column=2, columnspan=5)

timeLapse = Label(root, text=timeTaken(), padx=23, pady=10, font=('Verdana',8), fg="#000000", bg="#FFFFFF")
timeLapse.grid(row=10, column=6, columnspan=3)

root.mainloop()

#stop = timeit.default_timer()
#print (stop-start)