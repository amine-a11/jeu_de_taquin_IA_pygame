class Node:
    def __init__(self,bord):
        self.bord=bord
        self.children=[]
        self.parent=None
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
        child=Node(aux)
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
        child=Node(aux)
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
        child=Node(aux)
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
        child=Node(aux)
        self.children.append(child)
        child.parent=self

# BORD=[
#     [3,2,7],
#     [8,6,0],
#     [1,5,4]
# ]

# TARGET=[
#     [1,2,3],
#     [8,0,4],
#     [7,6,5]
# ]
# def toString(b):
#     s=''
#     for i in b:
#         for j in i:
#             s+=str(j)
#     return s
# root=Node(BORD)
# nodes=[]
# nodes.append(root)
# visited=set()
# def showNodes(node):
#     if not node.parent:
#         print(node.bord)
#         return
#     showNodes(node.parent)
#     print(node.bord)
# while nodes :
#     if nodes[0].bord==TARGET:
#         showNodes(nodes[0])
#         break
#     nodes[0].allPossibleMoves()
#     for child in nodes[0].children:
#         if toString(child.bord) not in visited:
#             nodes.append(child)
#     visited.add(toString(nodes.pop(0).bord))

