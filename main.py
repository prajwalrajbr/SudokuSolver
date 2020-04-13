try:
    import requests
    import json
    import sys
    from copy import deepcopy
    from random import choice
    from tkinter import Button,Entry,Tk,IntVar,END,Label,DISABLED,NORMAL,messagebox,Radiobutton,Toplevel
except:
    import install_requirements
    import requests
    import json
    import sys
    from copy import deepcopy
    from random import choice
    from tkinter import Button,Entry,Tk,IntVar,END,Label,DISABLED,NORMAL,messagebox,Radiobutton,Toplevel

# api_URL = http://www.cs.utep.edu/cheon/ws/sudoku/new/[?size][&level]

root = Tk()
root.resizable(0,0)
root.title('Sudoku - 9x9')
try:
    root.iconbitmap('sudoku.ico')
except:
    pass
root.protocol('WM_DELETE_WINDOW',lambda : sys.exit())

levelTk = IntVar()
levelTk.set(2)

Radiobutton(root, text="Easy", variable=levelTk, value=1, bg='#90EE90', font=('Verdana',10), padx=50, pady=3).grid(row=2, column=0, columnspan=1)
Radiobutton(root, text="Medium", variable=levelTk, value=2,bg='#FFFF9E', font=('Verdana',10), padx=50, pady=3).grid(row=2, column=1, columnspan=1)
Radiobutton(root, text="Hard", variable=levelTk, value=3, bg='#FF6961', font=('Verdana',10), padx=50, pady=3).grid(row=2, column=2, columnspan=1)

def levVal(z):
    global levelTk
    k=levelTk.get()
    if z:
        if k==1:
            levelTk.set(3)
        elif k==2:
            levelTk.set(1)
        else:
            levelTk.set(2)
    else:
        if k==1:
            levelTk.set(2)
        elif k==2:
            levelTk.set(3)
        else:
            levelTk.set(1)
        
introText = "Sudoku originally called Number Place\n is a logic-based combinatorial number-placement puzzle.\nThe objective is to fill a 9×9 grid with digits so that\n each column, each row, and each of the nine 3×3 subgrids\n that compose the grid (also called \"boxes\", \"blocks\",\n or \"regions\") contain all of the digits from 1 to 9.\nThe puzzle setter provides a partially completed grid,\n which for a well-posed puzzle has a single solution."

introLabel = Label(root, text=introText, font=('Verdana',12))
introLabel.grid(row=0, column=0, padx=7, pady=3, columnspan=3)

root.bind('<Return>', lambda *args : root.destroy())
root.bind('<Left>', lambda *args: levVal(True))
root.bind('<Right>', lambda *args: levVal(False))
root.bind('<Escape>', sys.exit)

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
error=0
newWinCount=False

root = Tk()
root.resizable(0,0)
root.title('Sudoku - 9x9')
try:
    root.iconbitmap('sudoku.ico')
except:
    pass


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
    def keyPress00():
        if len(str(label00.get()))>0:
            try:
                label00Value.set(str(label00Value.get())[-1])
            except:
                label00Value.set(0)
    label00 = Entry(root, bd=1, bg='#C0C0C0', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label00Value)
    label00Value.trace("w",lambda *args: keyPress00())
else:
    label00 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[0][0])+" ", borderwidth=1, relief='groove')
if board[0][1]==0:  
    def keyPress01():
        if len(str(label01.get()))>0:
            try:
                label01Value.set(str(label01Value.get())[-1])
            except:
                label01Value.set(0)
    label01 = Entry(root, bd=1, bg='#C0C0C0', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label01Value)
    label01Value.trace("w",lambda *args: keyPress01())
else:   
    label01 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[0][1])+" ", borderwidth=1, relief='groove')
if board[0][2]==0:  
    def keyPress02():
        if len(str(label02.get()))>0:
            try:
                label02Value.set(str(label02Value.get())[-1])
            except:
                label02Value.set(0)
    label02 = Entry(root, bd=1, bg='#C0C0C0', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label02Value)
    label02Value.trace("w",lambda *args: keyPress02())
else:    
    label02 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[0][2])+" ", borderwidth=1, relief='groove')
if board[0][3]==0:  
    def keyPress03():
        if len(str(label03.get()))>0:
            try:
                label03Value.set(str(label03Value.get())[-1])
            except:
                label03Value.set(0)
    label03 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label03Value)
    label03Value.trace("w",lambda *args: keyPress03())
else:    
    label03 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[0][3]))
if board[0][4]==0:  
    def keyPress04():
        if len(str(label04.get()))>0:
            try:
                label04Value.set(str(label04Value.get())[-1])
            except:
                label04Value.set(0)
    label04 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label04Value)
    label04Value.trace("w",lambda *args: keyPress04())
