
board=[
    [1,2,0,4,5,6,7,8,9],
    [1,2,3,4,5,0,7,8,9],
    [1,2,0,4,5,6,7,8,9],
    [9,2,3,0,5,6,7,8,9],
    [1,2,3,4,5,0,7,8,9],
    [1,2,3,0,5,6,7,8,9],
    [6,2,3,4,5,6,7,8,9],
    [1,2,3,0,5,6,7,8,9],
    [1,2,3,4,5,0,7,8,9]
      ]



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