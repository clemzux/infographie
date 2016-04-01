#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

###############################################################
# portage de planet.c

from OpenGL.GL import *  # car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from Image import open

###############################################################
# variables globales
year, day = 0, 0  # Terre
luna, periode = 0, 0  # Lune
quadric = None
SOLEIL, TERRE, ATERRE, LUNE = 1, 2, 3, 4  # ID astre, planete, satellite
texture_planete = [None for i in range(5)]

# variables de mon fichier

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

###############################################################
# chargement des textures

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

###############################################################
# creation des composants du systeme

def creerPlanete(rayon):
    ambient = (0.1, 0.1, 0.1, 1.0)
    diffuse = (0.8, 0.8, 0.8, 1.0)
    Black = (0.0, 0.0, 0.0, 1.0)
    sph1 = gluNewQuadric()

    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, Black)
    glMaterialfv(GL_FRONT, GL_EMISSION, ambient)
    glMaterialf(GL_FRONT, GL_SHININESS, 0.0)

    gluQuadricDrawStyle(sph1, GLU_FILL)
    gluQuadricNormals(sph1, GLU_SMOOTH)
    gluQuadricTexture(sph1, GL_TRUE)
    gluSphere(sph1, rayon, 100, 80)

def creerSoleil():

    # Création du "Soleil"
    
    creerPlanete(1.0)
    
def creerTerre():

    # Rotation de la "Terre" autour du "Soleil"
    glRotatef(year, 0.0, 1.0, 0.0)
    # Translation pour l'ajout de la "Terre"
    glTranslatef(2.0, 0.0, 0.0)
    # Rotation de la "Terre"
    glRotatef(day, 0.0, 1.0, 0.0)
    # création de la "Terre"
    
    creerPlanete(0.2)


def creerNuages():

    # Rotation de la "Terre" autour du "Soleil"
    glRotatef(year, 0.0, 1.0, 0.0)
    # Translation pour l'ajout de la "Terre"
    glTranslatef(2.0, 0.0, 0.0)
    # Rotation de la "Terre"
    glRotatef(day, 0.0, 1.0, 0.0)
    
    creerPlanete(0.21)

def creerLune():
    
    # Translation pour l'ajout de la "Lune"
    glTranslatef(4.0, 0.0, 0.0)
    # Couleur blannche pour la "Lune"

    glRotatef(moon, 0.0, 1.0, 0.0)
    
    creerPlanete(0.1)

###############################################################
# affichage

def display_sun():
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, SOLEIL)
    creerSoleil()
    glPopMatrix()

def display_earth():
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, TERRE)
    creerTerre()
    #glPopMatrix()

def display_atmosphere():
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, ATERRE)
    creerNuages()
    glPopMatrix()

def display_moon():
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, LUNE)
    creerLune()
    glPopMatrix()

###############################################################
# 

def init_texture():
    
    loadTexture('sun.bmp', SOLEIL)
    loadTexture('earth.bmp', TERRE)
    loadTexture('earthcld.bmp', ATERRE)
    loadTexture('moon.bmp', LUNE)
    

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

def display():
    # Le 2e argument gère la profondeur (pas forcément présent)
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Couleur du prochain élément créé (jaune pour le "Soleil")
    glColor4f (1.0, 1.0, 1.0, 1.0)
    
    glPushMatrix()
    
    # mouvement camera dynamique
    glLoadIdentity()
    gluLookAt(i, j, z, centeri, centerj, centerz, 0.0, 1.0, 0.0)
    
    display_sun()
    display_earth()
    display_atmosphere()
    display_moon()
    
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

init_texture()

init()

glutMainLoop()