else:    
    label04 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[0][4]))
if board[0][5]==0:  
    def keyPress05():
        if len(str(label05.get()))>0:
            try:
                label05Value.set(str(label05Value.get())[-1])
            except:
                label05Value.set(0)
    label05 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label05Value)
    label05Value.trace("w",lambda *args: keyPress05())
else:    
    label05 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[0][5]))
if board[0][6]==0:  
    def keyPress06():
        if len(str(label06.get()))>0:
            try:
                label06Value.set(str(label06Value.get())[-1])
            except:
                label06Value.set(0)
    label06 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label06Value)
    label06Value.trace("w",lambda *args: keyPress06())
else:    
    label06 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[0][6])+" ", borderwidth=1, relief='groove')
if board[0][7]==0:  
    def keyPress07():
        if len(str(label07.get()))>0:
            try:
                label07Value.set(str(label07Value.get())[-1])
            except:
                label07Value.set(0)
    label07 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label07Value)
    label07Value.trace("w",lambda *args: keyPress07())
else:    
    label07 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[0][7])+" ", borderwidth=1, relief='groove')
if board[0][8]==0:  
    def keyPress08():
        if len(str(label08.get()))>0:
            try:
                label08Value.set(str(label08Value.get())[-1])
            except:
                label08Value.set(0)
    label08 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label08Value)
    label08Value.trace("w",lambda *args: keyPress08())
else:    
    label08 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[0][8])+" ", borderwidth=1, relief='groove')

if board[1][0]==0:  
    def keyPress10():
        if len(str(label10.get()))>0:
            try:
                label10Value.set(str(label10Value.get())[-1])
            except:
                label10Value.set(0)
    label10 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label10Value)
    label10Value.trace("w",lambda *args: keyPress10())
else:
    label10 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[1][0])+" ", borderwidth=1, relief='groove')
if board[1][1]==0:  
    def keyPress11():
        if len(str(label11.get()))>0:
            try:
                label11Value.set(str(label11Value.get())[-1])
            except:
                label11Value.set(0)
    label11 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label11Value)
    label11Value.trace("w",lambda *args: keyPress11())
else:    
    label11 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[1][1])+" ", borderwidth=1, relief='groove')
if board[1][2]==0:  
    def keyPress12():
        if len(str(label12.get()))>0:
            try:
                label12Value.set(str(label12Value.get())[-1])
            except:
                label12Value.set(0)
    label12 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label12Value)
    label12Value.trace("w",lambda *args: keyPress12())
else:   
    label12 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[1][2])+" ", borderwidth=1, relief='groove')
if board[1][3]==0:  
    def keyPress13():
        if len(str(label13.get()))>0:
            try:
                label13Value.set(str(label13Value.get())[-1])
            except:
                label13Value.set(0)
    label13 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label13Value)
    label13Value.trace("w",lambda *args: keyPress13())
else:    
    label13 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[1][3]))
if board[1][4]==0:  
    def keyPress14():
        if len(str(label14.get()))>0:
            try:
                label14Value.set(str(label14Value.get())[-1])
            except:
                label14Value.set(0)
    label14 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label14Value)
    label14Value.trace("w",lambda *args: keyPress14())
else:
    label14 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[1][4]))
if board[1][5]==0:  
    def keyPress15():
        if len(str(label15.get()))>0:
            try:
                label15Value.set(str(label15Value.get())[-1])
            except:
                label15Value.set(0)
    label15 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label15Value)
    label15Value.trace("w",lambda *args: keyPress15())
else:
    label15 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[1][5]))
if board[1][6]==0:  
    def keyPress16():
        if len(str(label16.get()))>0:
            try:
                label16Value.set(str(label16Value.get())[-1])
            except:
                label16Value.set(0)
    label16 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label16Value)
    label16Value.trace("w",lambda *args: keyPress16())
else:
    label16 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[1][6])+" ", borderwidth=1, relief='groove')
if board[1][7]==0:  
    def keyPress17():
        if len(str(label17.get()))>0:
            try:
                label17Value.set(str(label17Value.get())[-1])
            except:
                label17Value.set(0)
    label17 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label17Value)
    label17Value.trace("w",lambda *args: keyPress17())
else:
    label17 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[1][7])+" ", borderwidth=1, relief='groove')
if board[1][8]==0:  
    def keyPress18():
        if len(str(label18.get()))>0:
            try:
                label18Value.set(str(label18Value.get())[-1])
            except:
                label18Value.set(0)
    label18 = Entry(root, bg='#C0C0C0', fg='#000000', bd=1, width=2, font=('Verdana',8), justify='center', textvariable=label18Value)
    label18Value.trace("w",lambda *args: keyPress18())
