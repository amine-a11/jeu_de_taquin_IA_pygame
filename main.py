import collections
from node import Node
from button import Button
import pygame
# pop up window test
# from pygame._sdl2 import messagebox
# answer = messagebox(
#     "I will open two windows! Continue?",
#     "Hello!",
#     info=True,
#     buttons=("Yes", "No", "Chance"),
#     return_button=0,
#     escape_button=1,
# )

pygame.font.init()
pygame.init()
pygame.mixer.init()
# -----------------------Start CONST-----------------------------------------------

SOUND=pygame.mixer.Sound('clack.wav')
LARGEUR=False
PROFONDEUR=False
ASTAR=False
FONT=pygame.font.SysFont('comicsans',40)
FONT2=pygame.font.SysFont('comicsans',20)
BORDSIZE=3
BORD=[
    [3,2,7],
    [8,6,0],
    [1,5,4]
]
TARGET=[
    [1,2,3],
    [8,0,4],
    [7,6,5]
]
SBS=6
WIDTH,HEIGHT=700,500
GAME_WIDTH,GAME_HEIGHT=300,300
SQUARESIZE=GAME_HEIGHT/BORDSIZE
SOLUTIONPATH_LARGEUR=[]
SOLUTIONPATH_PROFONDEUR=[]
SOLUTIONPATH_ASTAR=[]
FPS=60
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
WHITE=(255,255,255)
ALGS=[
    ["Largeur",100,GAME_HEIGHT+30,110,40],
    ["Profondeur",100+110+30,GAME_HEIGHT+30,110,40],
    ["Prof limite",100+110*2+60,GAME_HEIGHT+30,110,40],
    ["A*",100+110*3+90,GAME_HEIGHT+30,100,40]
]
b1=Button(100,GAME_HEIGHT+30,ALGS[0][0],WIN,110,40)
b2=Button(100+110+30,GAME_HEIGHT+30,ALGS[1][0],WIN,110,40)
b3=Button(100+110*2+60,GAME_HEIGHT+30,ALGS[2][0],WIN,110,40)
b4=Button(100+110*3+90,GAME_HEIGHT+30,ALGS[3][0],WIN,100,40)

nbdenoeudsvisites={'Largeur':-1,'Profondeur':-1,'Prof limite':-1,'A*':-1}
BACKGROUNDIMAGE=pygame.transform.scale(pygame.image.load('background_image.jpg'),(WIDTH,HEIGHT))
MAIN_MENU_BACKGROUNDIMAGE=pygame.transform.scale(pygame.image.load('main_menu_background_image.png'),(WIDTH,HEIGHT))
# -----------------------End CONST-----------------------------------------------

# --------------------Star window title and icon-------------------------------

pygame.display.set_caption("jeu taquin")

# --------------------End window title and icon-------------------------------


# ------------------------------------Start play mode----------------------------------------

# pos => position of the mouse (pygame.mouse.get_pos())
def move(pos):
    mousex=pos[0]
    mousey=pos[1]
    bordI=int((mousey)/SQUARESIZE)
    bordJ=int((mousex-(WIDTH-GAME_WIDTH)/2)/SQUARESIZE)
    dx,dy=0,0
    if bordI+1<3 and BORD[bordI+1][bordJ]==0:dx=1
    if bordJ+1<3 and BORD[bordI][bordJ+1]==0:dy=1
    if bordJ-1>=0 and BORD[bordI][bordJ-1]==0:dy=-1
    if bordI-1>=0 and BORD[bordI-1][bordJ]==0:dx=-1
    BORD[bordI][bordJ],BORD[bordI+dx][bordJ+dy]=BORD[bordI+dx][bordJ+dy],BORD[bordI][bordJ]
    SOUND.play()

# ------------------------------------End play mode----------------------------------------


# ------------------------------------Start Recherche en largeur----------------------------------------------

def getSolPath(node,tab):
    if not node.parent:
        tab.append(node.bord)
        return
    getSolPath(node.parent,tab)
    tab.append(node.bord)

def toString(b):
    s=''
    for i in b:
        for j in i:s+=str(j)
    return s

def solve_largeur():
    root=Node(BORD,0)
    nodes=[]
    nodes.append(root)
    visited=set()
    n=0
    while nodes :
        if nodes[0].bord==TARGET:
            getSolPath(nodes[0],SOLUTIONPATH_LARGEUR)
            print("DONE")
            break
        nodes[0].allPossibleMoves()
        for child in nodes[0].children:
            if toString(child.bord) not in visited:
                n+=1
                nodes.append(child)
                visited.add(toString(child.bord))
        nodes.pop(0)
    global LARGEUR
    LARGEUR=True
    nbdenoeudsvisites['Largeur']=n
    pygame.time.set_timer(pygame.USEREVENT,250)

def showSolution(nb,tab):
    nb[0]+=1
    if nb[0]>=len(tab):
        global LARGEUR
        LARGEUR=False
        global PROFONDEUR
        PROFONDEUR=False
        global ASTAR
        ASTAR=False

        nb[0]=0
        pygame.time.set_timer(pygame.USEREVENT,0)
        return
    for i in range(3):
        for j in range(3):
            BORD[i][j]=tab[nb[0]][i][j]
    SOUND.play()

