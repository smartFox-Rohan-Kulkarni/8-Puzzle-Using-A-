import numpy as np
#random or user imput
#Class for state
    #state must contain datastructure to store state
    #and variables for parent f(n) g(n) and method to compute h(n) and update f(n)
#initilize lists OPEN and CLOSED
#impliment A*

goal=[]
start=[]
OPEN=[]
CLOSED=[]
genCnt=0
class state:
    def __init__(self, parent, board, g_n):
        if parent==None:
            self.parent=self
        else:
            self.parent = parent
        self.board = board
        self.myX=board.index('x')
        self.g_n=g_n
        self.f_n=(self.g_n)+self.compute_h_n()

    def compute_h_n(self):
        global goal
        temp_h=0
        for ele in range(9):
            if self.board[ele] != goal[ele]:
                temp_h+=1
        return temp_h

    def printall(self):
        print("parent",self.parent)
        print("board",self.board)
        print("g_n",self.g_n)
        print("fn",self.f_n)
        print("h_n",self.compute_h_n())

    def printBoard(self):
        print("|",self.board[0],"|","|",self.board[1],"|","|",self.board[2],"|")
        print("|", self.board[3], "|", "|", self.board[4], "|", "|", self.board[5], "|")
        print("|", self.board[6], "|", "|", self.board[7], "|", "|", self.board[8], "|")

    def find_my_X(self):
        return self.myX

    def genpath(self):

        parent=self
        grandparent =parent.parent
        #print(" \t  START\n\t\t|\n\t\tV")


        while parent != grandparent:
            print(parent,"g(n)",parent.g_n,"f(n)",parent.f_n)
            parent.printBoard()
            parent=grandparent
            grandparent=parent.parent
            print(" \t\t^\n\t\t|")

        if parent == grandparent:
            print(parent, "g(n)", parent.g_n, "f(n)", parent.f_n)
            parent.printBoard()
            print(" \t\t^\n\t\t|")
        print("\t  START")


def swapME(tboard,parentpos,childpos):
    tboard[parentpos], tboard[childpos] = tboard[childpos], tboard[parentpos]
    return tboard

def generateSuccessors(N):
    successors=[]
    GrandParent=N.parent
    first = {
        0: [1,3],1: [0,4,2],2: [1,5],3: [0,4,6],4: [1,3,5,7],5: [2,4,8],6: [3,7],7: [4,6,8],8:[5,7]
    }

    if N == GrandParent:
        for ele in first[N.myX]:
            tboard = swapME(N.board.copy(), N.myX, ele)
            temp = state(N, tboard.copy(), N.g_n + 1)
            successors.append(temp)
    else:
        for ele in first[N.myX]:
            if GrandParent.myX == ele:
                continue
            tboard = swapME(N.board.copy(), N.myX, ele)
            temp = state(N, tboard.copy(), N.g_n + 1)
            successors.append(temp)
    return successors

def A_star():
    global goal,OPEN,CLOSED,genCnt
    while OPEN !=[]:
        genCnt+=1
        OPEN.sort(key=lambda x : x.f_n)
        n=OPEN.pop(0)
        CLOSED.append(n)

        print("openlist cnt:",len(OPEN),":closed[]:",len(CLOSED),"pulled :N")
        n.printBoard()
        #if n is goal then return success
        if n.compute_h_n()==0:
            print("success:",n.compute_h_n())
            print("path")
            n.genpath()

            return

        #expand node n
        #swap pos having 'x' with neighbours to produce successors
        # and successor not being same as grand parent
        successors=generateSuccessors(n)
        print("GEN:",genCnt)
        c=0
        for i in successors:
            print(c,":")
            i.printBoard()
            c+=1
        #if any successor is goal return success
            if i.compute_h_n()==0:
                print("GEN success:",i.compute_h_n())
                print("path")
                i.genpath()
                return

        for s in successors:
            flag=True
            for c in CLOSED:
                #print(s.board, "->", c.board, "1->", s.board == c.board)
                if s.board==c.board:
                    if s.f_n >= c.f_n:
                        flag=False
                    else:
                        CLOSED.pop(CLOSED.index(c))

            for o in OPEN:
                #print(s.board,"->",o.board,"2->", s.board==o.board)
                if s.board==o.board:
                    if s.f_n >= o.f_n:
                        flag = False
                    else:
                        OPEN.pop(OPEN.index(o))

            if flag==True:
                OPEN.append(s)
    print("NO SOLUTION FOUND: SAMPLE SPACE SEARCHED:",len(CLOSED))

def checkSolvable(play):
    inversions = 0

    for i in range(0,len(play)) :
        for j in range(i+1,len(play)):
            if play[j]>play[i] :
                inversions+=1

    if inversions%2 == 1:
        return False
    else:
        return True

def callmemain():
    #| 1 | | 2 | | 3 |
    #| 4 | | x | | 5 |
    #| 6 | | 7 | | 8 |
    global goal,start,OPEN,CLOSED,genCnt
    genCnt=0
    goal = [1,3,2,5,4,7,6,8,'x']
    start=state(None,[1,2,3,5,'x',6,4,8,7],0)
    #start.printall()
    OPEN.append(start)
    CLOSED=[]
    print("START:")
    start.printBoard()
    tgoal=goal.copy().pop(goal.index('x'))
    tstart=start.board.copy().pop(start.board.index('x'))
    #A_star()
    #the checkSolvable module still has to be improved. i used this as an improvise  
    if not(np.logical_xor(checkSolvable(tstart), checkSolvable(tgoal))):
        print("It is Solvable")
        A_star()
    else:
        print("It is unSolvable")

callmemain()