else:
    label18 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[1][8])+" ", borderwidth=1, relief='groove')

if board[2][0]==0:  
    def keyPress20():
        if len(str(label20.get()))>0:
            try:
                label20Value.set(str(label20Value.get())[-1])
            except:
                label20Value.set(0)
    label20 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label20Value)
    label20Value.trace("w",lambda *args: keyPress20())
else:
    label20 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[2][0])+" ", borderwidth=1, relief='groove')
if board[2][1]==0:  
    def keyPress21():
        if len(str(label21.get()))>0:
            try:
                label21Value.set(str(label21Value.get())[-1])
            except:
                label21Value.set(0)
    label21 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label21Value)
    label21Value.trace("w",lambda *args: keyPress21())
else:
    label21 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[2][1])+" ", borderwidth=1, relief='groove')
if board[2][2]==0:  
    def keyPress22():
        if len(str(label22.get()))>0:
            try:
                label22Value.set(str(label22Value.get())[-1])
            except:
                label22Value.set(0)
    label22 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label22Value)
    label22Value.trace("w",lambda *args: keyPress22())
else:
    label22 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[2][2])+" ", borderwidth=1, relief='groove')
if board[2][3]==0:  
    def keyPress23():
        if len(str(label23.get()))>0:
            try:
                label23Value.set(str(label23Value.get())[-1])
            except:
                label23Value.set(0)
    label23 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label23Value)
    label23Value.trace("w",lambda *args: keyPress23())
else:
    label23 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[2][3]))
if board[2][4]==0:  
    def keyPress24():
        if len(str(label24.get()))>0:
            try:
                label24Value.set(str(label24Value.get())[-1])
            except:
                label24Value.set(0)
    label24 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label24Value)
    label24Value.trace("w",lambda *args: keyPress24())
else:
    label24 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[2][4]))
if board[2][5]==0:  
    def keyPress25():
        if len(str(label25.get()))>0:
            try:
                label25Value.set(str(label25Value.get())[-1])
            except:
                label25Value.set(0)
    label25 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label25Value)
    label25Value.trace("w",lambda *args: keyPress25())
else:
    label25 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[2][5]))
if board[2][6]==0:  
    def keyPress26():
        if len(str(label26.get()))>0:
            try:
                label26Value.set(str(label26Value.get())[-1])
            except:
                label26Value.set(0)
    label26 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label26Value)
    label26Value.trace("w",lambda *args: keyPress26())
else:
    label26 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[2][6])+" ", borderwidth=1, relief='groove')
if board[2][7]==0:  
    def keyPress27():
        if len(str(label27.get()))>0:
            try:
                label27Value.set(str(label27Value.get())[-1])
            except:
                label27Value.set(0)
    label27 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label27Value)
    label27Value.trace("w",lambda *args: keyPress27())
else:
    label27 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[2][7])+" ", borderwidth=1, relief='groove')
if board[2][8]==0:  
    def keyPress28():
        if len(str(label28.get()))>0:
            try:
                label28Value.set(str(label28Value.get())[-1])
            except:
                label28Value.set(0)
    label28 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label28Value)
    label28Value.trace("w",lambda *args: keyPress28())
else:
    label28 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[2][8])+" ", borderwidth=1, relief='groove')

if board[3][0]==0:  
    def keyPress30():
        if len(str(label30.get()))>0:
            try:
                label30Value.set(str(label30Value.get())[-1])
            except:
                label30Value.set(0)
    label30 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label30Value)
    label30Value.trace("w",lambda *args: keyPress30())
else:
    label30 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[3][0]))
if board[3][1]==0:  
    def keyPress31():
        if len(str(label31.get()))>0:
            try:
                label31Value.set(str(label31Value.get())[-1])
            except:
                label31Value.set(0)
    label31 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label31Value)
    label31Value.trace("w",lambda *args: keyPress31())
else:
    label31 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[3][1]))
if board[3][2]==0:  
    def keyPress32():
        if len(str(label32.get()))>0:
            try:
                label32Value.set(str(label32Value.get())[-1])
            except:
                label32Value.set(0)
    label32 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label32Value)
    label32Value.trace("w",lambda *args: keyPress32())
else:
    label32 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[3][2]))
if board[3][3]==0:  
    def keyPress33():
        if len(str(label33.get()))>0:
            try:
                label33Value.set(str(label33Value.get())[-1])
            except:
                label33Value.set(0)
    label33 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label33Value)
    label33Value.trace("w",lambda *args: keyPress33())
else:
    label33 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[3][3])+" ", borderwidth=1, relief='groove')