# ------------------------------------End Recherche en largeur----------------------------------------------

# ------------------------------------Start Recherche en Profondeur----------------------------------------------
def getsolpath2(node):
    global SOLUTIONPATH_PROFONDEUR
    while node.parent:
        SOLUTIONPATH_PROFONDEUR.append(node.bord)
        node=node.parent
    SOLUTIONPATH_PROFONDEUR=SOLUTIONPATH_PROFONDEUR[::-1]
def solve_profondeur():
    root=Node(BORD,0)
    nodes=[]
    nodes.append(root)
    visited=set()
    n=0
    while nodes :
        node = nodes.pop()
        visited.add(toString(node.bord))
        if node.bord==TARGET:
            print("DONE")
            getsolpath2(node)
            break
        node.allPossibleMoves()
        for child in node.children:
            if toString(child.bord) not in visited:
                n+=1
                nodes.append(child)
                visited.add(toString(child.bord))
    global PROFONDEUR
    PROFONDEUR=True
    nbdenoeudsvisites['Profondeur']=n
    print(len(SOLUTIONPATH_PROFONDEUR))
    pygame.time.set_timer(pygame.USEREVENT,1)     


# ------------------------------------End Recherche en Profondeur----------------------------------------------
# ------------------------------------Start Recherche A*----------------------------------------------
def solve_Astar():
    root=Node(BORD,0)
    root.f=root.h(TARGET)+root.g
    n=0
    queue=collections.deque([root])
    visited=set()
    visited.add(root)
    while queue:
        queue=collections.deque(sorted(list(queue),key=lambda node:node.f))
        node=queue.popleft()
        if node.bord==TARGET:
            print("DONE")
            # print(node.bord)
            getSolPath(node,SOLUTIONPATH_ASTAR)
            break
        node.allPossibleMoves()
        for child in node.children:
            if toString(child.bord) not in visited:
                n+=1
                child.f=child.h(TARGET)+child.g
                print(child.h(TARGET))
                queue.appendleft(child)
                visited.add(toString(child.bord))
    global ASTAR
    ASTAR=True
    nbdenoeudsvisites['A*']=n
    print(len(SOLUTIONPATH_ASTAR))
    pygame.time.set_timer(pygame.USEREVENT,250)



# ------------------------------------End Recherche A*----------------------------------------------

#-------------------------------------Start Draw functions----------------------------------------

def reset_bord():
    global BORD
    BORD=[
    [3,2,7],
    [8,6,0],
    [1,5,4]
    ]

def display_bord():
    # pygame.draw.rect(WIN,(255,0,0),[(WIDTH-GAME_WIDTH)/2, 0, GAME_WIDTH, GAME_HEIGHT],1)
    for i in range(3):
        for j in range(3):
            if BORD[i][j]==0:continue
            rectX=(WIDTH-GAME_WIDTH)/2+j*SQUARESIZE+SBS/2
            rectY=i*SQUARESIZE+SBS/2
            pygame.draw.rect(WIN,(0,0,255),[rectX,rectY,SQUARESIZE-SBS,SQUARESIZE-SBS],border_radius=15)
            x=FONT.render(str(BORD[i][j]),1,(0,0,0))
            textX=(WIDTH-GAME_WIDTH)/2+(SQUARESIZE/2-(x.get_width())/2)+j*SQUARESIZE
            textY=i*SQUARESIZE+20
            WIN.blit(x,(textX,textY))


def display_algo():
    if b1.draw_button():
        reset_bord()
        solve_largeur()
    if b2.draw_button():
        reset_bord()
        solve_profondeur()
    if b3.draw_button():
        print(b3.text)
    if b4.draw_button():
        reset_bord()
        solve_Astar()
    for algo in ALGS:
        pygame.draw.rect(WIN,pygame.Color(192,192,192),[algo[1],algo[2]+60,algo[3],algo[4]])
        x=FONT2.render(str(nbdenoeudsvisites[algo[0]]),1,(0,0,0))
        WIN.blit(x,(algo[1]+abs(x.get_width()-algo[3])/2,algo[2]+60))

#-------------------------------------End Draw functions----------------------------------------


def main():
    clock=pygame.time.Clock()
    run=True
    prof=[0]
    lar=[0]
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.USEREVENT:
                if LARGEUR:
                    showSolution(lar,SOLUTIONPATH_LARGEUR)
                if PROFONDEUR:
                    showSolution(prof,SOLUTIONPATH_PROFONDEUR)
                if ASTAR:
                    showSolution(prof,SOLUTIONPATH_ASTAR)

            if event.type==pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                # play mode 
        # WIN.fill(WHITE)
        WIN.blit(BACKGROUNDIMAGE,(0,0))
        display_bord()
        display_algo()
        pygame.display.update()
    pygame.quit()

# ---------------------------------Start of main_menu-------------------------

def main_menu():
    clock=pygame.time.Clock()
    run=True
    btn=Button(200,100,"Experimental Mode",WIN,110,40,(255,255,255))
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()

        WIN.blit(MAIN_MENU_BACKGROUNDIMAGE,(0,0))
        if btn.draw_button():
            print("hello")

        pygame.display.update()
    pygame.quit()


# ---------------------------------end of main_menu-------------------------
# =============================
if __name__=="__main__":
    main()
    # main_menu()
    