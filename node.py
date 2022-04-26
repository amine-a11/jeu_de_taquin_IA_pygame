class Node:
    def __init__(self,bord,g):
        self.bord=bord
        self.children=[]
        self.parent=None
        self.g=g
        self.f=0
    def get_empty_pos(self):
        for i in range(len(self.bord)):
            for j in range(len(self.bord[i])):
                if self.bord[i][j]==0:
                    return (i,j)
    def copyBord(self,b):
        for i in self.bord:
            temp=[]
            for j in i:
                temp.append(j)
            b.append(temp)

    def allPossibleMoves(self):
        self.move_up()
        self.move_down()
        self.move_right()
        self.move_left()
    def move_down(self):
        pos=self.get_empty_pos()
        if pos[0]+1>=3:
            return
        aux=[]
        self.copyBord(aux)
        x=pos[0]
        y=pos[1]
        aux[x][y],aux[x+1][y]=aux[x+1][y],aux[x][y]
        child=Node(aux,self.g+1)
        self.children.append(child)
        child.parent=self
    def move_up(self):
        pos=self.get_empty_pos()
        if pos[0]-1<0:
            return
        aux=[]
        self.copyBord(aux)
        x=pos[0]
        y=pos[1]
        aux[x][y],aux[x-1][y]=aux[x-1][y],aux[x][y]
        child=Node(aux,self.g+1)
        self.children.append(child)
        child.parent=self
    def move_right(self):
        pos=self.get_empty_pos()
        if pos[1]+1>=3:
            return
        aux=[]
        self.copyBord(aux)
        x=pos[0]
        y=pos[1]
        aux[x][y],aux[x][y+1]=aux[x][y+1],aux[x][y]
        child=Node(aux,self.g+1)
        self.children.append(child)
        child.parent=self
    def move_left(self):
        pos=self.get_empty_pos()
        if pos[1]-1<0:
            return
        aux=[]
        self.copyBord(aux)
        x=pos[0]
        y=pos[1]
        aux[x][y],aux[x][y-1]=aux[x][y-1],aux[x][y]
        child=Node(aux,self.g+1)
        self.children.append(child)
        child.parent=self
    def h(self,target):
        n=0
        y=0
        for i in self.bord:
            x=0
            for j in i:
                if j!=target[y][x] and j!=0:n+=1
                x+=1
            y+=1
        return n