if board[3][4]==0:  
    def keyPress34():
        if len(str(label34.get()))>0:
            try:
                label34Value.set(str(label34Value.get())[-1])
            except:
                label34Value.set(0)
    label34 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label34Value)
    label34Value.trace("w",lambda *args: keyPress34())
else:
    label34 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[3][4])+" ", borderwidth=1, relief='groove')
if board[3][5]==0:  
    def keyPress35():
        if len(str(label35.get()))>0:
            try:
                label35Value.set(str(label35Value.get())[-1])
            except:
                label35Value.set(0)
    label35 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label35Value)
    label35Value.trace("w",lambda *args: keyPress35())
else:
    label35 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[3][5])+" ", borderwidth=1, relief='groove')
if board[3][6]==0:  
    def keyPress36():
        if len(str(label36.get()))>0:
            try:
                label36Value.set(str(label36Value.get())[-1])
            except:
                label36Value.set(0)
    label36 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label36Value)
    label36Value.trace("w",lambda *args: keyPress36())
else:
    label36 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[3][6]))
if board[3][7]==0:  
    def keyPress37():
        if len(str(label37.get()))>0:
            try:
                label37Value.set(str(label37Value.get())[-1])
            except:
                label37Value.set(0)
    label37 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label37Value)
    label37Value.trace("w",lambda *args: keyPress37())
else:
    label37 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[3][7]))
if board[3][8]==0:  
    def keyPress38():
        if len(str(label38.get()))>0:
            try:
                label38Value.set(str(label38Value.get())[-1])
            except:
                label38Value.set(0)
    label38 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label38Value)
    label38Value.trace("w",lambda *args: keyPress38())
else:
    label38 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[3][8]))

if board[4][0]==0:  
    def keyPress40():
        if len(str(label40.get()))>0:
            try:
                label40Value.set(str(label40Value.get())[-1])
            except:
                label40Value.set(0)
    label40 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label40Value)
    label40Value.trace("w",lambda *args: keyPress40())
else:
    label40 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[4][0]))
if board[4][1]==0:  
    def keyPress41():
        if len(str(label41.get()))>0:
            try:
                label41Value.set(str(label41Value.get())[-1])
            except:
                label41Value.set(0)
    label41 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label41Value)
    label41Value.trace("w",lambda *args: keyPress41())
else:
    label41 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[4][1]))
if board[4][2]==0:  
    def keyPress42():
        if len(str(label42.get()))>0:
            try:
                label42Value.set(str(label42Value.get())[-1])
            except:
                label42Value.set(0)
    label42 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label42Value)
    label42Value.trace("w",lambda *args: keyPress42())
else:
    label42 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[4][2]))
if board[4][3]==0:  
    def keyPress43():
        if len(str(label43.get()))>0:
            try:
                label43Value.set(str(label43Value.get())[-1])
            except:
                label43Value.set(0)
    label43 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label43Value)
    label43Value.trace("w",lambda *args: keyPress43())
else:
    label43 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[4][3])+" ", borderwidth=1, relief='groove')
if board[4][4]==0:  
    def keyPress44():
        if len(str(label44.get()))>0:
            try:
                label44Value.set(str(label44Value.get())[-1])
            except:
                label44Value.set(0)
    label44 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label44Value)
    label44Value.trace("w",lambda *args: keyPress44())
else:
    label44 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[4][4])+" ", borderwidth=1, relief='groove')
if board[4][5]==0:  
    def keyPress45():
        if len(str(label45.get()))>0:
            try:
                label45Value.set(str(label45Value.get())[-1])
            except:
                label45Value.set(0)
    label45 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label45Value)
    label45Value.trace("w",lambda *args: keyPress45())
else:
    label45 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[4][5])+" ", borderwidth=1, relief='groove')
if board[4][6]==0:  
    def keyPress46():
        if len(str(label46.get()))>0:
            try:
                label46Value.set(str(label46Value.get())[-1])
            except:
                label46Value.set(0)
    label46 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label46Value)
    label46Value.trace("w",lambda *args: keyPress46())
else:
    label46 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[4][6]))
if board[4][7]==0:  
    def keyPress47():
        if len(str(label47.get()))>0:
            try:
                label47Value.set(str(label47Value.get())[-1])
            except:
                label47Value.set(0)
    label47 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label47Value)
    label47Value.trace("w",lambda *args: keyPress47())
else:
    label47 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[4][7]))
if board[4][8]==0:  
    def keyPress48():
        if len(str(label48.get()))>0:
            try:
                label48Value.set(str(label48Value.get())[-1])
            except:
                label48Value.set(0)
    label48 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label48Value)
    label48Value.trace("w",lambda *args: keyPress48())
else:
    label48 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[4][8]))

