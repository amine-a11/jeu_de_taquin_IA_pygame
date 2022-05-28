import collections
from node import Node
from button import Button
from random import randint
import pygame
import pygame_menu
from pygame._sdl2 import messagebox
pygame.font.init()
pygame.init()
pygame.mixer.init()
# -----------------------Start CONST-----------------------------------------------

SOUND=pygame.mixer.Sound('clack.wav')
SHUFFLE_NUMBER=100
LARGEUR=False
PROFONDEUR=False
ASTAR=False
PROFONDEUR_LIMITE=False
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
def reset_bord():
    global BORD
    BORD=[
        [3,2,7],
        [8,6,0],
        [1,5,4]
    ]

BORDTOPLAY=[
    [1,2,3],
    [4,5,6],
    [7,8,0]
]
def reset_bordtoplay():
    global BORD
    BORD=[
        [1,2,3],
        [4,5,6],
        [7,8,0]
    ]

SBS=6
WIDTH,HEIGHT=700,500
GAME_WIDTH,GAME_HEIGHT=300,300
SQUARESIZE=GAME_HEIGHT/BORDSIZE
SOLUTIONPATH_LARGEUR=[]
SOLUTIONPATH_PROFONDEUR=[]
SOLUTIONPATH_ASTAR=[]
SOLUTIONPATH_PROFONDEUR_LIMITE=[]
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
b5=Button(20,20,"back to menu",WIN,150,30)
b6=Button(10,GAME_HEIGHT+65,"Reset",WIN,50,30)

nbdenoeudsvisites={'Largeur':-1,'Profondeur':-1,'Prof limite':-1,'A*':-1}
BACKGROUNDIMAGE=pygame.transform.scale(pygame.image.load('background_image.jpg'),(WIDTH,HEIGHT))
# -----------------------End CONST-----------------------------------------------

# --------------------Star window title and icon-------------------------------

pygame.display.set_caption("jeu taquin")

# --------------------End window title and icon-------------------------------
#--------------------------Start shuffle bord---------------------------------

def shuffle_bord():
    global BORDTOPLAY
    for _ in range(SHUFFLE_NUMBER):
        bordI=randint(0,2)
        bordJ=randint(0,2)
        dx,dy=0,0
        if bordI+1<3 and BORDTOPLAY[bordI+1][bordJ]==0:dx=1
        if bordJ+1<3 and BORDTOPLAY[bordI][bordJ+1]==0:dy=1
        if bordJ-1>=0 and BORDTOPLAY[bordI][bordJ-1]==0:dy=-1
        if bordI-1>=0 and BORDTOPLAY[bordI-1][bordJ]==0:dx=-1
        BORDTOPLAY[bordI][bordJ],BORDTOPLAY[bordI+dx][bordJ+dy]=BORDTOPLAY[bordI+dx][bordJ+dy],BORDTOPLAY[bordI][bordJ]


#--------------------------end shuffle bord---------------------------------

# ------------------------------------Start play mode----------------------------------------

# pos => position of the mouse (pygame.mouse.get_pos())
def move(pos):
    mousex=pos[0]
    mousey=pos[1]
    var1=(WIDTH-GAME_WIDTH)/2
    var2=(WIDTH+GAME_WIDTH)/2
    if mousex>var1 and mousex<var2 and mousey>0 and mousey<GAME_HEIGHT:
        bordI=int((mousey)/SQUARESIZE)
        bordJ=int((mousex-(WIDTH-GAME_WIDTH)/2)/SQUARESIZE)
        dx,dy=0,0
        if bordI+1<3 and BORDTOPLAY[bordI+1][bordJ]==0:dx=1
        if bordJ+1<3 and BORDTOPLAY[bordI][bordJ+1]==0:dy=1
        if bordJ-1>=0 and BORDTOPLAY[bordI][bordJ-1]==0:dy=-1
        if bordI-1>=0 and BORDTOPLAY[bordI-1][bordJ]==0:dx=-1
        if dx!=0 or dy!=0:
            SOUND.play()
        BORDTOPLAY[bordI][bordJ],BORDTOPLAY[bordI+dx][bordJ+dy]=BORDTOPLAY[bordI+dx][bordJ+dy],BORDTOPLAY[bordI][bordJ]

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
def getsolpath3(node):
    global SOLUTIONPATH_PROFONDEUR_LIMITE
    while node.parent:
        SOLUTIONPATH_PROFONDEUR_LIMITE.append(node.bord)
        node=node.parent
    SOLUTIONPATH_PROFONDEUR_LIMITE=SOLUTIONPATH_PROFONDEUR_LIMITE[::-1]

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




