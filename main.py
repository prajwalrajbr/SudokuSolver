
board=[
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,5],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
      ]



def findEmpty():
    for i in range(0,9):
        for j in range(0,9):
            if board[i][j]==0:
                return i,j

def checkIfValid(value,row,col):
    global board
    #Row checker
    for i in range(0,9):
        if board[i][col]==value and i!=row:
            return False

    #Column checker
    for i in range(0,9):
        if board[row][i]==value and i!=col:
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

def showBoard():
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
                   
showBoard()