if board[5][0]==0:  
    def keyPress50():
        if len(str(label50.get()))>0:
            try:
                label50Value.set(str(label50Value.get())[-1])
            except:
                label50Value.set(0)
    label50 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label50Value)
    label50Value.trace("w",lambda *args: keyPress50())
else:
    label50 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[5][0]))
if board[5][1]==0:  
    def keyPress51():
        if len(str(label51.get()))>0:
            try:
                label51Value.set(str(label51Value.get())[-1])
            except:
                label51Value.set(0)
    label51 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label51Value)
    label51Value.trace("w",lambda *args: keyPress51())
else:
    label51 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[5][1]))
if board[5][2]==0:  
    def keyPress52():
        if len(str(label52.get()))>0:
            try:
                label52Value.set(str(label52Value.get())[-1])
            except:
                label52Value.set(0)
    label52 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label52Value)
    label52Value.trace("w",lambda *args: keyPress52())
else:
    label52 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[5][2]))
if board[5][3]==0:  
    def keyPress53():
        if len(str(label53.get()))>0:
            try:
                label53Value.set(str(label53Value.get())[-1])
            except:
                label53Value.set(0)
    label53 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label53Value)
    label53Value.trace("w",lambda *args: keyPress53())
else:
    label53 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[5][3])+" ", borderwidth=1, relief='groove')
if board[5][4]==0:  
    def keyPress54():
        if len(str(label54.get()))>0:
            try:
                label54Value.set(str(label54Value.get())[-1])
            except:
                label54Value.set(0)
    label54 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label54Value)
    label54Value.trace("w",lambda *args: keyPress54())
else:
    label54 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[5][4])+" ", borderwidth=1, relief='groove')
if board[5][5]==0:  
    def keyPress55():
        if len(str(label55.get()))>0:
            try:
                label55Value.set(str(label55Value.get())[-1])
            except:
                label55Value.set(0)
    label55 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label55Value)
    label55Value.trace("w",lambda *args: keyPress55())
else:
    label55 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[5][5])+" ", borderwidth=1, relief='groove')
if board[5][6]==0:  
    def keyPress56():
        if len(str(label56.get()))>0:
            try:
                label56Value.set(str(label56Value.get())[-1])
            except:
                label56Value.set(0)
    label56 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label56Value)
    label56Value.trace("w",lambda *args: keyPress56())
else:
    label56 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[5][6]))
if board[5][7]==0:  
    def keyPress57():
        if len(str(label57.get()))>0:
            try:
                label57Value.set(str(label57Value.get())[-1])
            except:
                label57Value.set(0)
    label57 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label57Value)
    label57Value.trace("w",lambda *args: keyPress57())
else:
    label57 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[5][7]))
if board[5][8]==0:  
    def keyPress58():
        if len(str(label58.get()))>0:
            try:
                label58Value.set(str(label58Value.get())[-1])
            except:
                label58Value.set(0)
    label58 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label58Value)
    label58Value.trace("w",lambda *args: keyPress58())
else:
    label58 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[5][8]))

if board[6][0]==0:  
    def keyPress60():
        if len(str(label60.get()))>0:
            try:
                label60Value.set(str(label60Value.get())[-1])
            except:
                label60Value.set(0)
    label60 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label60Value)
    label60Value.trace("w",lambda *args: keyPress60())
else:
    label60 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[6][0])+" ", borderwidth=1, relief='groove')
if board[6][1]==0:  
    def keyPress61():
        if len(str(label61.get()))>0:
            try:
                label61Value.set(str(label61Value.get())[-1])
            except:
                label61Value.set(0)
    label61 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label61Value)
    label61Value.trace("w",lambda *args: keyPress61())
else:
    label61 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[6][1])+" ", borderwidth=1, relief='groove')
if board[6][2]==0:  
    def keyPress62():
        if len(str(label62.get()))>0:
            try:
                label62Value.set(str(label62Value.get())[-1])
            except:
                label62Value.set(0)
    label62 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label62Value)
    label62Value.trace("w",lambda *args: keyPress62())
else:
    label62 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[6][2])+" ", borderwidth=1, relief='groove')
if board[6][3]==0:  
    def keyPress63():
        if len(str(label63.get()))>0:
            try:
                label63Value.set(str(label63Value.get())[-1])
            except:
                label63Value.set(0)
    label63 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label63Value)
    label63Value.trace("w",lambda *args: keyPress63())
else:
    label63 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[6][3]))
if board[6][4]==0:  
    def keyPress64():
        if len(str(label64.get()))>0:
            try:
                label64Value.set(str(label64Value.get())[-1])
            except:
                label64Value.set(0)
    label64 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label64Value)
    label64Value.trace("w",lambda *args: keyPress64())
