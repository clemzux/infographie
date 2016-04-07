from OpenGL.GL import *  # car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *
from time import sleep
import sys


# var globales

# parametres source lumineuse
    # Couleur
light_diffuse = [1.0 , 1.0, 1.0, 0.0]
    # Position
light_position = [1.0 , 1.0, 1.0, 0.0]

# position camera
i = 0.0
j = 0.0
z = 5.0
centeri = 0.0
centerj = 0.0
centerz = 0.0
flag = True # indicateur pour la camera (position z)

quadric = None

# couleurs

r = 0.0
g = 0.0
b = 0.0

# la taille est une sorte d'echelle 

taille = 0.2

# guidage canon

xC = 0.0 # position en x
zC = 0.0 # position en z
direction = 'E' # orientation actuelle du canon
directionDeg = 0.0 # cette var change par pas de 90deg ou 180deg pour changer l'orientation du canon
orientationCanon = -30 # orientation du canon en deg par rapport au sol

xBoulet = 0.0
yBoulet = 0.0

# limites (coordonnees des bords a ne pas depasser)

xLimiteDroite = 0.8
xLimiteGauche = -0.8
zLimiteHaut = -1.8
zLimiteBas = 1.8


####################################
####### Fonctions objets3D #########
####################################


def setRGB(i, j, k): # permet juste de changer les couleurs en factorisant un peu le code
    
    global r, g, b
    
    r = i
    g = j
    b = k


def fabriquerRectangle(taille):

    glColor3f(r, g, b)
    glutSolidCube(taille)
    glutSwapBuffers()
    

def fabriquerTerrain():
    
    glPushMatrix()
    
    # couleur bleue de l'eau
    setRGB(0.0,0.0,1.0)
    # on formate le cube
    glScalef(1,0.1,1)
    fabriquerRectangle(4)
    
    glPopMatrix()
    glPushMatrix()
    
    # on se deplace vers la gauche pour creer un carre d'herbe
    glTranslatef(-3.0, 0.0, 0.0)
    # couleur verte de l'herbe
    setRGB(0.0, 1.0, 0.0)
    # on formate de cube
    glScalef(1, 0.1, 2)
    fabriquerRectangle(2)
    
    glPopMatrix()
    glPushMatrix()
    
    # on se deplace vers la droite pour creer un carre d'herbe
    glTranslatef(3.0, 0.0, 0.0)
    # on formate le cube
    glScalef(1, 0.1, 2)
    fabriquerRectangle(2)
    
    glPopMatrix()
    

def fabriquerRoue(taille):

    # fabrication d'une roue
    
    glPushMatrix()

    # couleur marron de la roue (cylindre)
    glColor3f(0.4, 0.2, 0.05)
    
    # cylindre "surface qui touche le sol"
    gluCylinder(gluNewQuadric(), taille, taille, taille/3, 20, 20)
    # disque equivalent a un "chapeau de roue"
    gluDisk(gluNewQuadric(), taille-(taille-(taille*0.15)), taille, 20, 20)
    
    # axe au centre du chapeau de roue
    # couleur grise de l'axe
    glColor3f(0.36, 0.36, 0.36)
    # affichage du disque "axe de roue"
    gluDisk(gluNewQuadric(), 0, taille-(taille-(taille*0.15)), 12, 12)
    
    # on se deplace pour dessiner la seconde roue
    glTranslate(0.0, 0.0, taille/3)
    # couleur marron du chapeau de roue
    glColor3f(0.4, 0.2, 0.05)
    # affichage du disque "chapeau de roue"
    gluDisk(gluNewQuadric(), taille-(taille-(taille*0.15)), taille, 12, 12)
    
    # axe au centre du chapeau de roue
    # couleur grise de l'axe
    glColor3f(0.36, 0.36, 0.36)
    # affichage du disque "axe de roue"
    gluDisk(gluNewQuadric(), 0, taille-(taille-(taille*0.15)), 20, 20)
    
    glPopMatrix()
    
    
def fabriquerTube(taille):

    # fabrication tube du canon

    glPushMatrix()
    
    # couleur grise du tube du canon
    glColor3f(0.36, 0.36, 0.36)
    
    # affichage du canon
    # on oriente le tube de facon a ce qu'il soit parallele aux roues
    glRotate(90, 0.0, 1.0, 0.0)
    # on oriente le canon vers le haut a 30deg
    glRotate(orientationCanon, 1.0, 0.0, 0.0)
    # affichage du tube
    gluCylinder(gluNewQuadric(), taille*0.5, taille*0.5*0.75, taille*4, 15, 15)
    
    # on fabrique le boulet :D
    # on change la couleur du boulet , un peu plus sombre que le canon
    glColor3f(0.2, 0.2, 0.2)
    # on applique une rotation pour remetre l'axe en place
    glRotate(-90, 0.0, 1.0, 0.0)
    # on cree le boulet au fond du canon mais on prevoit de le faire bouger
    print(xBoulet, yBoulet)
    glTranslate(0.0 + xBoulet , 0.0 + yBoulet, 0.0)
    gluSphere(gluNewQuadric(), taille*0.5*0.75, 20, 20)
    
    glPopMatrix()
    
    
