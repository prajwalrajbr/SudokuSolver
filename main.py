import requests
import json
from random import choice
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
        print("BEFORE:")                      
        self.showBoard()
        self.solve()
        print("AFTER:")
        self.showBoard()

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

#stop = timeit.default_timer()
#print (stop-start)