else:
    label64 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[6][4]))
if board[6][5]==0:  
    def keyPress65():
        if len(str(label65.get()))>0:
            try:
                label65Value.set(str(label65Value.get())[-1])
            except:
                label65Value.set(0)
    label65 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label65Value)
    label65Value.trace("w",lambda *args: keyPress65())
else:
    label65 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[6][5]))
if board[6][6]==0:  
    def keyPress66():
        if len(str(label66.get()))>0:
            try:
                label66Value.set(str(label66Value.get())[-1])
            except:
                label66Value.set(0)
    label66 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label66Value)
    label66Value.trace("w",lambda *args: keyPress66())
else:
    label66 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[6][6])+" ", borderwidth=1, relief='groove')
if board[6][7]==0:  
    def keyPress67():
        if len(str(label67.get()))>0:
            try:
                label67Value.set(str(label67Value.get())[-1])
            except:
                label67Value.set(0)
    label67 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label67Value)
    label67Value.trace("w",lambda *args: keyPress67())
else:
    label67 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[6][7])+" ", borderwidth=1, relief='groove')
if board[6][8]==0:  
    def keyPress68():
        if len(str(label68.get()))>0:
            try:
                label68Value.set(str(label68Value.get())[-1])
            except:
                label68Value.set(0)
    label68 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label68Value)
    label68Value.trace("w",lambda *args: keyPress68())
else:
    label68 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[6][8])+" ", borderwidth=1, relief='groove')

if board[7][0]==0:  
    def keyPress70():
        if len(str(label70.get()))>0:
            try:
                label70Value.set(str(label70Value.get())[-1])
            except:
                label70Value.set(0)
    label70 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label70Value)
    label70Value.trace("w",lambda *args: keyPress70())
else:
    label70 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[7][0])+" ", borderwidth=1, relief='groove')
if board[7][1]==0:  
    def keyPress71():
        if len(str(label71.get()))>0:
            try:
                label71Value.set(str(label71Value.get())[-1])
            except:
                label71Value.set(0)
    label71 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label71Value)
    label71Value.trace("w",lambda *args: keyPress71())
else:
    label71 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[7][1])+" ", borderwidth=1, relief='groove')
if board[7][2]==0:  
    def keyPress72():
        if len(str(label72.get()))>0:
            try:
                label72Value.set(str(label72Value.get())[-1])
            except:
                label72Value.set(0)
    label72 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label72Value)
    label72Value.trace("w",lambda *args: keyPress72())
else:
    label72 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[7][2])+" ", borderwidth=1, relief='groove')
if board[7][3]==0:  
    def keyPress73():
        if len(str(label73.get()))>0:
            try:
                label73Value.set(str(label73Value.get())[-1])
            except:
                label73Value.set(0)
    label73 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label73Value)
    label73Value.trace("w",lambda *args: keyPress73())
else:
    label73 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[7][3]))
if board[7][4]==0:  
    def keyPress74():
        if len(str(label74.get()))>0:
            try:
                label74Value.set(str(label74Value.get())[-1])
            except:
                label74Value.set(0)
    label74 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label74Value)
    label74Value.trace("w",lambda *args: keyPress74())
else:
    label74 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[7][4]))
if board[7][5]==0:  
    def keyPress75():
        if len(str(label75.get()))>0:
            try:
                label75Value.set(str(label75Value.get())[-1])
            except:
                label75Value.set(0)
    label75 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label75Value)
    label75Value.trace("w",lambda *args: keyPress75())
else:
    label75 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), text=str(board[7][5]))
if board[7][6]==0:  
    def keyPress76():
        if len(str(label76.get()))>0:
            try:
                label76Value.set(str(label76Value.get())[-1])
            except:
                label76Value.set(0)
    label76 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label76Value)
    label76Value.trace("w",lambda *args: keyPress76())
else:
    label76 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[7][6])+" ", borderwidth=1, relief='groove')
if board[7][7]==0:  
    def keyPress77():
        if len(str(label77.get()))>0:
            try:
                label77Value.set(str(label77Value.get())[-1])
            except:
                label77Value.set(0)
    label77 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label77Value)
    label77Value.trace("w",lambda *args: keyPress77())
else:
    label77 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[7][7])+" ", borderwidth=1, relief='groove')
if board[7][8]==0:  
    def keyPress78():
        if len(str(label78.get()))>0:
            try:
                label78Value.set(str(label78Value.get())[-1])
            except:
                label78Value.set(0)
    label78 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label78Value)
    label78Value.trace("w",lambda *args: keyPress78())
else:
    label78 = Label(root, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[7][8])+" ", borderwidth=1, relief='groove')

