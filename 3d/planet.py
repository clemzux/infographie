#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

###############################################################
# portage de planet.c

from OpenGL.GL import *  # exception car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

###############################################################
# variables globales
year, day, moon, nuages = 0, 0, 0, 0
quadric = None
# Paramètres de la source lumineuse
# ---Couleur
light_diffuse = [1.0 , 1.0, 1.0, 0.0]
# ---Position
light_position = [1.0 , 1.0, 1.0, 0.0]

# position camera
i = 0.0
j = 0.0
z = 5.0
centeri = 0.0
centerj = 0.0
centerz = 0.0

# textures

SOLEIL, TERRE, ATERRE, LUNE = 1, 2, 3, 4  # ID astre, planete, satellite
texture_planete = [None for i in range(5)]

earthT = None
sunT = None
cloudT = None
moonT = None

###############################################################
# 

def loadTexture(filename, ident):
    global texture_planete
    image = open(filename)  # retourne une PIL.image si import Image (!)
    
    ix = image.size[0]
    iy = image.size[1]
    image = image.tostring("raw", "RGBX", 0, -1)
    
    # 2d texture (x and y size)
    # BUG (?)
    #glBindTexture(GL_TEXTURE_2D, glGenTextures(1, texture_planete[ident]))
    texture_planete[ident] = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, int(texture_planete[ident]))

    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    # commente car alpha blinding (cf. atmosphere)
    #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

# Initialisation des librairies et du mode d'affichage
def init():
    global quadric
    # Autorisation des sources de lumière
    glEnable(GL_LIGHTING)
    # Autorisation pour la source de lumière n°0
    glEnable(GL_LIGHT0)
    # Autorisation des couleurs (obligatoire si "éclairé")
    glEnable(GL_COLOR_MATERIAL)
    # Autorisation de la profondeur
    glEnable(GL_DEPTH_TEST)
    # ????
    gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    # Couleur de fond (ici noir)
    glClearColor (0.0, 0.0, 0.0, 0.0)
    # Ombrage (SMOOTH plus rond, FLAT plus triangulaire)
    glShadeModel (GL_SMOOTH)
    quadric = gluNewQuadric()
    # Affichage de solides et non de traits
    gluQuadricDrawStyle(quadric, GLU_FILL)
    # Déclaration de la source de lumière n°0
    # ---Couleur
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    # ---Position
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    
    # perspective
    #glFrustum(-1.0, 1.0, -1.0, 1.0, 1.5, 20.0)
    
    # autoriser textures
    glEnable(GL_TEXTURE_2D)
    

def creerSoleil():
    
    # Création du "Soleil"
    gluSphere(quadric, 1.0, 20, 16)
    

def creerTerre():
    # Rotation de la "Terre" autour du "Soleil"
    glRotatef(year, 0.0, 1.0, 0.0)
    # Translation pour l'ajout de la "Terre"
    glTranslatef(2.0, 0.0, 0.0)
    # Rotation de la "Terre"
    glRotatef(day, 0.0, 1.0, 0.0)
    # Couleur bleue pour la "Terre"
    glColor4f (0.0, 0.0, 1.0, 1.0)
    # création de la "Terre"
    gluSphere(quadric, 0.2, 10, 8)


def creerNuages():
    # Rotation de la "Terre"
    # glRotatef(nuages, 0.0, 1.0, 0.0)
    # Couleur blblanche pour les nuages
    glColor4f (1.0, 1.0, 1.0, 0.0)
    # création des nuages
    gluSphere(quadric, 0.3, 10, 8)
    

def creerLune():
    # Translation pour l'ajout de la "Lune"
    glTranslatef(1.0, 0.0, 0.0)
    # Couleur blannche pour la "Lune"
    glEnable(GL_BLEND)
    glColor4f (1.0, 1.0, 1.0, 1.0)
    glRotatef(moon, 0.0, 1.0, 0.0)
    # création de la "Lune"
    gluSphere(quadric, 0.1, 10, 8)
    

# Affichage (appelé à chaque appui sur une touche)
def display():

	# Le 2e argument gère la profondeur (pas forcément présent)
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Couleur du prochain élément créé (jaune pour le "Soleil")
    glColor4f (1.0, 1.0, 0.0, 1.0)
    
    glPushMatrix()
    
    # mouvement camera dynamique
    glLoadIdentity()
    gluLookAt(i, j, z, centeri, centerj, centerz, 0.0, 1.0, 0.0)
    
    creerSoleil()
    creerTerre()
    creerNuages()
    creerLune()
    
    glPopMatrix()
	# Comment fonctionnent les rotations ???
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

# Binding des touches
def keyboard(key, x, y):
    global day, year, moon, nuages, i, j, z, centeri, centerj, centerz
    if key == 'j':
        day = (day + 10) % 360
    elif key == 'J':
        day = (day - 10) % 360
    elif key == 'e':
        day = (day + 10) % 360
        moon = (moon + 10) % 24
        year = (year + 3) % 360
        nuages = (nuages + 10) % 24
    elif key == 'z':
        z -= 0.5
        centerz += 0.5
    elif key == 's':
        z += 0.5
        centerz -= 0.5
    elif key == 'q':
        i += 0.5
        centeri += 0.5
    elif key == 'd':
        i -= 0.5
        centeri -= 0.5
    elif key == 'g':
        j += 0.5
        centerj += 0.5
    elif key == 't':
        j -= 0.5
        centerj -= 0.5
    elif key == 'o':
        i += 0.5
        print(i)
    elif key == 'p':
        i -= 0.5
        print(i)
    elif key == '\033':
        sys.exit( )
    glutPostRedisplay()  # indispensable en Python

###############################################################
# MAIN

# Initialiation des librairies et du mode d'affichage
glutInit()
# Le 2e argument gère les couleurs, le 3e la profondeur
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
# Création de la fenêtre
glutCreateWindow('planet')
glutReshapeWindow(800,512)
# Binding des fonctions aux actions d'OpenGL
glutReshapeFunc(reshape)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)

init()

glutMainLoop()