def fabriquerCanon(taille):

    # on se deplace sur le terrain de gauche
    glTranslate(-3.0+xC, 0.3, 0.0+zC)
    
    # direction du canon
    glRotate(directionDeg, 0.0, 1.0, 0.0)

    # on deplace legerement la roue vers la camera (axe Z par rapport a l'endroit ou on se trouve)
    glTranslate(0.0, 0.0, taille*0.85)
    # fabrication d'une roue
    fabriquerRoue(taille*0.7)
    
    # vu qu'on fait un popMatrix , on retourne au bon endroit (sur le terrain de gauche)
    # glTranslate(-3.0, 0.5, 0.0)
    
    # on eloigne legerement la roue de la camera (axe Z par rapport a l'endroit ou on se trouve)
    glTranslate(0.0, 0.0, -((taille*0.85)*2))
    # fabrication d'une roue
    fabriquerRoue(taille*0.7)
    
    # on on retourne au centre des deux roues
    glTranslate(0.0, 0.0, taille*0.85)
    # on recule legerement le tube du canon
    glTranslate(-(taille), 0.0, 0.0)
    # fabrication du tube du canon
    fabriquerTube(taille)
    
    # on fabrique le fond du canon
    gluSphere(gluNewQuadric(), taille*0.49, 20, 20)
    
    
def keyboard(key, x, y):

    global i, j, z, centeri, centerj, centerz, flag # vars de guidage camera
    global xC, zC, direction, directionDeg, orientationCanon # vars de guidage du canon
    global xBoulet, yBoulet # var de trajectoire du boulet
    
    # guidage camera
    
    if key == 'o':
        z -= 0.5
        centerj -= 0.5
    elif key == 'l':
        z += 0.5
        centerj += 0.5
    elif key == 'k':
        i -= 0.5
        centeri += 0.5
        
        if (i < 0):
            z -= 0.5
        else:
            z += 0.5
    elif key == 'm':
        i += 0.5
        centeri -= 0.5
        
        if (i < 0):
            z += 0.5
        else:
            z -= 0.5
        
    # guidage canon
    
    elif key == 'z':
    
        if (zC > zLimiteHaut):
            zC -= 0.1
        
        if (direction == 'E'):
            directionDeg += 90
        elif (direction == 'O'):
            directionDeg -= 90
        elif (direction == 'S'):
            directionDeg += 180
            
        direction = 'N'
        
    elif key == 's':
    
        if (zC < zLimiteBas):
            zC += 0.1
        
        if (direction == 'E'):
            directionDeg -= 90
        elif (direction == 'O'):
            directionDeg += 90
        elif (direction == 'N'):
            directionDeg -= 180
        
        direction = 'S'
        
    elif key == 'q':
        
        if (xC > xLimiteGauche):
            xC -= 0.1
        
        if (direction == 'E'):
            directionDeg += 180
        elif (direction == 'S'):
            directionDeg -= 90
        elif (direction == 'N'):
            directionDeg += 90
        
        direction = 'O'
        
    elif key == 'd':
    
        if (xC < xLimiteDroite):
            xC += 0.1
        
        if (direction == 'O'):
            directionDeg += 180
        elif (direction == 'S'):
            directionDeg += 90
        elif (direction == 'N'):
            directionDeg -= 90
        
        direction = 'E'
        
    elif key == 'r':
        orientationCanon -= 1
        
    elif key == 'f':
        orientationCanon += 1
    
    elif key == 'e':
        
        cpt = 0;
        
        while (cpt < 50):
            xBoulet += 0.05
            
            if ( cpt > 25):
                yBoulet -= 0.05
            else:
                yBoulet += 0.05
            cpt+=1
            sleep(0.1)
            fabriquerTube(taille)
        
    # touche echap pour quitter
    elif key == '\033':
        sys.exit( )
    glutPostRedisplay()  # indispensable en Python


####################################
###### Fonctions de gestion ########
####################################


def init():

    global quadric
    # Autorisation des sources de lumiere
    glEnable(GL_LIGHTING)
    # Autorisation pour la source de lumiere 0
    glEnable(GL_LIGHT0)
    # Autorisation des couleurs
    glEnable(GL_COLOR_MATERIAL)

    glEnable(GL_DEPTH_TEST)
    # camera
    # position, oeuil, ...
    # gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    # Couleur de fond (ici noir)
    glClearColor (0.0, 0.0, 0.0, 0.0)
    glShadeModel(GL_SMOOTH)
    quadric = gluNewQuadric()
    # Affichage de solides et non de traits
    gluQuadricDrawStyle(quadric, GLU_FILL)
    # Declaration de la source de lumiere n0
    # ---Couleur
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    # ---Position
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    
    # autoriser textures
    glEnable(GL_TEXTURE_2D)
    
    
def display():

    # Le 2e argument gere la profondeur (pas forcement present)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glColor4f (1.0, 1.0, 1.0, 1.0)
    
    glPushMatrix()
    
    # mouvement camera dynamique
    glLoadIdentity()
    # position, oeuil, ...
    gluLookAt(i, j, z, centeri, centerj, centerz, 0.0, 1.0, 0.0)
    
    # lance une serie de fonctions qui permettent de fabriquer le terrain
    fabriquerTerrain()
    # lance une serie de fonctions qui permettent de fabriquer le canon
    fabriquerCanon(taille)
    
    glPopMatrix()
    glutSwapBuffers()
    
    
def reshape(width, height):
    
    # ici c'est un copier / coller , aucune idee de ce qu'il s'y passe :D
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if width <= height:
        glOrtho(-2.5, 2.5, -2.5*height/width, 2.5*height/width, -10.0, 10.0)
    else:
        glOrtho(-2.5*width/height, 2.5*width/height, -2.5, 2.5, -10.0, 10.0)
    glMatrixMode(GL_MODELVIEW)
    

####################################
############## MAIN ################
####################################


glutInit()
# Le 2e argument gere les couleurs, le 3e la profondeur
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)

glutCreateWindow('Canon')
glutReshapeWindow(1000,700)
# Binding des fonctions aux actions d'OpenGL
glutReshapeFunc(reshape)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)

init()
glutMainLoop()