if board[8][0]==0:  
    def keyPress80():
        if len(str(label80.get()))>0:
            try:
                label80Value.set(str(label80Value.get())[-1])
            except:
                label80Value.set(0)
    label80 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label80Value)
    label80Value.trace("w",lambda *args: keyPress80())
else:
    label80 = Label(root, bd=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), text=""+str(board[8][0])+" ", borderwidth=1, relief='groove')
if board[8][1]==0:  
    def keyPress81():
        if len(str(label81.get()))>0:
            try:
                label81Value.set(str(label81Value.get())[-1])
            except:
                label81Value.set(0)
    label81 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label81Value)
    label81Value.trace("w",lambda *args: keyPress81())
else:
    label81 = Label(root, bg='#C0C0C0', fg='#000000', bd=2, font=('Verdana',8), text=""+str(board[8][1])+" ", borderwidth=1, relief='groove')
if board[8][2]==0:  
    def keyPress82():
        if len(str(label82.get()))>0:
            try:
                label82Value.set(str(label82Value.get())[-1])
            except:
                label82Value.set(0)
    label82 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label82Value)
    label82Value.trace("w",lambda *args: keyPress82())
else:
    label82 = Label(root, bg='#C0C0C0', fg='#000000', bd=2, font=('Verdana',8), text=""+str(board[8][2])+" ", borderwidth=1, relief='groove')
if board[8][3]==0:  
    def keyPress83():
        if len(str(label83.get()))>0:
            try:
                label83Value.set(str(label83Value.get())[-1])
            except:
                label83Value.set(0)
    label83 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label83Value)
    label83Value.trace("w",lambda *args: keyPress83())
else:
    label83 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), bd=2, text=str(board[8][3]))
if board[8][4]==0:  
    def keyPress84():
        if len(str(label84.get()))>0:
            try:
                label84Value.set(str(label84Value.get())[-1])
            except:
                label84Value.set(0)
    label84 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label84Value)
    label84Value.trace("w",lambda *args: keyPress84())
else:
    label84 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), bd=2, text=str(board[8][4]))
if board[8][5]==0:  
    def keyPress85():
        if len(str(label85.get()))>0:
            try:
                label85Value.set(str(label85Value.get())[-1])
            except:
                label85Value.set(0)
    label85 = Entry(root, bd=1, bg='#FFFFFF', fg='#000000', width=2, font=('Verdana',8), justify='center', textvariable=label85Value)
    label85Value.trace("w",lambda *args: keyPress85())
else:
    label85 = Label(root, bg='#FFFFFF', fg='#000000', font=('Verdana',8), bd=2, text=str(board[8][5]))
if board[8][6]==0:  
    def keyPress86():
        if len(str(label86.get()))>0:
            try:
                label86Value.set(str(label86Value.get())[-1])
            except:
                label86Value.set(0)
    label86 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label86Value)
    label86Value.trace("w",lambda *args: keyPress86())
else:
    label86 = Label(root, bg='#C0C0C0', fg='#000000', bd=2, font=('Verdana',8), text=""+str(board[8][6])+" ", borderwidth=1, relief='groove')
if board[8][7]==0:  
    def keyPress87():
        if len(str(label87.get()))>0:
            try:
                label87Value.set(str(label87Value.get())[-1])
            except:
                label87Value.set(0)
    label87 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label87Value)
    label87Value.trace("w",lambda *args: keyPress87())
else:
    label87 = Label(root, bg='#C0C0C0', fg='#000000', bd=2, font=('Verdana',8), text=""+str(board[8][7])+" ", borderwidth=1, relief='groove')
if board[8][8]==0:  
    def keyPress88():
        if len(str(label88.get()))>0:
            try:
                label88Value.set(str(label88Value.get())[-1])
            except:
                label88Value.set(0)
    label88 = Entry(root, bd=1, width=2, bg='#C0C0C0', fg='#000000', font=('Verdana',8), justify='center', textvariable=label88Value)
    label88Value.trace("w",lambda *args: keyPress88())
else:
    label88 = Label(root, bg='#C0C0C0', fg='#000000', bd=2, font=('Verdana',8), text=""+str(board[8][8])+" ", borderwidth=1, relief='groove') 