#----------------------------------------prof limite------------------------
def solve_profondeur_limite(lim):
    root=Node(BORD,0)
    nodes=[]
    nodes.append(root)
    visited=set()
    n=0
    found=False
    while nodes :
        node = nodes.pop()
        visited.add(toString(node.bord))
        if node.bord==TARGET:
            print("DONE")
            found=True
            getsolpath3(node)
            break
        node.allPossibleMoves()
        for child in node.children:
            if toString(child.bord) not in visited and child.g<=lim:
                n+=1
                nodes.append(child)
                visited.add(toString(child.bord))
    if not found:
        messagebox(
            "info",
            "There's no solution",
            info=True,
        )
        return 

    global PROFONDEUR_LIMITE
    PROFONDEUR_LIMITE=True
    nbdenoeudsvisites['Prof limite']=n
    print(len(SOLUTIONPATH_PROFONDEUR_LIMITE))
    pygame.time.set_timer(pygame.USEREVENT,100)     

#----------------------------------------end prof limite------------------------

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
            getSolPath(node,SOLUTIONPATH_ASTAR)
            break
        node.allPossibleMoves()
        for child in node.children:
            if toString(child.bord) not in visited:
                n+=1
                child.f=child.h(TARGET)+child.g
                # print(child.h(TARGET))
                queue.appendleft(child)
                visited.add(toString(child.bord))
    global ASTAR
    ASTAR=True
    nbdenoeudsvisites['A*']=n
    print(len(SOLUTIONPATH_ASTAR))
    pygame.time.set_timer(pygame.USEREVENT,250)



# ------------------------------------End Recherche A*----------------------------------------------

#-------------------------------------Start Draw functions----------------------------------------


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

def display_bordtoplay():
    # pygame.draw.rect(WIN,(255,0,0),[(WIDTH-GAME_WIDTH)/2, 0, GAME_WIDTH, GAME_HEIGHT],1)
    for i in range(3):
        for j in range(3):
            if BORDTOPLAY[i][j]==0:continue
            rectX=(WIDTH-GAME_WIDTH)/2+j*SQUARESIZE+SBS/2
            rectY=i*SQUARESIZE+SBS/2
            pygame.draw.rect(WIN,(0,0,255),[rectX,rectY,SQUARESIZE-SBS,SQUARESIZE-SBS],border_radius=15)
            x=FONT.render(str(BORDTOPLAY[i][j]),1,(0,0,0))
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
        reset_bord()
        solve_profondeur_limite(20)
    if b4.draw_button():
        reset_bord()
        solve_Astar()
    if b5.draw_button():
        main_menu()
    if b6.draw_button():
        reset_bord()
    for algo in ALGS:
        pygame.draw.rect(WIN,pygame.Color(192,192,192),[algo[1],algo[2]+60,algo[3],algo[4]])
        x=FONT2.render(str(nbdenoeudsvisites[algo[0]]),1,(0,0,0))
        WIN.blit(x,(algo[1]+abs(x.get_width()-algo[3])/2,algo[2]+60))

#-------------------------------------End Draw functions----------------------------------------


def main():
    reset_bord()
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
                if PROFONDEUR_LIMITE:
                    showSolution(prof,SOLUTIONPATH_PROFONDEUR_LIMITE)

        # WIN.fill(WHITE)
        WIN.blit(BACKGROUNDIMAGE,(0,0))
        display_bord()
        display_algo()
        pygame.display.update()
    pygame.quit()

# ---------------------------------Start of play Mode-------------------------
def Play_Mode():
    clock=pygame.time.Clock()
    run=True
    shuffle_bord()
    you_win=False
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                move((x,y))
                if BORDTOPLAY==[[1,2,3],[4,5,6],[7,8,0]]:
                    you_win=True

        WIN.blit(BACKGROUNDIMAGE,(0,0))
        display_bordtoplay()
        if b5.draw_button():
            main_menu()
        pygame.display.update()
        if you_win:
            answer = messagebox(
                "Congrats",
                "Do you wanna play again",
                info=True,
                buttons=("No", "Yes"),
                return_button=0,
                escape_button=1,
            )
            if answer:
                you_win=False
                reset_bordtoplay()
                shuffle_bord()
            else:
                main_menu()

    pygame.quit()
    


# ---------------------------------end of Play Mode-------------------------
# ----------------------------------start main menu----------------------------

def main_menu():
    menu = pygame_menu.Menu('Jeu Taquin', WIDTH, HEIGHT,
                       theme=pygame_menu.themes.THEME_BLUE)
    # menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
    menu.add.button('Experimental Mode', main)
    menu.add.button('Play Mode', Play_Mode)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(WIN)

# ----------------------------------End main menu---------------------------- 
# =============================
if __name__=="__main__":
    main_menu()
    