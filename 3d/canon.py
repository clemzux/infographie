from OpenGL.GL import *  # car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *
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

quadric = None

# couleurs

r = 0.0
g = 0.0
b = 0.0

# orientation canon

ic = 1.0
jc = 0.0
zc = 0.0
degCanon = 0.0


####################################
####### Fonctions objets3D #########
####################################


def setRGB(i, j, k):
    
    global r, g, b
    
    r = i
    g = j
    b = k


def fabriquerRectangle(taille):

    glColor3f(r, g, b)
    glutSolidCube(taille)
    glutSwapBuffers()
    

def fabriquerTerrain():
	
    global i, j, z

    glPushMatrix()

    setRGB(0.0,0.0,1.0)
    glScalef(1,0.1,1)
    fabriquerRectangle(4)
    
    glPopMatrix()
    glPushMatrix()
    
    glTranslatef(-3.0, 0.0, 0.0)
    setRGB(0.0, 1.0, 0.0)
    glScalef(1, 0.1, 2)
    fabriquerRectangle(2)
    
    glPopMatrix()
    glPushMatrix()
    
    glTranslatef(3.0, 0.0, 0.0)
    glScalef(1, 0.1, 2)
    fabriquerRectangle(2)
    
    i = -1
    j =  2
    
    glPopMatrix()
    

def fabriquerRoue(taille):

    # fabrication d'une roue
    
    glPushMatrix()

    # couleur marron de la roue (cylindre)
    glColor3f(0.4, 0.2, 0.05)
    
    # test de rotation pour voir toute la roue
    # glRotate(degCanon, ic, jc, zc)
    
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
    glRotate(-30, 1.0, 0.0, 0.0)
    gluCylinder(gluNewQuadric(), taille*0.5, taille*0.5*0.8, taille*4, 12, 12)
    
    glPopMatrix()
    
    
def fabriquerCanon(taille):
    
    # test de rotation pour voir tout le canon
    glRotate(degCanon, ic, jc, zc)
    
    # on se deplace sur le terrain de gauche
    glTranslate(-3.0, taille*2, 0.0)

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
    fabriquerTube(0.5)
    
    # on fabrique le fond du canon
    gluSphere(gluNewQuadric(), taille*0.49, 20, 20)


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
    gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
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
    gluLookAt(i, j, z, centeri, centerj, centerz, 0.0, 1.0, 0.0)
    
    # lance une serie de fonctions qui permettent de fabriquer le terrain
    fabriquerTerrain()
    # lance une serie de fonctions qui permettent de fabriquer le canon
    fabriquerCanon(0.5)
    
    glPopMatrix()
    glutSwapBuffers()
    
    
def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if width <= height:
        glOrtho(-2.5, 2.5, -2.5*height/width, 2.5*height/width, -10.0, 10.0)
    else:
        glOrtho(-2.5*width/height, 2.5*width/height, -2.5, 2.5, -10.0, 10.0)
    glMatrixMode(GL_MODELVIEW)
    
    
def keyboard(key, x, y):

    global i, j, z, centeri, centerj, centerz
    global degCanon
    
    if key == 's':
        j += 0.5
        centerj += 0.5
    elif key == 'z':
        j -= 0.5
        centerj -= 0.5
    elif key == 'q':
        i += 0.5
        centeri += 0.5
    elif key == 'd':
        i -= 0.5
        centeri -= 0.5
        
        
    elif key == 'o':
        degCanon += 10
    elif key == 'k':
        centerj -= 0.5
    elif key == 'l':
        i -= 0.5
        centeri -= 0.5
    elif key == 'm':
        i -= 0.5
        centeri -= 0.5
    elif key == '\033':
        sys.exit( )
    glutPostRedisplay()  # indispensable en Python
    

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