def newWin():
    global newWinCount
    if not newWinCount:
        newWinCount=True
    else:
        return
    global attempt,sec,hour,min
    newWin = Toplevel(root)
    newWin.title('Sudoku - 9x9')
    try:
        newWin.iconbitmap('sudoku.ico')
    except:
        pass    
    
    newWin.protocol('WM_DELETE_WINDOW', lambda *args : sys.exit())
    newWin.bind('<Return>', lambda *args : sys.exit())
    newWin.bind('<Escape>', lambda *args : sys.exit())
    newWin.resizable(0,0)
    at = "Attempt : "+str(int(attempt))
    attemptLabel = Label(newWin, text=at, padx=80, pady=10, bg='#FFCCCB', fg='#000000', font=('Verdana',10))
    attemptLabel.grid(row=0, column=0)
    t = "Time taken : "
    sec -= 1
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
    timeLabel = Label(newWin, text=t, padx=45, pady=10, bg='#87CEEB', fg='#000000', font=('Verdana',10))
    timeLabel.grid(row=1, column=0)
    okButtton = Button(newWin, text='Ok', command=lambda : sys.exit(),width=12, font=('Verdana',10), bg='#000000', fg='#FFFFFF')
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
    global submitButtonCount,attempt,error
    attempt += 1
    submitButtonCount += 1
    error=0
    submit()

def changeColor(): 
    global board
    if not solved:
        submitButton.configure(state=NORMAL)

    if solveButtonCount==1:

        solveButton.configure(state=DISABLED)
        for i in range(0,9):
            for j in range(0,9):
                if board[i][j]==0:
                    if i in [0,1,2,6,7,8]:
                        if j in [0,1,2,6,7,8]:
                            labels[i][j].configure(state=DISABLED, disabledbackground='#C0C0C0', disabledforeground='#000000')
                        else:
                            labels[i][j].configure(state=DISABLED, disabledbackground='#FFFFFF', disabledforeground='#000000')
                    elif i in [3,4,5]:
                        if j in [3,4,5]:
                            labels[i][j].configure(state=DISABLED, disabledbackground='#C0C0C0', disabledforeground='#000000')
                        else:
                            labels[i][j].configure(state=DISABLED, disabledbackground='#FFFFFF', disabledforeground='#000000')
                    else:
                        labels[i][j].configure(bg='#FFFFFF', fg='#000000')
                
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
    global count,submitButtonCount,noOfEmpty,attempt,error,solved
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
                                error += 1
                        except:       
                            labels[i][j].configure(bg='#FFCCCB')
                            error += 1
                        k += 1
        count += 1
        if noOfEmpty==count:
            if error==0:
                solved=True
                newWin()
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
                                error += 1
                        except:       
                            labels[i][j].configure(bg='#FFCCCB')
                            error += 1
            count=0
            if error==0:
                solved=True
                newWin()
            root.after(3000,changeColor)
    del temp
    del t

def solve():
    global algorithm,solveButtonCount
    if len(algorithm)==0:
        
        solveButton.configure(state=DISABLED)
        solveButtonCount=1
        root.after(3000,changeColor)
        root.after(3000,newWin)

        return
    if algorithm[0][0]==True:
        entryValues[algorithm[0][1]][algorithm[0][2]].set(algorithm[0][3])
        labels[algorithm[0][1]][algorithm[0][2]].configure(state=DISABLED, disabledbackground='#87CEEB', disabledforeground='#000000')
    else:
        entryValues[algorithm[0][1]][algorithm[0][2]].set(algorithm[0][3])
        labels[algorithm[0][1]][algorithm[0][2]].configure(state=DISABLED, disabledbackground='#FFCCCB', disabledforeground='#000000')
    algorithm.pop(0)
    if(solveButtonCount==0):
        root.after(250,solve)
        root.after((len(algorithm)*250+3000),changeColor)
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
                    labels[i][j].configure(state=DISABLED, disabledbackground='#87CEEB', disabledforeground='#000000')        
        root.after(3000,changeColor)  
        algorithm.clear()   
        solve()
        solveButton.configure(state=DISABLED)  
    del temp
    del t

root.bind('<Return>', call_submit)
root.bind('<space>', call_solve)

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
    sec+=1
    if sec%2==0:
        timeLapse.configure(text=t, fg="#FFFFFF", bg="#000000")
    else:
        timeLapse.configure(text=t, fg="#000000", bg="#FFFFFF")
    
    if sec==60:
        min += 1
        sec = 0
    if min==60:
        hour += 1
        min = 0
    return t

submitButton = Button(root, text="Submit\n[Enter]", padx=23, pady=2, font=('Verdana',8), bg='#FFCCCB',fg='#000000', command=call_submit)
submitButton.grid(row=10, column=0, columnspan=3)

solveButton = Button(root, text="Solve\n[SpaceBar]", padx=10, pady=2, font=('Verdana',8), bg='#87CEEB', fg='#000000', command=call_solve)
solveButton.grid(row=10, column=2, columnspan=5)

timeLapse = Label(root, text=timeTaken(), padx=18, pady=10, font=('Verdana',8), fg="#000000", bg="#FFFFFF")
timeLapse.grid(row=10, column=6, columnspan=3)

root.mainloop()